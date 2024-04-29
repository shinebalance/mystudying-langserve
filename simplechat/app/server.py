#!/usr/bin/env python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from langchain_core.prompts.chat import ChatPromptTemplate
# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_openai import ChatOpenAI
from langserve import add_routes
from .loggers import get_custom_logger

logger = get_custom_logger(__file__)

# from .settings import Settings
# settings = Settings()

from .chains import ChainsHolder


def create_app() -> FastAPI:
    logger.info("Creating FastAPI app")

    application = FastAPI(
        title="LangChain Server",
        version="1.0",
        description="A simple api server using Langchain's Runnable interfaces",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # chainsからchain関係の処理を取得
    chains_holder = ChainsHolder()

    logger.info("チェーン処理読み込み")
    # OpenAIモデル
    add_routes(
        application,
        chains_holder.openai_model,
        path="/openai",
    )
    # ユーザー定義のチェーン
    add_routes(
        application,
        chains_holder.drag_girlchat(),
        path="/joke",
    )

    return application


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)