from app.prompt.prompt import PROMPT
from app.llm.llm import get_llm
from langchain_core.output_parsers import PydanticOutputParser
from app.schemas.responses import AssistantResponse
import json

def generate_answer(context: str, question: str) -> str:
    if context is None:
        return "No matching information identified. Please upload relevant documents."

    llm=get_llm()
    prompt=PROMPT
    parser=PydanticOutputParser(pydantic_object=AssistantResponse)

    chain= prompt | llm | parser

    response=chain.invoke({"context": context, "question": question})
    return response.model_dump()