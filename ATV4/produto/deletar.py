from produto.select import buscar_produtos
import uuid

def excluir_produto(session):
    buscar_produtos(session)
    codigoProduto_str = input('Digite o codigo do produto que deseja excluir: ')
    
    try:
        codigoProduto = int(codigoProduto_str)
        if session.execute("SELECT codigoProduto FROM mercadolivre.produtos WHERE codigoProduto = %s ALLOW FILTERING", [codigoProduto]).one():
            session.execute("DELETE FROM mercadolivre.produtos WHERE codigoProduto = %s", [codigoProduto])
            print(f'\nProduto de codigo {codigoProduto} excluído com sucesso.\n')
        else:
            print("Produto não encontrado.")
    except (ValueError, TypeError):
        print("ID de produto inválido.")