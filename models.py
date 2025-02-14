from enum import Enum
from pydantic import BaseModel

from sqlalchemy import Table, Column, Integer, String, JSON, DateTime, func, MetaData
from sqlalchemy import create_engine, inspect
from databases import Database

DATABASE_URL = "sqlite:///./database.db"

# Conexão e metadados
database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Verificar se a tabela 'historias' já existe
if not inspect(engine).has_table("historias"):
    historias = Table(
        "historias",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("data_criacao", DateTime, server_default=func.now()),
        Column("prompt", String),
        Column("groq", JSON),
        Column("openai", JSON),
    )
    metadata.create_all(engine)

else:
    # Caso a tabela já exista, apenas defina o objeto `historias` sem recriar
    historias = Table("historias", metadata, autoload_with=engine)
    

class NomeGrupo(str, Enum):
    """
    Enumeração que representa os nomes dos grupos.

    Atributos:
        operacoes (str): Retorna o nome do grupo de operações matemáticas simples.
        teste (str): Retorna o nome do grupo de teste.
    """

    operacoes = "Operações matemáticas simples"
    teste = "Teste"


class TipoOperacao(str, Enum):
    """
    Enumeração que representa os tipos de operações matemáticas.

    Atributos:
        soma (str): Representa a operação de soma.
        subtracao (str): Representa a operação de subtração.
        multiplicacao (str): Representa a operação de multiplicação.
        divisao (str): Representa a operação de divisão.
    """

    soma = "soma"
    subtracao = "subtracao"
    multiplicacao = "multiplicacao"
    divisao = "divisao"


class Numero(BaseModel):
    """
    Classe Numero que herda de BaseModel.

    Atributos:
        numero1 (int): Primeiro número inteiro.
        numero2 (int): Segundo número inteiro.
    """

    numero1: int
    numero2: int


class Resultado(BaseModel):
    """
    Classe que representa o resultado de uma operação.

    Atributos:
        resultado (int): O valor do resultado.
    """

    resultado: int
