from fastapi import APIRouter
from models import database, historias
from sqlalchemy import insert
from utils import obter_logger_e_configuracao, executar_prompt
import json

logger = obter_logger_e_configuracao()

router = APIRouter()


@router.post(
    "/gerar_historia",
    summary="Gera uma história sobre o tema informado por parâmetro",
    description="Gera uma história em português brasileiro sobre um tema específico usando a API Groq.",
)
async def gerar_historia(tema: str):
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
