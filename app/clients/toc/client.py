import os
from typing import Any

from langchain_anthropic import ChatAnthropic
from langgraph.graph import END, START, StateGraph
from pydantic import SecretStr

from app.clients.toc.state import TocState
from app.clients.toc.utils import model_chain
from app.schemas.api import TocRequest, TocResponse


class TocClient:
    def __init__(self) -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable must be set")
        self.model = ChatAnthropic(model="claude-sonnet-4-6", api_key=SecretStr(api_key))  # type: ignore[call-arg]
        self.graph = self._build_graph()

    def _generate_toc(self, state: TocState) -> dict[str, Any]:
        chain = model_chain("generate_toc", self.model)

        keywords_dict = state.keywords
        keywords_parts = []
        keywords_parts.append(f"Primary Keyword: {keywords_dict['primary_keyword']}")
        if keywords_dict.get("secondary_keywords"):
            keywords_parts.append(
                f"Secondary Keywords: {', '.join(keywords_dict['secondary_keywords'])}"
            )
        if keywords_dict.get("supporting_keywords"):
            keywords_parts.append(
                f"Supporting Keywords: {', '.join(keywords_dict['supporting_keywords'])}"
            )
        keywords_str = "\n".join(keywords_parts)

        toc_schema = chain.invoke(
            {
                "generic_rules": state.generic_rules,
                "company_metadata": state.company_metadata,
                "company_toc_rules": state.company_toc_rules,
                "keywords": keywords_str,
                "title": state.title,
                "type_of_blog": state.type_of_blog,
            }
        )

        return {
            "toc": toc_schema.toc,
        }

    def _build_graph(self) -> Any:
        graph = StateGraph(TocState)
        graph.add_node("generate_toc", self._generate_toc)
        graph.add_edge(START, "generate_toc")
        graph.add_edge("generate_toc", END)
        compiled_graph = graph.compile()
        return compiled_graph

    def invoke(self, input_state: TocRequest) -> TocResponse:
        initial_state = TocState(
            generic_rules=input_state.generic_rules,
            company_metadata=input_state.company_metadata,
            company_toc_rules=input_state.company_toc_rules,
            keywords=input_state.keywords.model_dump(),
            title=input_state.title,
            type_of_blog=input_state.type_of_blog,
        )

        result_state_data = self.graph.invoke(initial_state)

        if isinstance(result_state_data, dict):
            toc_dict = result_state_data.get("toc")
        else:
            toc_dict = getattr(result_state_data, "toc", None)

        if toc_dict is None:
            raise ValueError("TOC generation failed - no TOC was generated")

        return TocResponse(toc=toc_dict)


def generate_toc_client() -> TocClient:
    return TocClient()
