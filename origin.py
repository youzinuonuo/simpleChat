import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.utils import CancellationToken
from autogen_agentchat.teams import Swarm

# Configure model client
model_client = OpenAIChatCompletionClient(model="gpt-4o")

# Mock function to get client data
async def get_client_data(client_id: str) -> str:
    """Get client data"""
    return f"Client {client_id} data: Purchase amount $10,000, Latest purchase date 2023-05-15, Frequently purchased category: Electronics."

# Create knowledge expert agent
base_knowledge_agent = AssistantAgent(
    name="BaseKnowledgeAgent",
    model_client=model_client,
    system_message="You are a knowledge expert responsible for answering general knowledge questions. Please provide accurate and comprehensive answers."
)

# Create client data agent
client_data_agent = AssistantAgent(
    name="ClientDataAgent",
    model_client=model_client,
    system_message="You are a client data expert responsible for handling client data-related queries. Please provide detailed client data analysis.",
    tools=[get_client_data]  # Pass function directly, AutoGen will convert it to FunctionTool
)

# Create planning agent with handoffs parameter
planning_agent = AssistantAgent(
    name="PlanningAgent",
    model_client=model_client,
    system_message="""You are an intelligent router. You need to analyze user queries and decide which specialized agent to route them to:
    1. BaseKnowledgeAgent - handles general knowledge questions
    2. ClientDataAgent - handles client data-related questions
    
    Please make the best judgment based on the query content and use HandoffMessage to forward the query to the appropriate agent.
    """,
    handoffs=["BaseKnowledgeAgent", "ClientDataAgent"]  # Specify possible handoff targets
)

# Create a Swarm team to handle the routing automatically
router_team = Swarm(
    participants=[planning_agent, base_knowledge_agent, client_data_agent],
    max_turns=3  # Limit the maximum number of turns to prevent infinite loops
)

async def chatbot_service(query: str):
    """Chatbot service provided externally"""
    try:
        # Create a cancellation token
        cancellation_token = CancellationToken()
        
        # Start the conversation with the planning agent
        result = await router_team.run(
            messages=[TextMessage(source="user", content=query)],
            initial_speaker=planning_agent,  # Planning agent speaks first
            cancellation_token=cancellation_token
        )
        
        # Return the last message from the conversation
        if result.messages:
            return result.messages[-1].content
        else:
            return "No response generated."
    except Exception as e:
        return f"Error processing query: {str(e)}"

# Example usage
async def main():
    # Test general knowledge question
    knowledge_query = "What is artificial intelligence?"
    print(f"Question: {knowledge_query}")
    print(f"Answer: {await chatbot_service(knowledge_query)}")
    print()
    
    # Test client data question
    client_query = "Please analyze the purchase history of client ID12345"
    print(f"Question: {client_query}")
    print(f"Answer: {await chatbot_service(client_query)}")

if __name__ == "__main__":
    asyncio.run(main())

