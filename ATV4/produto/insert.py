from vendedor.select import buscar_vendedores
import uuid
from decimal import Decimal

def inserir_produto(session):
    buscar_vendedores(session)

    cnpj = input("Digite o cnpj do vendedor para este produto: ").strip()
    if not cnpj:
        print("CNPJ inválido.")
        return

    vendedor_row = session.execute("SELECT id FROM vendedor.vendedores WHERE cnpj = %s ALLOW FILTERING", [cnpj]).one()
    if not vendedor_row:
        print("Vendedor não encontrado para o CNPJ informado.")
        return

    id_vendedor = vendedor_row.id

    nome = input("Digite o nome do produto: ").strip()
    descricao = input("Digite a descrição do produto: ").strip()
    preco_str = input("Digite o preço do produto: ").strip()
    estoque_str = input("Digite a quantidade em estoque: ").strip()

    try:
        preco = Decimal(preco_str)
        estoque = int(estoque_str)
    except Exception:
        print("Preço ou estoque inválido.")
        return

    codigo_str = input("Digite o código do produto (número): ").strip()
    try:
        codigo = int(codigo_str)
    except ValueError:
        print("Código inválido.")
        return

    session.execute("""
        INSERT INTO mercadolivre.produtos (id, codigoProduto, nome, descricao, preco, vendedor_id, estoque)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (uuid.uuid1(), codigo, nome, descricao, preco, id_vendedor, estoque))

    print("\nProduto cadastrado com sucesso.")