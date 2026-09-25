from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq(model_name="openai/gpt-oss-120b",temperature=1)
template = "Matn o`zbek tiliga tarjima qiling: \n{english}"
prompt=PromptTemplate(input_variables=["english"],template=template)

chain = prompt | llm
response=chain.invoke({"english": "Kiss me hard before you go Summertime sadness"})
print(response.content)
