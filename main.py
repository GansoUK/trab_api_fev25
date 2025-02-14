from fastapi import FastAPI, Depends
from utils import commom_verificacao_api_token
from routers import llm_router, operacoes_router


description = """
    Trabalho da disciplina de API da Pós-graduação em Sistemas e Agentes Inteligentes
    Prof. Rogério Rodrigues
    
    - /llm1: retorna uma resposta do Groq
    - /llm2: retorna uma resposta da OpenAI
    - /llm3: recebe as resposta de llm1 e llm2, mescla as respostas e gera uma nova
"""


app = FastAPI(
    title="API para IA",
    description=description,
    version="1.0",
    terms_of_service="https://en.wikipedia.org/wiki/WTFPL",
    contact={
        "name": "Diego Oliveira e Jorge Ferla",
        "url": "http://github.com/GansoUK/",
        "email": "jfxxi@hotmail.com",
    },
    license_info={
        "name": "Do What The F*ck You Want To Public License",
        "url": "https://github.com/geeksam/wtf/blob/master/LICENSE",
    },
    dependencies=[Depends(commom_verificacao_api_token)],
)


app.include_router(llm_router.router, prefix="/llm")
app.include_router(operacoes_router.router, prefix="/operacoes")
