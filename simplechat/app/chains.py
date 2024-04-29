#!/usr/bin/env python
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from langchain_core.prompts.chat import ChatPromptTemplate
# from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
# from langserve import add_routes
from .loggers import get_custom_logger

logger = get_custom_logger(__file__)

from .settings import Settings
settings = Settings()



class ChainsHolder:
    def __init__(self):
        # OpenAIモデルの指定
        self.openai_model = ChatOpenAI(api_key=settings.openai_api_key, model="gpt-3.5-turbo-0125")
        self.gemini_model = ChatGoogleGenerativeAI(google_api_key=settings.google_api_key,model="gemini-pro")

    def drag_girlchat(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "あなたはオタクに優しいギャルです。語尾には必ず「ね」をつけて話します。"),
                ("human", "{human_input}"),
            ]
        )

        return prompt | self.openai_model

