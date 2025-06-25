from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RevenueProjection(BaseModel):
    title: str
    projected_ad_revenue: float
    notes: str

class CommercialIdea(BaseModel):
    title: str
    description: str
    commercial_angle: str
    estimated_cpm_range: Optional[str] = None # e.g., "$5-$15"
    keywords: List[str] = []
    revenue_projection: Optional[RevenueProjection] = Field(None, description="An optional, basic revenue projection for this idea.")

class CommercialIdeaRequest(BaseModel):
    niche: str = Field(..., description="Niche to generate ideas for")
    focus: str = Field("high_cpm", description="Focus for idea generation (e.g., high_cpm, affiliate_friendly)")
    count: int = Field(3, ge=1, le=10, description="Number of ideas to generate")
    project_revenue: bool = Field(True, description="Whether to include a revenue projection for each idea.")
    estimated_views: int = Field(10000, ge=1000, description="Estimated views for revenue projection.")
    estimated_cpm: float = Field(5.0, ge=0.1, description="Average CPM for the niche for revenue projection.")

class PipelineInitiationRequest(BaseModel):
    idea: CommercialIdea
    target_platform_url: Optional[str] = None # To override default if needed