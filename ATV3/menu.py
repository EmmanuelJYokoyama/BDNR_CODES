from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import redis
from usuarioCrud import *
from vendedorCrud import *
from produtoCrud import *
from compraCrud import *
from favoritosCrud import *
from login import verifcaLogin, logout
from sync_utils import sync_mongo_to_redis, sync_redis_to_mongo

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

key = 0
while (key != 'S' and verifcaLogin(r, db)):

    print("\n\tMenu Principal")
    print("1-CRUD Usuário")
    print("2-CRUD Vendedor")
    print("3-CRUD Produto")
    print("4-CRUD Compra")
    print("5-CRUD Favorito")
    print("6-Sync Mongo -> Redis") 
    print("7-Sync Redis -> Mongo") 
    print("L-Logout")
    key = input("Digite a opção desejada? (S para sair) ").upper()

    if (key == '1'):
        verifcaLogin(r, db)  # garante sessão antes do submenu
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
        verifcaLogin(r, db)
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
        verifcaLogin(r, db)
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
            cod = int(input("Update produto, informe o código (prod_cod): "))
            update_produto(cod)
        elif (sub == '4'):
            print("Deletar produto")
            cod = input("Código (prod_cod) do produto a ser deletado: ")
            delete_produto(cod)

    elif (key == '4'):
        verifcaLogin(r, db)
        print("\n\tMenu de Compra")
        print("1-Create Compra")
        print("2-Read Compra")
        print("3-Update Compra")
        print("4-Delete Compra")
        sub = input("Digite a opção desejada? (V para voltar) ").upper()
        if (sub == '1'):
            create_compra(db, r)  # <— passa Redis para refletir estoque
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
        verifcaLogin(r, db)
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
        verifcaLogin(r, db)
        sync_mongo_to_redis(db, r)

    elif (key == '7'):
        verifcaLogin(r, db)
        sync_redis_to_mongo(db, r)

    elif key == 'L':
        logout(r)

print("ATÉ LOGO!")