from produto.select import buscar_produtos
import uuid
from decimal import Decimal

def atualizar_produto(session):
    buscar_produtos(session)
    id_produto_str = input(str("Digite o id do produto que deseja atualizar: "))
    
    try:
        id_produto = uuid.UUID(id_produto_str)
        if not session.execute("SELECT id FROM mercadolivre.produtos WHERE id = %s", [id_produto]).one():
            print("\nProduto não encontrado.\n")
            return

        nome = input(str("Digite o novo nome: "))
        descricao = input(str("Digite a nova descrição: "))
        preco_str = input(str("Digite o novo preço: "))
        estoque_str = input(str("Digite a nova quantidade em estoque: "))

        query = """
            UPDATE mercadolivre.produtos 
            SET nome=%s, descricao=%s, preco=%s, estoque=%s 
            WHERE id=%s
        """
        session.execute(query, (nome, descricao, Decimal(preco_str), int(estoque_str), id_produto))
        print("\nProduto atualizado com sucesso.\n")

    except (ValueError, TypeError):
        print("ID de produto ou valor numérico inválido.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")