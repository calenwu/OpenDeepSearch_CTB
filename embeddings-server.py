import requests
base_url = "http://172.81.127.5:8000"

rerank_url = base_url + "/rerank"
model1 = "mixedbread-ai/mxbai-rerank-xsmall-v1"
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

vastai create instance 8932368 --image michaelf34/infinity:latest --env '-p 8000:8000' --disk 40 --args v2 --model-id mixedbread-ai/mxbai-rerank-xsmall-v1 --port 8000