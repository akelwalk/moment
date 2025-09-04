from agent import Agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_ollama import ChatOllama
import json5
import os
from json_repair import repair_json

class JournalPromptAgent(Agent):
    input_format = {"entry": "contents of a previous journal entry"}
    output_format = {"prompts":["prompt1", "prompt2", "prompt3"]}
    normal_example = {
    "entry": "Work has been overwhelming lately. I feel like I can't keep up with all the deadlines, and it's making me anxious.",
    "prompts": [
        "What are the specific parts of work that feel most overwhelming right now?",
        "Can you recall a moment this week where you managed the stress more effectively than expected?",
        "How does your body usually signal to you that you're feeling anxious?"
    ]
    }
    sensitive_example = {
    "entry": "I feel hopeless. Nothing I do seems to matter, and I don't think I can handle much more of this.",
    "prompts": [
        "When you've felt this way before, what has helped you get through those difficult moments?",
        "Are there small daily routines or activities that bring you even a brief sense of calm or grounding?",
        "Who in your life has been a source of comfort or understanding when you've struggled?"
    ]
    }
    format_warning = """Return ONLY valid JSON. Follow these rules strictly:
    1. Use double quotes for all strings and keys.
    2. Do NOT wrap strings in extra single quotes.
    3. Do NOT add trailing commas.
    4. Do NOT add any text outside the JSON."""

    prompt = f"""You are an empathetic and knowledgeable reflection companion who is well versed in creating journal prompts for individuals to reflect deeply, navigate inner turmoil, and build resilience to overcome difficult situations, drawing inspiration from approaches such as cognitive behavioral therapy. 
    Given the text of a previous journal entry, create 3 relevant journal prompts that gently encourage the user to delve further into the topics the user had discussed in the entry.
    If there is no journal entry in the input, use the Tavilly web search tool to find inspiration to come up with general journaling prompts.
    Be professional, kind, and creative. Make sure to not encourage destructive behaviors. If the content is highly sensitive or indicates harm, respond with safe, general reflective prompts that focus on support.
    Input Format: {input_format}
    Always create 3 journaling prompts.
    Output Format: {output_format} 
    {format_warning}

    Here are some examples of expected inputs and outputs. These are just examples; try to make the actual journaling prompts different.
    Example 1: Normal entry (work stress)
    {normal_example}

    Example 2: Sensitive entry (hopelessness)
    {sensitive_example}
    """

    def __init__(self, model, tools):
        self.product_idea = ""
        super().__init__(model, tools, self.prompt)

    def run(self, inputData):
        self.product_idea = inputData
        result = super().run(inputData)
        return result
# # example usage of this class
# tavily_api_key= os.getenv("TAVILY_API_KEY")

# tools = [TavilySearchResults(max_results = 1, api_key = tavily_api_key)]
# model = ChatOllama(model="phi4-mini", temperature=1)
# journal_prompt_agent = JournalPromptAgent(model, tools)
# result = journal_prompt_agent.run("""entry: "Today was a mix of emotions. I woke up feeling anxious about an upcoming deadline, but after taking a short walk outside, I felt a bit calmer. Later in the day, I had a long conversation with a friend who reminded me not to be too hard on myself. That made me reflect on how often I focus on what I haven't done instead of appreciating the progress I've already made. I want to get better at celebrating small wins and practicing gratitude even during stressful times." """)
# print(journal_prompt_agent.last_message) #last message's content
# print("_____________________________________________________________________________")
# if journal_prompt_agent.last_message != "" and "Error" not in journal_prompt_agent.last_message: # last message could be empty or contain an error
#     dictionary = json5.loads(journal_prompt_agent.last_message)
#     print(dictionary)
#     prompts = dictionary["prompts"]
#     for i in range(len(prompts)):
#         prompts[i] = prompts[i].strip("'")
# else:
#     print(f"prompt agent's last message (could be empty): {journal_prompt_agent.last_message}")

