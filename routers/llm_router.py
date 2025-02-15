from fastapi import APIRouter
from models import database, historias
from sqlalchemy import insert
from utils import obter_logger_e_configuracao, executar_prompt
# import json

logger = obter_logger_e_configuracao()

router = APIRouter()


@router.post(
    "/v1/gerar_historia",
    summary="* * * GERADOR DE HISTÓRIAS * * *",
    description="Gera duas histórias em português brasileiro sobre um tema específico usando  a API Groq e a API da OpenAI.",
)
async def gerar_historia(tema: str):
    logger.info(f"Tema informado: {tema}")

    response = executar_prompt(tema)    

#gravando no banco
    query = insert(historias).values(
        prompt=tema,
        groq=response.get("GROQ"),
    )

    # Executando a inserção assíncrona
    await database.execute(query)

    return response


@router.post(
    "/v2/gerar_historia",
    summary="* * * GERADOR DE HISTÓRIAS * * *",
    description="Gera duas histórias em português brasileiro sobre um tema específico usando  a API Groq e a API da OpenAI.",
)
async def gerar_historia2(tema: str):
    logger.info(f"Tema informado: {tema}")

    response = executar_prompt(tema)    

#gravando no banco
    query = insert(historias).values(
        prompt=tema,
        groq=response.get("GROQ"),
        openai=response.get("OPENAI"),
    )

    # Executando a inserção assíncrona
    await database.execute(query)

    return response