from produto.select import buscar_produtos
import uuid

def excluir_produto(session):
    buscar_produtos(session)
    id_produto_str = input(str('Digite o id do produto que deseja excluir: '))
    
    try:
        id_produto = uuid.UUID(id_produto_str)
        # Check if product exists before deleting
        produto = session.execute("SELECT id FROM mercadolivre.produtos WHERE id = %s", [id_produto]).one()
        if produto:
            session.execute("DELETE FROM mercadolivre.produtos WHERE id = %s", [id_produto])
            print(f'\nProduto de id {id_produto} excluído com sucesso.\n')
        else:
            print("Produto não encontrado.")
    except (ValueError, TypeError):
        print("ID de produto inválido.")