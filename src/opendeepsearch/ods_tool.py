from typing import Optional, Literal
from smolagents import Tool
from opendeepsearch.ods_agent import OpenDeepSearchAgent
from litellm import completion, utils
import json
import re

class OpenDeepSearchTool(Tool):
    name = "web_search"
    description = """
    Performs web search based on your query (think a Google search) then returns the final answer that is processed by an llm."""
    inputs = {
        "query": {
            "type": "string",
            "description": "The search query to perform",
        },
    }
    output_type = "string"

    def __init__(
        self,
        model_name: Optional[str] = None,
        reranker: str = "jina",
        search_provider: Literal["serper", "searxng"] = "serper",
        serper_api_key: Optional[str] = None,
        searxng_instance_url: Optional[str] = None,
        searxng_api_key: Optional[str] = None
    ):
        super().__init__()
        self.search_model_name = model_name  # LiteLLM model name
        self.reranker = reranker
        self.search_provider = search_provider
        self.serper_api_key = serper_api_key
        self.searxng_instance_url = searxng_instance_url
        self.searxng_api_key = searxng_api_key

    def forward(self, query: str):
        answer = self.search_tool.ask_sync(query, max_sources=2, pro_mode=True)
        return answer

    def setup(self):
        self.search_tool = OpenDeepSearchAgent(
            self.search_model_name,
            reranker=self.reranker,
            search_provider=self.search_provider,
            serper_api_key=self.serper_api_key,
            searxng_instance_url=self.searxng_instance_url,
            searxng_api_key=self.searxng_api_key
        )
import json
from typing import Optional, Literal

class EnhancedOpenDeepSearchTool(Tool):
    name = OpenDeepSearchTool.name
    description = OpenDeepSearchTool.description
    inputs = {
        "query": {
            "type": "string",
            "description": "The search query to perform",
        },
    }
    output_type = OpenDeepSearchTool.output_type

    def __init__(
        self,
        model_name: Optional[str] = None,
        reranker: str = "jina",
        search_provider: Literal["serper", "searxng"] = "serper",
        serper_api_key: Optional[str] = None,
        searxng_instance_url: Optional[str] = None,
        searxng_api_key: Optional[str] = None
    ):
        super().__init__()
        self.search_model_name = model_name  # LiteLLM model name
        self.reranker = reranker
        self.search_provider = search_provider
        self.serper_api_key = serper_api_key
        self.searxng_instance_url = searxng_instance_url
        self.searxng_api_key = searxng_api_key

    def forward(self, query: str):
        # Perform the search using the improved query.
        answer_response = self.search_tool.ask_sync(query, max_sources=2, pro_mode=True)
        
        # Generate a concise answer from the search response.
        augmented_query_completion = completion(
            model=self.search_model_name,
            messages=[
                {"role": "user", "content": f"Given the query: {query} find an alternative query that might give a more detailed answer."}
            ],
            temperature=0.2,
            top_p=0.3
        )
        augmented_query = augmented_query_completion.choices[0].message.content
        answer_response_2 = self.search_tool.ask_sync(augmented_query, max_sources=2, pro_mode=True)

        # Generate a concise answer from the search response.
        concise_response_completion = completion(
            model=self.search_model_name,
            messages=[
                {"role": "user", "content": f"Given the query: {query}, and the answer: {answer_response}, make the answer as concise as possible but still answer the question. "}
            ],
            temperature=0.2,
            top_p=0.3
        )
        answer = concise_response_completion.choices[0].message.content
        # Generate a concise answer from the search response.
        concise_response_completion_2 = completion(
            model=self.search_model_name,
            messages=[
                {"role": "user", "content": f"Given the query: {augmented_query}, and the answer: {answer_response_2}, make the answer as concise as possible but still answer the question. "}
            ],
            temperature=0.2,
            top_p=0.3
        )
        answer_2 = concise_response_completion_2.choices[0].message.content

        print(f"query: {query}, answer: {answer}")
        print(f"query: {augmented_query}, answer: {answer_2}")

        final_answer_completion = completion(
            model=self.search_model_name,
            messages=[
                {"role": "user", "content": f"Given the query: {query}, and the answers: {answer_response} and {answer_response_2} find a final answer that is the most accurate and expansive."}
            ],
            temperature=0.2,
            top_p=0.3
        )
        final_answer = final_answer_completion.choices[0].message.content
        # Fallback return (ideally should not reach here).
        return final_answer

    def setup(self):
        self.search_tool = OpenDeepSearchAgent(
            self.search_model_name,
            reranker=self.reranker,
            search_provider=self.search_provider,
            serper_api_key=self.serper_api_key,
            searxng_instance_url=self.searxng_instance_url,
            searxng_api_key=self.searxng_api_key
        )
