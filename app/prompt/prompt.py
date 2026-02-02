from langchain_core.prompts import PromptTemplate
import os
from pathlib import Path 

BASE_DIR=Path(__file__).resolve().parent
file_pth=BASE_DIR/"prompt.txt"

with open(file_pth, "r") as file:
    template=file.read()

PROMPT=PromptTemplate(input_variables=["context", "question"], template=template)