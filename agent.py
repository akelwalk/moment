import json
import operator
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END
from json_repair import repair_json

# agent state definition
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

# base agent class
class Agent:
    def __init__(self, model, tools, system_prompt=""):
        print("--- Agent Initializing ---")
        self.last_message = ""
        self.system = system_prompt
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

        # graph definition
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_llm)
        graph.add_node("action", self.take_action)        
        graph.add_conditional_edges( # conditional edge: llm -> exists_action -> action or END
            "llm",
            self.exists_action,
            {True: "action", False: END} # route to action if tool calls exist, else end
        )
        graph.add_edge("action", "llm") # edge: action -> llm 
        graph.set_entry_point("llm") # set entry point        
        self.graph = graph.compile() # compile graph

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        has_tool_calls = hasattr(result, 'tool_calls') and len(result.tool_calls) > 0
        return has_tool_calls

    def call_llm(self, state: AgentState):
        print("\n--- Calling LLM ---")
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def take_action(self, state: AgentState):
        print("\n--- Calling Tool ---")
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}") 
            result = self.tools[t["name"]].invoke(t["args"])
            results.append(ToolMessage(tool_call_id=t["id"], name=t["name"], content=str(result)))
        return {'messages': results}

    def run(self, inputData):
        messages = [HumanMessage(content=inputData)]
        # invoke the graph
        result_state = self.graph.invoke({"messages": messages}, {"recursion_limit": 10})
        # process the final message
        if result_state and 'messages' in result_state and result_state['messages']:
            final_message_content = result_state['messages'][-1].content
            self.last_message = self.clean_result(final_message_content) 
        else:
            self.last_message = "// Error: No final message content from agent."

        return result_state # return the full state as before
    
    def clean_result(self, result):
        i1 = result.find("{")
        i2 = result.find("}")
        if i1 == -1 or i2 == -2:
            return "// Error: JSON object not contained within { } braces"
        cleaned = result[i1:i2+1].strip().replace("\n", "").replace("  ", "")
        return repair_json(cleaned)
