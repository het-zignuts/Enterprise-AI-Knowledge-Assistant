from app.prompt.prompt import PROMPT
from app.llm.llm import get_llm
from langchain_core.output_parsers import PydanticOutputParser
from app.schemas.responses import AssistantResponse
import json

def generate_answer(context: str, question: str) -> str:
    """
    This functions creates a LangChain and returns the response genrated by passing the query along with the context to the chain.
    """
    if context is None:
        return "No matching information identified. Please upload relevant documents."

    llm=get_llm() # get the LLM instance
    prompt=PROMPT # a reusable prompt template
    parser=PydanticOutputParser(pydantic_object=AssistantResponse) # parser instance to parser the LLM response accroding to given pydantic schema.

    chain= prompt | llm | parser # creating the LangChain

    response=chain.invoke({"context": context, "question": question}) # invoke the chain with the context and query values passed which will be substituted into the prompt before passing to LLM.
    return response.model_dump() # send a dict object as response