from typing import List, Dict, Any
from ..config import settings
from ..models import CommercialIdea
import logging
from fastapi import HTTPException
import json
import vertexai
from vertexai.generative_models import GenerativeModel

from .revenue_projector import SimpleRevenueProjector

logger = logging.getLogger(__name__)

# Initialize Vertex AI. This will use Application Default Credentials on Google Cloud.
vertexai.init(project=settings.gcp_project_id, location=settings.gcp_region)

revenue_proj_service = SimpleRevenueProjector()

class CommercialIdeaGenerator:
    async def generate_ideas(
        self,
        niche: str,
        focus: str,
        count: int,
        project_revenue: bool,
        estimated_views: int,
        estimated_cpm: float,
    ) -> List[CommercialIdea]:
        prompt = f"""
        Generate {count} YouTube video ideas for the niche '{niche}' with a strong commercial focus on '{focus}'.
        For each idea, provide:
        - A catchy "title".
        - A brief "description" (1-2 sentences).
        - A "commercial_angle" (e.g., affiliate products, sponsorship type, high ad revenue potential).
        - An "estimated_cpm_range" (e.g., '$X-$Y') if applicable for '{focus}'.
        - A list of 3-5 relevant "keywords".
        """
        try:
            # Use Gemini 1.5 Pro for this task
            model = GenerativeModel("gemini-1.5-pro-preview-0409")
            
            system_instruction = """You are an expert YouTube content strategist.
                        You will generate video ideas based on user's niche and commercial focus.
                        You must respond with a valid JSON object containing a single key 'ideas',
                        which is a list of idea objects. Each object must have keys: 'title',
                        'description', 'commercial_angle', 'estimated_cpm_range', and 'keywords'."""
            
            response = await model.generate_content_async(
                [prompt],
                generation_config={
                    "response_mime_type": "application/json",
                },
                system_instruction=system_instruction
            )            
            content = response.text
            if not content:
                raise ValueError("Received empty content from Vertex AI.")

            ideas_data = json.loads(content).get("ideas", [])
            ideas = [CommercialIdea(**idea) for idea in ideas_data if idea.get("title")]

            if project_revenue:
                for idea in ideas:
                    projection = revenue_proj_service.project(
                        title=idea.title,
                        niche=niche,
                        estimated_views=estimated_views,
                        estimated_cpm=estimated_cpm,
                    )
                    idea.revenue_projection = projection

            return ideas[:count]

        except Exception as e:
            logger.error(f"Error generating commercial ideas: {e}")
            # Re-raise the exception to be handled by the router, which will create
            # a proper HTTP response.
            raise e