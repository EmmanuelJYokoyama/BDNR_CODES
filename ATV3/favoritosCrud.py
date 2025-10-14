from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import redis

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre

r = redis.Redis(
    host='redis-15823.crce216.sa-east-1-2.ec2.redns.redis-cloud.com',
    port=15823,
    decode_responses=True,
    username="admin",
    password="Admin1!admin",
)

key = 0
sub = 0

def create_favorito():
    col = db.favoritos
    usuarios = db.usuario
    produtos = db.produto

    cpf = input("CPF do usuário: ").strip()
    cod = input("Código do produto (prod_cod): ").strip()
    try:
        cod = int(cod)
    except ValueError:
        print("Código inválido.")
        return

    if not usuarios.find_one({"usu_cpf": cpf}):
        print("Usuário não encontrado.")
        return
    prod = produtos.find_one({"prod_cod": cod})
    if not prod:
        print("Produto não encontrado.")
        return

    col.create_index([("usu_cpf", 1), ("prod_cod", 1)], unique=True)
    try:
        col.insert_one({
            "usu_cpf": cpf,
            "prod_cod": cod,
            "prod_nome": prod["prod_nome"]
        })
        print("Favorito adicionado.")
    except Exception:
        print("Este favorito já existe.")

def read_favoritos(cpf):
    col = db.favoritos
    for fav in col.find({"usu_cpf": cpf}):
        print(fav)

def delete_favorito(cpf, prod_cod):
    col = db.favoritos
    try:
        cod = int(prod_cod)
    except ValueError:
        print("Código inválido.")
        return
    res = col.delete_one({"usu_cpf": cpf, "prod_cod": cod})
    if res.deleted_count:
        print("Favorito removido.")
    else:
        print("Favorito não encontrado.")