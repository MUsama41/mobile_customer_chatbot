from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable

from app.clients.toc.prompts import system_prompt, user_prompt
from app.schemas.api import TocResponse


def model_chain(func_key: str, model: BaseChatModel) -> RunnableSerializable[dict[str, Any], Any]:
    if func_key == "generate_toc":
        pydantic_parser = PydanticOutputParser(pydantic_object=TocResponse)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("user", user_prompt),
            ]
        )
        chain = prompt | model | pydantic_parser
        return chain
    else:
        raise ValueError(f"Function key {func_key} not found")
