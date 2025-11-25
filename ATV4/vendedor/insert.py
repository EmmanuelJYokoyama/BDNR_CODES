from datetime import date
import uuid

def insert_vendedor(session):
    print("\n--- Cadastro de Novo Vendedor ---")

    nome = input(str("Digite o nome do vendedor: "))
    email = input(str('Digite o endereço de email: '))
    cnpj = input(str("Digite o cnpj: "))
    telefone = input(str('Digite o numero do telefone: '))
    endereco = input(str('Digite o endereço: '))

    session.execute("""
        INSERT INTO vendedor.vendedores
            (id, nome, email, cnpj, telefone, endereco)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (uuid.uuid1(), nome, email, cnpj, telefone, endereco))

    print("\nVendedor cadastrado com sucesso.\n")