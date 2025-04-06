from typing import Optional, Dict, Any
from litellm import completion
import os
from dotenv import load_dotenv
from .prompts import REASONING_REACT_PROMPT

load_dotenv()

class ReasoningAgent:
    """
    A reasoning agent that generates a chain of thought plan before the CodeAgent processes a query.
    This helps the CodeAgent formulate a more coherent approach to solving the query.
    """
    
    def __init__(
        self,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ):
        """
        Initialize the reasoning agent.
        
        Args:
            model: The model to use for reasoning (defaults to the same as the CodeAgent)
            system_prompt: The system prompt to use for the reasoning model
            temperature: The temperature to use for the reasoning model
            max_tokens: The maximum number of tokens to generate
        """
        self.model = model
        self.system_prompt = REASONING_REACT_PROMPT
        self.temperature = temperature
        self.max_tokens = max_tokens
        
    def generate_plan(self, query: str) -> str:
        """
        Generate a chain of thought plan for the given query.
        
        Args:
            query: The user's query
            
        Returns:
            A string containing the chain of thought plan
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Create a detailed plan for answering this question: {query}"}
        ]
        response = completion(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        
        return response.choices[0].message.content
    
    def format_query_with_plan(self, query: str, plan: str) -> str:
        """
        Format the query with the plan to be used by the CodeAgent.
        
        Args:
            query: The user's query
            plan: The chain of thought plan
            
        Returns:
            A formatted string containing both the query and the plan
        """
        return f"""Question: {query}

Reasoning Plan:
{plan}

Please follow this exact plan step by step to answer the question, while using web_search to confirm the information you need specified by the step. Use the plan as a guide for your approach, but feel free to adapt if you discover new information that requires a different approach.

Make sure to output the final answer in pure string format, without formatting or markdown.
""" 