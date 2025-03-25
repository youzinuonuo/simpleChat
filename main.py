from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os

# Setup environment variables first
from utils.env_config import setup_environment
setup_environment()

from agents.plan_agent import PlanAgent

# Initialize FastAPI application
app = FastAPI(
    title="Intelligent Service API",
    description="Multi-Agent Service System Based on AutoGen",
    version="1.0.0"
)

# Initialize the planning agent (which initializes the team)
plan_agent = PlanAgent()

class ChatRequest(BaseModel):
    query: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    source_agent: Optional[str] = None

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Process the query through the plan agent
        result = await plan_agent.analyze_query(request.query)
        
        # Extract the answer
        if "answer" in result:
            answer = result["answer"]
        else:
            answer = "I couldn't process your query properly."
        
        # Determine the source agent
        source_agent = None
        if "knowledge_found" in result:
            source_agent = "knowledge_agent"
        elif "client_data_found" in result:
            source_agent = "client_data_agent"
        
        return ChatResponse(
            answer=answer,
            source_agent=source_agent
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
