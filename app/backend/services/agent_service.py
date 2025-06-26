from typing import Dict


def trigger_agent(agent: Dict, event: Dict):
    if agent["type"] == "lambda":
        print(f"Invoking Lambda: {agent['endpoint']} with event {event}")
    elif agent["type"] == "bot":
        print(f"POST to bot webhook: {agent['endpoint']} with event {event}")
    elif agent["type"] == "ai":
        print(
            f"Calling internal AI service for agent {agent['name']} with event {event}"
        )
    else:
        print(f"Assigning task to human agent {agent['name']} (notify in UI)")


def handle_task_created(task: dict):
    # FLAW: The line below created a circular dependency and violated architecture layers.
    # A service should NOT import from the API layer, especially for data access.
    # For demonstration purposes, re-adding the import to maintain in-memory demo functionality.
    from app.backend.api.agents import agents_db

    # In a real system, you would get a DB session and query for the agent.
    # e.g., agent = agent_crud.get(db, id=task['assigned_to'])
    agent = agents_db.get(task["assigned_to"])
    if not agent:
        print(f"Agent {task['assigned_to']} not found for task {task['id']}")
        return
    print(f"[Workflow] Auto-executing task {task['id']} for agent {agent['name']}")
    trigger_agent(agent, task)
    # Strategic contenting logic
    if "content" in task["type"].lower():
        content = generate_strategic_content(task)
        print(f"[Workflow] Generated content: {content}")
    # Smart marketing logic
    if "marketing" in task["type"].lower():
        content = generate_strategic_content(task)
        marketing_result = execute_smart_marketing(task, content)
        print(f"[Workflow] Marketing result: {marketing_result}")


def generate_strategic_content(task: dict):
    # Simulate strategic content generation logic
    print(
        f"[StrategicContent] Generating high-impact content for task {task['id']} (type: {task['type']})"
    )
    # TODO: Integrate with AI/ML models for content ideation, SEO, and trend analysis
    return {
        "title": f"Strategic Video Title for {task['type']}",
        "description": f"Auto-generated description for {task['type']} (task {task['id']})",
        "tags": ["ai", "automation", "growth"],
    }


def execute_smart_marketing(task: dict, content: dict):
    # Simulate smart marketing logic
    print(
        f"[SmartMarketing] Launching marketing campaign for task {task['id']} with content title: {content['title']}"
    )
    # TODO: Integrate with social media APIs, email, influencer outreach, etc.
    return {"campaign_id": f"mktg-{task['id']}", "status": "launched"}
