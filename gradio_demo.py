from smolagents import CodeAgent, GradioUI, LiteLLMModel
from opendeepsearch import OpenDeepSearchTool
import os
from dotenv import load_dotenv
import argparse


QWEN_2_5_32B = 'fireworks_ai/accounts/fireworks/models/qwen2p5-32b'
LLAMA_3_3 = 'fireworks_ai/accounts/fireworks/models/llama-v3p3-70b-instruct'
# LLAMA_3_3 = 'fireworks_ai/llama-v3p1-70b-instruct'
# QWEN_2_5_32B = 'accounts/fireworks/models/qwen2p5-32b'
# LLAMA_3_3 = 'accounts/fireworks/models/llama-v3p3-70b-instruct'
# Load environment variables
load_dotenv()

print("🔍 DEBUG: LITELLM_SEARCH_MODEL_ID =", os.getenv("LITELLM_SEARCH_MODEL_ID"))
print("🔍 DEBUG: LITELLM_ORCHESTRATOR_MODEL_ID =", os.getenv("LITELLM_ORCHESTRATOR_MODEL_ID"))
print("🔍 DEBUG: SERPER_API_KEY =", os.getenv("SERPER_API_KEY"))

# Add command line argument parsing
parser = argparse.ArgumentParser(description='Run the Gradio demo with custom models')
parser.add_argument('--model-name',
    default=os.getenv("LITELLM_SEARCH_MODEL_ID", QWEN_2_5_32B),
    help='Model name for search')
parser.add_argument('--orchestrator-model',
    default=os.getenv("LITELLM_ORCHESTRATOR_MODEL_ID", QWEN_2_5_32B),
    help='Model name for orchestration')
parser.add_argument('--reranker',
    choices=['jina', 'infinity'],
    default='jina',
    help='Reranker to use (jina or infinity)')
parser.add_argument('--search-provider',
    choices=['serper', 'searxng'],
    default='serper',
    help='Search provider to use (serper or searxng)')
parser.add_argument('--searxng-instance',
    help='SearXNG instance URL (required if search-provider is searxng)')
parser.add_argument('--searxng-api-key',
    help='SearXNG API key (optional)')
parser.add_argument('--serper-api-key',
    help='Serper API key (optional, will use SERPER_API_KEY env var if not provided)',
    default=os.getenv("SERPER_API_KEY"))
parser.add_argument('--openai-base-url',
    help='OpenAI API base URL (optional, will use OPENAI_BASE_URL env var if not provided)')
parser.add_argument('--server-port',
    type=int,
    default=7860,
    help='Port to run the Gradio server on')

args = parser.parse_args()

# Validate arguments
if args.search_provider == 'searxng' and not (args.searxng_instance or os.getenv('SEARXNG_INSTANCE_URL')):
    parser.error("--searxng-instance is required when using --search-provider=searxng")

# Set OpenAI base URL if provided via command line
if args.openai_base_url:
    os.environ["OPENAI_BASE_URL"] = args.openai_base_url

# Use the command line arguments
search_tool = OpenDeepSearchTool(
    model_name=LLAMA_3_3,
    reranker=args.reranker,
    search_provider=args.search_provider,
    serper_api_key=args.serper_api_key,
    searxng_instance_url=args.searxng_instance,
    searxng_api_key=args.searxng_api_key
)
print("LLAMA_3_3 =", LLAMA_3_3)
print('args.orchestrator_model')
print(args.orchestrator_model)
model = LiteLLMModel(
    model_id=LLAMA_3_3,
    temperature=0.2,
)

# Initialize the agent with the search tool
agent = CodeAgent(tools=[search_tool], model=model)

# Add a name when initializing GradioUI
GradioUI(agent).launch(server_name="127.0.0.1", server_port=args.server_port, share=False)
