from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from usuarioCrud import *
from vendedorCrud import *
from produtoCrud import *
from compraCrud import *
from favoritosCrud import * 

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))
db = client.mercado_livre

key = 0
sub = 0
while (key != 'S'):
    print("\n\tMenu Principal")
    print("1-CRUD Usuário")
    print("2-CRUD Vendedor")
    print("3-CRUD Produto")
    print("4-CRUD Compra")
    print("5-CRUD Favorito") 
    key = input("Digite a opção desejada? (S para sair) ").upper()

    if (key == '1'):
        print("\n\tMenu do Usuário")
        print("1-Create Usuário")
        print("2-Read Usuário")
        print("3-Update Usuário")
        print("4-Delete Usuário")
        sub = input("Digite a opção desejada? (V para voltar) ").upper()
        if (sub == '1'):
            print("Create usuario")
            create_usuario()
        elif (sub == '2'):
            nome = input("Read usuário, digite seu cpf para consulta: ")
            read_usuario(nome)
        elif (sub == '3'):
            nome = input("Update usuário, digite o cpf do usuário a ser atualizado: ")
            update_usuario(nome)
        elif (sub == '4'):
            print("Delete usuario")
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
            print("Create Vendedor")
            create_vendedor()
        elif (sub == '2'):
            cnpj = input("Read Vendedor, deseja algum CNPJ especifico? ")
            read_vendedor(cnpj)
        elif (sub == '3'):
            cnpj = input("Update vendedor, deseja algum CNPJ especifico? ")
            update_vendedor(cnpj)
        elif (sub == '4'):
            print("delete vendedor")
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
            print("Create produto")
            create_produto()
        elif (sub == '2'):
            nome = input("Read produto, deseja algum codigo especifico? ")
            read_produto(nome)
        elif (sub == '3'):
            nome = int(input("Update produto, deseja algum ID especifico? "))
            update_produto(nome)
        elif (sub == '4'):
            print("Deletar produto")
            nome = input("Id do produto a ser deletado: ")
            delete_produto(nome)

    elif (key == '4'):
        print("\n\tMenu de Compra")
        print("1-Create Compra")
        print("2-Read Compra")
        print("3-Update Compra")
        print("4-Delete Compra")
        sub = input("Digite a opção desejada? (V para voltar) ").upper()
        if (sub == '1'):
            print("Create compra")
            create_compra()
        elif (sub == '2'):
            nome = input("Read compra, deseja algum CPF especifico? ")
            read_compra(nome)
        elif (sub == '3'):
            nome = input("Update compra, deseja algum CPF especifico? ")
            update_compra(nome)
        elif (sub == '4'):
            print("delete compra")
            nome = input("CPF da compra a ser deletada: ")
            delete_compra(nome)

    elif (key == '5'):
        print("\n\tMenu de Favorito")
        print("1-Create Favorito")
        print("2-Read Favorito")
        print("3-Delete Favorito")
        sub = input("Digite a opção desejada? (V para voltar) ").upper()
        if (sub == '1'):
            print("Create favorito")
            create_favorito()
        elif (sub == '2'):
            cpf = input("Read favorito, digite seu cpf para consulta: ")
            read_favoritos(cpf)
        elif (sub == '3'):
            print("Delete favorito")
            codigo = input("Codigo do favorito a ser deletado: ")
            delete_favorito(codigo)

print("ATÉ LOGO!")