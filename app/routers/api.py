import os

from fastapi import APIRouter

from app.clients.toc import generate_toc_client
from app.schemas.api import HealthResponse, StatusResponse, TocApiRequest, TocRequest, TocResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def read_health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/status", response_model=StatusResponse)
def read_status() -> StatusResponse:
    return StatusResponse(service="content_tool", status="running")


@router.post("/toc", response_model=TocResponse)
def toc_generation(request: TocApiRequest) -> TocResponse:
    knowledge_base_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "knowledge_base"
    )

    with open(os.path.join(knowledge_base_dir, "ground_truth", "toc_skills.md"), "r") as f:
        generic_rules = f.read()

    with open(os.path.join(knowledge_base_dir, "ground_truth", "company_metadata.md"), "r") as f:
        company_metadata = f.read()

    with open(os.path.join(knowledge_base_dir, "company_blogs", "toc.md"), "r") as f:
        company_toc_rules = f.read()

    toc_request = TocRequest(
        generic_rules=generic_rules,
        company_metadata=company_metadata,
        company_toc_rules=company_toc_rules,
        keywords=request.keywords,
        title=request.title,
        type_of_blog=request.type_of_blog,
    )

    toc_client = generate_toc_client()
    toc_response = toc_client.invoke(toc_request)

    return TocResponse(toc=toc_response.toc)
