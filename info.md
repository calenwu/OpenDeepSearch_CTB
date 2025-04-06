you need to modify:
`venv/lib/python3.11/site-packages/gradio_client/utils.py`
In line 897:
you need to add

```
if isinstance(schema, bool):
		return "boolean"
```

```
def get_type(schema: dict):
    if isinstance(schema, bool):
        return "boolean"
    if "const" in schema:
```

docker run --rm \
 -d -p 8080:8080 \
 -v "${PWD}/searxng:/etc/searxng" \
 -e "BASE_URL=http://localhost:8080/" \
 -e "INSTANCE_NAME=my-instance" \
 -e "UWSGI_WORKERS=64" \
 searxng/searxng

python evals/autograde_df.py --num_cpus 12 /Users/georgye/Documents/repos/OpenDeepSearch_CTB/output/fireworks_ai**accounts**fireworks**models**llama-v3p3-70b-instruct/codeact/frames_test_set/fireworks_ai**accounts**fireworks**models**llama-v3p3-70b-instruct**codeact**frames_test_set\_\_trial0.jsonl

# requires ~16-32GB VRAM NVIDIA Compute Capability >= 8.0

docker run \
-v $PWD/data:/app/.cache
--runtime=nvidia \
--gpus "0" -p "7997":"7997" \
michaelf34/infinity:0.0.68-trt-onnx \
v2 --model-id Alibaba-NLP/gte-Qwen2-7B-instruct --revision "refs/pr/38" \
--dtype bfloat16 --batch-size 8 --device cuda --engine torch --port 7997 \
--no-bettertransformer

docker run \
 --rm \
 --runtime=nvidia \
 --gpus all \
 -v $PWD/data:/app/.cache \
 -p 7997:7997 \
 michaelf34/infinity:0.0.68-trt-onnx \
 v2 --model-id Alibaba-NLP/gte-Qwen2-7B-instruct --revision "refs/pr/38" \
 --dtype bfloat16 --batch-size 8 --device cuda --engine torch --port 7997 \
 --no-bettertransformer

port=7997
model1=michaelfeil/bge-small-en-v1.5
model2=mixedbread-ai/mxbai-rerank-xsmall-v1
volume=$PWD/data

docker run -it --gpus all \
 --runtime=nvidia \
 -v $PWD/data:/app/.cache \
 -p 7997:7997 \
 michaelf34/infinity:latest \
 v2 \
 --model-id mixedbread-ai/mxbai-rerank-xsmall-v1 \
 --model-id michaelfeil/bge-small-en-v1.5 \
 --port 7997

python ./evals/eval_tasks.py --parallel-workers=32 --num-trials=1 --eval-tasks=./evals/datasets/frames_test_set.csv

`wc -l '/Users/georgye/Documents/repos/OpenDeepSearch_CTB/output/fireworks_ai__accounts__fireworks__models__llama-v3p3-70b-instruct/codeact/frames_test_set/fireworks_ai__accounts__fireworks__models__llama-v3p3-70b-instruct__codeact__frames_test_set__trial0.jsonl'`

`python evals/autograde_df.py --num_cpus 25 /Users/georgye/Documents/repos/OpenDeepSearch_CTB/output/fireworks_ai__accounts__fireworks__models__llama-v3p3-70b-instruct/codeact/frames_test_set/fireworks_ai__accounts__fireworks__models__llama-v3p3-70b-instruct__codeact__frames_test_set__trial0_copy.jsonl`
