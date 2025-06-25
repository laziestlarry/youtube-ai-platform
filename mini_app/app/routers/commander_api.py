from fastapi import APIRouter, HTTPException, Body
from typing import List

from ..models import (
    CommercialIdeaRequest,
    CommercialIdea,
    PipelineInitiationRequest
)
from ..services.idea_generator import CommercialIdeaGenerator
from ..services.pipeline_initiator import MainPipelineInitiator

router = APIRouter()
idea_gen_service = CommercialIdeaGenerator()
pipeline_init_service = MainPipelineInitiator()

@router.post("/ideas", response_model=List[CommercialIdea], summary="Generate Commercial Video Ideas")
async def generate_commercial_ideas_endpoint(request: CommercialIdeaRequest):
    """
    Generates a list of commercially-focused YouTube video ideas based on a niche.
    
    Optionally includes a basic revenue projection for each idea.
    """
    try:
        ideas = await idea_gen_service.generate_ideas(
            niche=request.niche,
            focus=request.focus,
            count=request.count,
            project_revenue=request.project_revenue,
            estimated_views=request.estimated_views,
            estimated_cpm=request.estimated_cpm,
        )
        return ideas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")

@router.post("/initiate-pipeline", response_model=dict, summary="Initiate a Video Pipeline in the Main App")
async def initiate_main_pipeline_endpoint(request: PipelineInitiationRequest):
    """
    Takes a generated commercial idea and sends it to the main platform
    to initiate the full video production pipeline.
    """
    try:
        result = await pipeline_init_service.initiate(request.idea, request.target_platform_url)
        return result
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "healthy", "app": "YouTube Income Commander Mini"}