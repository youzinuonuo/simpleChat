from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from utils.api_key_utils import get_api_key
from utils.client_functions import get_client_info_tool
from autogen_core import CancellationToken
import json

class ClientDataAgent:
    def __init__(self):
        self.model_client = AzureOpenAIChatCompletionClient(
            azure_endpoint='https://r2d2-c3p0-genaihub.apps.nsroot.net/azure',
            api_key=get_api_key(),
            api_version='2024-02-15-preview',
            model='gpt-4',
            azure_deployment='gpt-4-deployment'
        )
        
        self.agent = AssistantAgent(
            name="client_data_expert",
            model_client=self.model_client,
            system_message="""You are a client data expert. Your main tasks are:

1. Understand what specific information of client the user is looking for
2. Use the appropriate tools to retrieve relevant data
3. Extract ONLY the specific information the user wants from the response
4. Present the information in a clear, concise manner

Important guidelines:
- Focus only on answering the user's specific question
- DO NOT return the entire API response, only extract the relevant portions

Examples of good responses:
- User: "What is John Smith's phone number?"
  You: "John Smith's phone number is 123-456-789."
- User: "Is client whose member number is 123456789 account active?"
  You: "Yes, your account is currently active."
- User: "Tell me about Jane Doe's recent activity"
  You: "Jane's account showed 3 transactions in the past month, with the most recent one on August 15th."
""",
            tools=[get_client_info_tool]  # Add the function tool here
        )

    async def analyze_query(self, query: str) -> dict:
        """Analyze client data query and provide answer"""
        cancellation_token = CancellationToken()
        response = await self.agent.on_messages([
            TextMessage(source="user", content=query)
        ], cancellation_token=cancellation_token)
        
        return {
            "answer": response.chat_message.content
        }
        
    async def simple_query(self, query: str) -> str:
        """Simple test method that returns a fixed response"""
        return f"I'm client data agent, I will analyze your query: '{query}'"
