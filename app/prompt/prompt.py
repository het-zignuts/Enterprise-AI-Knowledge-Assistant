from langchain_core.prompts import PromptTemplate
import os

with open("prompt.txt", "r") as file:
    template=file.read()

PROMPT=PromptTemplate(input_variables=["context", "question"], template=template)