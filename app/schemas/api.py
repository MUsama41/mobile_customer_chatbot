from typing import Dict, List

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class StatusResponse(BaseModel):
    service: str
    status: str


class KeywordsRequest(BaseModel):
    primary_keyword: str
    secondary_keywords: List[str]
    supporting_keywords: List[str]


class TocApiRequest(BaseModel):
    keywords: KeywordsRequest
    title: str
    type_of_blog: str


class TocRequest(BaseModel):
    generic_rules: str
    company_metadata: str
    company_toc_rules: str
    keywords: KeywordsRequest
    title: str
    type_of_blog: str


class TocResponse(BaseModel):
    toc: Dict[str, List[str]]
