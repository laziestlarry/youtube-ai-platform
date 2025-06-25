import httpx
import logging
from ..config import settings
from ..models import CommercialIdea

logger = logging.getLogger(__name__)

class MainPipelineInitiator:
    async def initiate(self, idea: CommercialIdea, target_platform_url: str = None) -> dict:
        main_platform_url = target_platform_url or settings.main_platform_url
        # This endpoint should exist on the main platform to accept a brief and create a video draft.
        initiation_endpoint = f"{main_platform_url}/api/videos/initiate-from-brief/"

        payload = {
            "title": idea.title,
            "description": idea.description,
            "keywords": idea.keywords,
            "commercial_angle": idea.commercial_angle,
            "source": "youtube-income-commander-mini",
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(initiation_endpoint, json=payload, timeout=15)
                response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
                logger.info(f"Successfully initiated pipeline on main platform for: {idea.title}")
                return {"status": "success", "message": "Pipeline initiated on main platform.", "details": response.json()}
        except httpx.RequestError as e:
            logger.error(f"Failed to initiate pipeline on main platform for {idea.title}: {e}")
            raise ConnectionError(f"Could not connect to main platform at {initiation_endpoint}") from e
        except Exception as e:
            logger.error(f"An unexpected error occurred during pipeline initiation: {e}")
            raise e