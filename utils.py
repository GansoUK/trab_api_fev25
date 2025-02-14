import json
import logging
from fastapi import HTTPException
from groq import Groq
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# LIMPAR
# API_TOKEN = int(os.getenv("API_TOKEN"))
API_TOKEN = "123"


def obter_logger_e_configuracao():
    """
    Configura o logger padrão para o nível de informação e formato especificado.

    Retorna:
        logging.Logger: Um objeto de logger com as configurações padrões.
    """
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
    )
    logger = logging.getLogger("fastapi")
    return logger

''' LIMPAR
def commom_verificacao_api_token(api_token: int):
    """
    Verifica se o token da API fornecido é válido.

    Args:
        api_token (int): O token da API a ser verificado.

    Raises:
        HTTPException: Se o token da API for inválido, uma exceção HTTP 401 é levantada com a mensagem "Token inválido".
    """
    if api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
'''

import json
def executar_prompt(tema: str):
    """
    Gera uma história em português brasileiro sobre um tema específico usando a API Groq ou OpenAI.
    Args:
        tema (str): O tema sobre o qual a história será escrita.
    Returns:
        dict: Dicionário contendo a história gerada e o uso de tokens para cada serviço disponível.
    """
    prompt = f"Escreva uma história em pt-br sobre {tema}"

    resultados = {}

    # Executar via Groq
    if os.getenv("GROQ_API_KEY"):
        client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response_groq = client_groq.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=os.getenv("GROQ_MODEL", "mixtral-8x7b-32768"),
        )

        resultados["GROQ"] = {
            "historia": response_groq.choices[0].message.content,
            "custo": response_groq.usage.__dict__
        }

    # Executar via OpenAI
    if os.getenv("OPENAI_API_KEY"):
        client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response_openai = client_openai.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        )


        # Usando pop com valor padrão para evitar KeyError
        response_openai.usage.__dict__.pop("completion_tokens_details", None)
        response_openai.usage.__dict__.pop("prompt_tokens_details", None)

        resultados["OPENAI"] = {
            "historia": response_openai.choices[0].message.content,
            "custo": response_openai.usage.__dict__
        }

    return resultados
