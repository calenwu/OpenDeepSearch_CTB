import requests, base64

# Use the base URL for the API endpoint
base_url = "http://81.166.173.12:11604"

# Prepare the payload with the desired model and input
payload = {
    "model": "mixedbread-ai/mxbai-embed-large-v1",
    "input": ["What is Deep Learning?", "What is Deep Learning?", "What is Deep Learning?"]
}

# Send a POST request to the /embeddings endpoint
response = requests.post(f"{base_url}/embeddings", json=payload)

# Check for successful response and print the embedding or error
if response.status_code == 200:
    data = response.json()
    print(data)
    embedding = data.get("data", [{}])[0].get("embedding")
    print("Embeddings:")
    print(embedding)
else:
    print("Error:", response.status_code, response.text)

# input_json = {"query": "Where is Munich?","documents": ["Munich is in Germany.", "The sky is blue."],"return_documents": "false","model": "mixedbread-ai/mxbai-rerank-xsmall-v1"}
# headers = {
#     "accept": "application/json",
#     "Content-Type": "application/json"
# }
    
# payload = {
#     "query": input_json["query"],
#     "documents": input_json["documents"],
#     "return_documents": input_json["return_documents"],
#     "model": model1
# }

# response = requests.post(rerank_url, json=payload, headers=headers)
    
# if response.status_code == 200:
#     resp_json = response.json()
#     print(resp_json)
# else: 
#     print(response.status_code)
#     print(response.text)

# vastai create instance 19210345 --image michaelf34/infinity:latest --env '-p 8000:8000' --disk 40 --args v2 --model-id mixedbread-ai/mxbai-embed-large-v1 --model-id mixedbread-ai/mxbai-rerank-xsmall-v1 --port 8000