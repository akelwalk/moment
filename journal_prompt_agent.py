from agent import Agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import json5
import os
from json_repair import repair_json

class JournalPromptAgent(Agent):
    input_format = {"entry": "contents of a previous journal entry"}
    output_format = {"prompt":["prompt"]}
    normal_example = {
    "entry": "Work has been overwhelming lately. I feel like I can't keep up with all the deadlines, and it's making me anxious.",
    "prompt": [
        "What are the specific parts of work that feel most overwhelming right now?"
    ]
    }
    sensitive_example = {
    "entry": "I feel hopeless. Nothing I do seems to matter, and I don't think I can handle much more of this.",
    "prompt": [
        "When you've felt this way before, what has helped you get through those difficult moments?"
    ]
    }
    format_warning = """Return ONLY valid JSON. Follow these rules strictly:
    1. Use double quotes for all strings and keys.
    2. Do NOT wrap strings in extra single quotes.
    3. Do NOT add trailing commas.
    4. Do NOT add any text outside the JSON.
    5. Follow the specified output format."""

    prompt = f"""You are an empathetic and knowledgeable reflection companion who is well versed in creating journal prompts for individuals to reflect deeply, navigate inner turmoil, and build resilience to overcome difficult situations, drawing inspiration from approaches such as cognitive behavioral therapy. 
    Given the text of a previous journal entry, create 1 relevant journal prompt that gently encourages the user to delve further into the topics the user had discussed in the entry.
    If there is no journal entry or user request for a specific prompt in the input, come up with a single general journaling prompt.
    Be professional, kind, and creative. Make sure to not encourage destructive behaviors. If the content is highly sensitive or indicates harm, respond with a safe, general reflective prompt that focus on support.
    Input Format: {input_format}
    Output Format: {output_format} Make sure to only create a single prompt!
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
        if not self.validate_input(inputData): # input validation step
            print("Invalid input!")
            inputData = json5.dumps({"entry": ""})  # force safe default if input is invalid

        self.product_idea = inputData
        result = super().run(inputData)
        return result
    
    def validate_input(self, inputData):
        if isinstance(inputData, str): # parsing json string into a dictionary
            try:
                inputData = json5.loads(inputData)  # json5 allows trailing commas etc.
            except Exception:
                return False  # invalid JSON

        if not isinstance(inputData, dict): # making sure the data type is a dictionary
            return False

        entry = inputData.get("entry") # making sure that the key entry is in the dictionary
        if not isinstance(entry, str):
            return False

        if len(entry) > 5000:  # prevent extremely long input - 5000 is the max characters that can be entered in a journal entry
            return False
        
        # prevent obvious injection patterns
        suspicious_patterns = ["import ", "exec(", "os.", "sys.", "open(", "<script>", "--", ";", "DROP ", "DELETE ", "INSERT ", "UPDATE ", "SELECT ", "UNION ", "' OR '1'='1", '" OR "1="1', "`"]
        if any(pat in entry for pat in suspicious_patterns):
            return False

        return True


