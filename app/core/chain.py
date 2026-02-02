from app.prompt.prompt import PROMPT
from app.llm.llm import get_llm

def generate_answer(context: str, question: str) -> str:
    llm=get_llm()

    if context is None:
        return "No matching information identified. Please upload relevant documents."

    prompt=PROMPT.format(
        context=context,
        question=question
    )

    response=llm.invoke(prompt)
    return response.content