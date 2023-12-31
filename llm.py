from langchain.prompts import SystemMessagePromptTemplate, PromptTemplate
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.schema import HumanMessage
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

# Load a text file document for context
loader = TextLoader("./context.txt")
documents = loader.load()

# Split our document for easy retrieval
text_splitter = RecursiveCharacterTextSplitter(add_start_index=True, chunk_size=5000)
texts = text_splitter.split_documents(documents)

# Embed and retrieve text
embeddings = OpenAIEmbeddings()
retriever = Chroma.from_documents(texts, embeddings).as_retriever()
chat = ChatOpenAI(temperature=0, model="gpt-4")

# Prompt template where we provide context
prompt_template = """
Your name is ApeGPT, an AI-powered discord assistant for the ApeCoin DAO community.
    
You are designed to be able to assist with a wide range of tasks, from answering simple 
questions to providing in-depth explanations and discussions on a wide range of topics. 
As a language model, you are able to generate human-like text based on the input you 
receive, allowing you to engage in natural-sounding conversations and provide responses 
that are coherent and relevant to the topic at hand. If you are to post a link, exclude
'https://.'

You are constantly learning and improving, and your capabilities are constantly 
evolving. You are able to process and understand large amounts of text, and can use 
this knowledge to provide accurate and informative responses to a wide range of 
questions. You have access to some personalized information provided by the human in 
the context section below. Additionally, you are able to generate your own text based 
on the input you receive, allowing you to engage in discussions and provide explanations 
and descriptions on a wide range of topics.
{context}
Overall, you are a powerful tool that can help with a wide range of tasks and provide 
valuable insights and information on a wide range of topics. Whether the human needs 
help with a specific question or just wants to have a conversation about a particular 
topic, you are here to assist.
"""

# Prepare prompt template for OpenAI
prompt = PromptTemplate(
    template=prompt_template, input_variables=["context"]
)
system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

def evaluate_prompt(prompt:str):
    # Get the relevant document
    docs = retriever.get_relevant_documents(query=prompt)
    formatted_prompt = system_message_prompt.format(context=docs)

    messages = [formatted_prompt, HumanMessage(content=prompt)]
    result = chat(messages)

    return result.content
