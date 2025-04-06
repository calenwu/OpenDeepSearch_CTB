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
        "original_question": {
            "type": "string",
            "description": "Enter the full actual original question which was asked in the very beginning of the user prompt",
        },
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

    def forward(self, original_question: str, query: str):
        max_retries = 3
        retries = 0
        # Preserve the full original question for use in every iteration.
        full_original_question = original_question
        
        while retries < max_retries:
            # Perform the search using the improved query.
            answer_response = self.search_tool.ask_sync(query, max_sources=2, pro_mode=True)

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

            print(f"query: {query}, answer: {answer}")

            # If we've hit the maximum number of retries, return the final answer.
            if retries == max_retries - 1:
                return answer

            try:
                # Evaluate if the current answer is adequate or if a better search query is needed.
                evaluation_response = completion(
                    model=self.search_model_name,
                    messages=[
                        {
                            "role": "system", 
                            "content": (
                                f"Evaluate if the answer adequately addresses the question. If not, provide a better search query that might yield a more relevant answer. "
                                f"This result should get us closer to answering '{query}'. "
                                "Return a JSON with two fields: 'retry' (boolean) and either 'search_for' (string with improved search query if retry is true) or 'answer' (string with the answer if retry is false with a concise answer which answers the query)."
                            )
                        },
                        {"role": "user", "content": f"Question: {query}\nAnswer: {answer}"}
                    ],
                    temperature=0.2,
                    top_p=0.3
                )
                print(f"DEBUG for testing: {evaluation_response.choices[0].message.content}")

                # Parse the evaluation JSON response.
                try:
                    evaluation_json = json.loads(evaluation_response.choices[0].message.content)
                except json.JSONDecodeError as e:
                    print(evaluation_response.choices[0].message.content)
                    print(f"JSON Decode Error: {e}")
                    # Make a second LLM call to extract the JSON from the response.
                    # The LLM is instructed to extract only the JSON portion.
                    extraction_response = completion(
                        model=self.search_model_name,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "The following text contains a JSON response embedded within additional commentary. "
                                    "Extract and return only the JSON part nothing else!"
                                )
                            },
                            {
                                "role": "user",
                                "content": evaluation_response.choices[0].message.content
                            }
                        ],
                        temperature=0.2,
                        top_p=0.3
                    )
                    try:
                        raw_string = extraction_response.choices[0].message.content.replace("```", '').replace("json\n", '').replace('\n', '')
                        

                        # Step 2: Decode the escaped characters (like \n, \")
                        decoded = raw_string.encode().decode('unicode_escape')
                        # Step 3: Load as JSON
                        evaluation_json = json.loads(decoded)
                        # evaluation_json = json.loads(extraction_response.choices[0].message.content.replace('json\n'))
                    except Exception as ex:
                        print(f"Second extraction failed: {ex}")
                        raise ex
                    if evaluation_json.get('retry', False):
                        # Update the query for the next iteration.
                        new_query = evaluation_json.get('search_for', query)
                        query = new_query
                        retries += 1
                        continue
                    else:
                        # If no retry is needed, return the current answer.
                        return evaluation_json.get('answer', answer)
            except Exception as e:
                print(f"Error: {e}")
                raise e

        # Fallback return (ideally should not reach here).
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
