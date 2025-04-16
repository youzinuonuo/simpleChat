from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage, HandoffMessage
from utils.api_key_utils import get_api_key
import json
from autogen_core import CancellationToken
class PlanAgent:
    def __init__(self):
        # Initialize model client
        self.model_client = AzureOpenAIChatCompletionClient(
            azure_endpoint='https://r2d2-c3p0-genaihub.apps.nsroot.net/azure',
            api_key=get_api_key(),  
            api_version='2024-02-15-preview',
            model='gpt-4',
            azure_deployment='gpt-4-deployment',
            # Disable parallel tool calls to ensure only the first handoff is executed
            parallel_tool_calls=False
        )
        
        # Initialize planning agent with handoffs parameter
        # Using string list to specify potential handoff targets
        self.agent = AssistantAgent(
            name="planner",
            model_client=self.model_client,
            system_message="""You are a planning expert. Your tasks are:
            1. Analyze user query intent
            2. Determine if the query is about general knowledge or client data
            
            If the query is about general knowledge, transfer the conversation to the 
            knowledge_agent using the HandoffMessage format.
            
            If the query is about client data, transfer the conversation to the 
            client_data_agent using the HandoffMessage format.
            
            Before making a decision, carefully think about the query content and choose 
            the most appropriate specialist to handle it.
            """,
            handoffs=["knowledge_agent", "client_data_agent"]  # Specify potential handoff targets
        )
    
    async def analyze_query(self, query: str) -> dict:
        """Analyze the query and route to appropriate agent"""
        # Send user query to planning agent
        cancellation_token = CancellationToken()
        response = await self.agent.on_messages([
            TextMessage(source="user", content=query)
        ], cancellation_token=cancellation_token)
        
        # Check if response is a HandoffMessage
        if isinstance(response.chat_message, HandoffMessage):
            # Extract handoff target
            target = response.chat_message.target
            
            # Route based on target agent
            if target == "knowledge_agent":
                from agents.base_knowledge_agent import BaseKnowledgeAgent
                knowledge_agent = BaseKnowledgeAgent()
                return await knowledge_agent.analyze_query(query)
                
            elif target == "client_data_agent":
                from agents.client_data_agent import ClientDataAgent
                client_data_agent = ClientDataAgent()
                return await client_data_agent.analyze_query(query)
            else:
                return {"answer": f"Unknown target agent: {target}"}
        else:
            # If not a HandoffMessage, try to determine from content
            content = response.chat_message.content.lower()
            
            # Simple rule-based routing
            if "knowledge" in content:
                from agents.base_knowledge_agent import BaseKnowledgeAgent
                knowledge_agent = BaseKnowledgeAgent()
                return await knowledge_agent.analyze_query(query)
            elif "client" in content or "data" in content:
                from agents.client_data_agent import ClientDataAgent
                client_data_agent = ClientDataAgent()
                return await client_data_agent.analyze_query(query)
            else:
                return {"answer": content} 