from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from utils.api_key_utils import get_api_key
import json

class BaseKnowledgeAgent:
    def __init__(self):
        # self.model_client = AzureOpenAIChatCompletionClient(
        #     azure_endpoint='https://r2d2-c3p0-genaihub.apps.nsroot.net/azure',
        #     api_key=get_api_key(),
        #     api_version='2024-02-15-preview',
        #     model='gpt-4',
        #     azure_deployment='gpt-4-deployment'
        # )
        
        # self.agent = AssistantAgent(
        #     name="knowledge_expert",
        #     model_client=self.model_client,
        #     system_message="""You are a knowledge base expert. Your tasks are:
        #     1. Understand user query 
        #     2. Retrieve relevant information from knowledge base
        #     3. Integrate knowledge and form a comprehensive answer
            
        #     Please return your analysis in JSON format:
        #     {
        #         "knowledge_found": true/false,
        #         "relevant_info": "relevant knowledge content",
        #         "answer": "complete and informative answer",
        #         "confidence": 0.0-1.0
        #     }"""
        # )
        pass

    async def analyze_query(self, query: str) -> dict:
        """Analyze knowledge query and provide answer"""
        # Simple test response without connecting to the actual agent
        return {
            "knowledge_found": True,
            "relevant_info": "This is a test response",
            "answer": f"I'm base knowledge agent, I will analyze your query: '{query}'"
        }
        
    async def simple_query(self, query: str) -> str:
        """Simple test method that returns a fixed response"""
        return f"I'm base knowledge agent, I will analyze your query: '{query}'"
