from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import redis
from usuarioCrud import *
from vendedorCrud import *
from produtoCrud import *
from compraCrud import *
from sync_utils import sync_mongo_to_redis, sync_redis_to_mongo
from favoritosCrud import *
from login import cadastrar_usuario, login_usuario, verificar_login, logout, renovar_sessao, ttl_restante  # <- TTL via Redis

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

r = redis.Redis(
    host='redis-15823.crce216.sa-east-1-2.ec2.redns.redis-cloud.com',
    port=15823,
    decode_responses=True,
    username="admin",
    password="Admin1!admin",
)

client = MongoClient(uri, server_api=ServerApi('1'))
db = client.mercado_livre

def fluxo_login(db, cache):
    while True:
        print("\nLogin")
        print("1 - Fazer login")
        print("2 - Cadastrar")
        print("0 - Sair")
        op = input("Digite a opção desejada: ").strip()
        if op == '1':
            if login_usuario(db, cache):
                return True
        elif op == '2':
            cadastrar_usuario(db)
        elif op == '0':
            return False
        else:
            print("Opção inválida!")

if not fluxo_login(db, r):
    print("ATÉ LOGO!")
else:
    while True:
        if not verificar_login(r, renew=True):
            if not fluxo_login(db, r):
                print("ATÉ LOGO!")
                break

        print("\n\tMenu Principal")
        print(f"(Sessão: {ttl_restante(r)}s restantes)")
        print("1-CRUD Usuário")
        print("2-CRUD Vendedor")
        print("3-CRUD Produto")
        print("4-CRUD Compra")
        print("5-CRUD Favorito")
        print("6-Sync Mongo -> Redis")
        print("7-Sync Redis -> Mongo")
        print("L-Logout")
        key = input("Digite a opção desejada? (S para sair) ").upper()

        if key == 'S':
            break

        if (key == '1'):
            print("\n\tMenu do Usuário")
            print("1-Create Usuário")
            print("2-Read Usuário")
            print("3-Update Usuário")
            print("4-Delete Usuário")
            sub = input("Digite a opção desejada? (V para voltar) ").upper()
            if (sub == '1'):
                create_usuario()
            elif (sub == '2'):
                cpf = input("Read usuário, digite seu cpf para consulta: ")
                read_usuario(cpf)
            elif (sub == '3'):
                cpf = input("Update usuário, digite o cpf do usuário a ser atualizado: ")
                update_usuario(cpf)
            elif (sub == '4'):
                nome = input("Nome a ser deletado: ")
                sobrenome = input("Sobrenome a ser deletado: ")
                delete_usuario(nome, sobrenome)

        elif (key == '2'):
            print("\n\tMenu do Vendedor")
            print("1-Create Vendedor")
            print("2-Read Vendedor")
            print("3-Update Vendedor")
            print("4-Delete Vendedor")
            sub = input("Digite a opção desejada? (V para voltar) ").upper()
            if (sub == '1'):
                create_vendedor()
            elif (sub == '2'):
                cnpj = input("Read Vendedor, deseja algum CNPJ especifico? ")
                read_vendedor(cnpj)
            elif (sub == '3'):
                cnpj = input("Update vendedor, deseja algum CNPJ especifico? ")
                update_vendedor(cnpj)
            elif (sub == '4'):
                cnpj = input("CNPJ a ser deletado: ")
                delete_vendedor(cnpj)

        elif (key == '3'):
            print("\n\tMenu do Produto")
            print("1-Create Produto")
            print("2-Read Produto")
            print("3-Update Produto")
            print("4-Delete Produto")
            sub = input("Digite a opção desejada? (V para voltar) ").upper()
            if (sub == '1'):
                create_produto()
            elif (sub == '2'):
                cod = input("Read produto, deseja algum codigo especifico? ")
                read_produto(cod if cod else None)
            elif (sub == '3'):
                cod = input("Update produto, informe o código (prod_cod): ")
                update_produto(cod)
            elif (sub == '4'):
                print("Deletar produto")
                cod = input("Código (prod_cod) do produto a ser deletado: ")
                delete_produto(cod)

        elif (key == '4'):
            print("\n\tMenu de Compra")
            print("1-Create Compra")
            print("2-Read Compra")
            print("3-Update Compra")
            print("4-Delete Compra")
            sub = input("Digite a opção desejada? (V para voltar) ").upper()
            if (sub == '1'):
                create_compra(db, r)
            elif (sub == '2'):
                cpf = input("Read compra, deseja algum CPF especifico? ")
                read_compra(cpf)
            elif (sub == '3'):
                cpf = input("Update compra, deseja algum CPF especifico? ")
                update_compra(cpf)
            elif (sub == '4'):
                cpf = input("CPF da compra a ser deletada: ")
                delete_compra(cpf)

        elif (key == '5'):
            print("\n\tMenu de Favorito")
            print("1-Create Favorito")
            print("2-Read Favorito")
            print("3-Delete Favorito")
            sub = input("Digite a opção desejada? (V para voltar) ").upper()
            if (sub == '1'):
                create_favorito()
            elif (sub == '2'):
                cpf = input("Read favorito, digite seu cpf para consulta: ")
                read_favoritos(cpf)
            elif (sub == '3'):
                cpf = input("CPF do usuário: ")
                cod = input("Código do produto (prod_cod): ")
                delete_favorito(cpf, cod)

        elif (key == '6'):
            sync_mongo_to_redis(db, r)

        elif (key == '7'):
            sync_redis_to_mongo(db, r)

        elif key == 'L':
            logout(r)
            if not fluxo_login(db, r):
                print("ATÉ LOGO!")
                break

        renovar_sessao(r)

print("ATÉ LOGO!")