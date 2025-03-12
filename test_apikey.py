import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage, HandoffMessage
from autogen_agentchat.utils import CancellationToken

# Configure model client with API key directly
model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key="<api_key>"  
)

# Create planning agent
planning_agent = AssistantAgent(
    name="PlanningAgent",
    model_client=model_client,
    system_message="""You are an intelligent router. You need to analyze user queries and decide which specialized agent to route them to:
    1. BaseKnowledgeAgent - handles general knowledge questions
    2. ClientDataAgent - handles client data-related questions
    
    Please make the best judgment based on the query content and use HandoffMessage to forward the query to the appropriate agent.
    """
)

async def test_planning_agent(query: str):
    """Test the planning agent's routing decision"""
    print(f"\nQuery: {query}")
    
    # Create a cancellation token
    cancellation_token = CancellationToken()
    
    # Get planning agent's response
    planning_response = await planning_agent.on_messages([
        TextMessage(source="user", content=query)
    ], cancellation_token=cancellation_token)
    
    # Check if planning_agent generated a HandoffMessage
    if isinstance(planning_response, HandoffMessage):
        print(f"Decision: Route to {planning_response.target}")
        print(f"Reason: {planning_response.content}")
    else:
        print(f"Response: {planning_response.content}")
    
    print("-" * 50)

async def main():
    print("Planning Agent Test - Enter 'exit' to quit")
    print("-" * 50)
    
    while True:
        # Get user input from console
        query = input("\nEnter your query: ")
        
        # Check if user wants to exit
        if query.lower() in ['exit', 'quit', 'q']:
            print("Exiting test...")
            break
        
        # Process the query
        await test_planning_agent(query)

if __name__ == "__main__":
    asyncio.run(main())