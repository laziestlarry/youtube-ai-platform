from typing import List, Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

agents_db = {}


class AgentCreate(BaseModel):
    name: str
    type: Literal["human", "ai", "bot", "lambda"]
    skills: List[str] = []
    endpoint: str = ""  # For bots/lambdas: webhook or ARN
    is_active: bool = True


class AgentOut(AgentCreate):
    id: int


@router.get("/", response_model=List[AgentOut])
def list_agents():
    return list(agents_db.values())


@router.post("/", response_model=AgentOut)
def create_agent(agent: AgentCreate):
    agent_id = len(agents_db) + 1
    agent_out = AgentOut(id=agent_id, **agent.dict())
    agents_db[agent_id] = agent_out
    return agent_out


@router.get("/{agent_id}", response_model=AgentOut)
def get_agent(agent_id: int):
    agent = agents_db.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent
