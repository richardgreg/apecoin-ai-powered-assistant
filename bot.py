import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import os
from langchain.prompts import SystemMessagePromptTemplate, PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.schema import HumanMessage

load_dotenv(find_dotenv())

# Load a text file document for context
loader = TextLoader("./context.txt")
documents = loader.load()

# Split our document for easy retrieval
text_splitter = CharacterTextSplitter(chunk_size=5000)
texts = text_splitter.split_documents(documents)

# Embed and retrieve text
embeddings = OpenAIEmbeddings()
retriever = Chroma.from_documents(texts, embeddings).as_retriever()
chat = ChatOpenAI(temperature=0, model="gpt-4")

# Prompt template where we provide context
prompt_template = """You are a helpful dicord bot.

{context}

Please provide the most suitable response for the users question.
Answer:"""

# Prepare prompt template for OpenAI
prompt = PromptTemplate(
    template=prompt_template, input_variables=["context"]
)
system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command()
async def apegpt(ctx, *, question):
    try:
        async with ctx.typing():
            # Get the relevant document
            docs = retriever.get_relevant_documents(query=question)
            formatted_prompt = system_message_prompt.format(context=docs)

            messages = [formatted_prompt, HumanMessage(content=question)]
            result = chat(messages)

            content = result.content

            # Split the content into chunks if it's too long
            if len(content) > 2000:
                for i in range(0, len(content), 2000):
                    await ctx.send(content[i:i+2000])
            else:
                await ctx.send(content)
    except Exception as e:
        print(f"Error occurred: {e}")
        await ctx.send("Sorry, I was unable to process your question.")


# bot.run(os.environ.get("DISCORD_TOKEN"))
