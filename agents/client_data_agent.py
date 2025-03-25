from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from utils.api_key_utils import get_api_key
import json

class ClientDataAgent:
    def __init__(self):
        # self.model_client = AzureOpenAIChatCompletionClient(
        #     azure_endpoint='https://r2d2-c3p0-genaihub.apps.nsroot.net/azure',
        #     api_key=get_api_key(), 
        #     api_version='2024-02-15-preview',
        #     model='gpt-4',
        #     azure_deployment='gpt-4-deployment'
        # )
        
        # self.agent = AssistantAgent(
        #     name="client_data_expert",
        #     model_client=self.model_client,
        #     system_message="""You are a client data expert. Your tasks are:
        #     1. Understand user query related to client data
        #     2. Retrieve relevant information from client data
        #     3. Provide personalized answer based on client specifics
            
        #     Please return your analysis in JSON format:
        #     {
        #         "client_data_found": true/false,
        #         "client_info": "relevant client data",
        #         "answer": "personalized response",
        #         "confidence": 0.0-1.0
        #     }"""
        # )
        pass
    async def analyze_query(self, query: str) -> dict:
        """Analyze client data query and provide answer"""
        # Simple test response without connecting to the actual agent
        return {
            "client_data_found": True,
            "client_info": "This is a test client data",
            "answer": f"I'm client data agent, I will analyze your query: '{query}'"
        }
        
    async def simple_query(self, query: str) -> str:
        """Simple test method that returns a fixed response"""
        return f"I'm client data agent, I will analyze your query: '{query}'"
