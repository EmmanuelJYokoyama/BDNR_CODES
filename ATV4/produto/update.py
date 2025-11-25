from produto.select import buscar_produtos
import uuid
from decimal import Decimal

def atualizar_produto(session):
    buscar_produtos(session)
    codigoProduto_str = input("Digite o código do produto que deseja atualizar: ")
    
    try:
        codigoProduto = int(codigoProduto_str)
        if not session.execute("SELECT codigoProduto FROM mercadolivre.produtos WHERE codigoProduto = %s ALLOW FILTERING", [codigoProduto]).one():
            print("\nProduto não encontrado.\n")
            return

        nome = input("Digite o novo nome: ")
        descricao = input("Digite a nova descrição: ")
        preco_str = input("Digite o novo preço: ")
        estoque_str = input("Digite a nova quantidade em estoque: ")

        query = """
            UPDATE mercadolivre.produtos 
            SET nome=%s, descricao=%s, preco=%s, estoque=%s 
            WHERE codigoProduto=%s
        """
        session.execute(query, (nome, descricao, Decimal(preco_str), int(estoque_str), codigoProduto))
        print("\nProduto atualizado com sucesso.\n")

    except (ValueError, TypeError):
        print("ID de produto ou valor numérico inválido.")