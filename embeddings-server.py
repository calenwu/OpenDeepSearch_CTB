import requests
base_url = "213.181.123.81:37188"

from openai import OpenAI

# Modify OpenAI's API key and API base to use vLLM's's API server.
openai_api_key = "EMPTY"
openai_api_base = f"http://{base_url}/v1"
client = OpenAI(
	api_key=openai_api_key,
	base_url=openai_api_base,
)
model = "michaelfeil/bge-small-en-v1.5"
embeddings = client.embeddings.create(model=model, input="What is Deep Learning?").data[0].embedding
print("Embeddings:")
print(embeddings)

input_json = {"query": "Where is Munich?","documents": ["Munich is in Germany.", "The sky is blue."],"return_documents": "false","model": "mixedbread-ai/mxbai-rerank-xsmall-v1"}
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
    
payload = {
    "query": input_json["query"],
    "documents": input_json["documents"],
    "return_documents": input_json["return_documents"],
    "model": model1
}

response = requests.post(rerank_url, json=payload, headers=headers)
    
if response.status_code == 200:
    resp_json = response.json()
    print(resp_json)
else: 
    print(response.status_code)
    print(response.text)

# vastai create instance 8932368 --image michaelf34/infinity:latest --env '-p 8000:8000' --disk 40 --args v2 --model-id mixedbread-ai/mxbai-rerank-xsmall-v1 --port 8000