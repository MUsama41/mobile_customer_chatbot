from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class TocState(BaseModel):
    generic_rules: str
    company_metadata: str
    company_toc_rules: str
    keywords: Dict[str, Any]
    title: str
    type_of_blog: str
    toc: Optional[Dict[str, List[str]]] = None
