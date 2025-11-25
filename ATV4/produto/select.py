import json
import uuid

def buscar_produtos(session):
    rows = list(session.execute("SELECT id, nome, codigoproduto, preco, estoque FROM mercadolivre.produtos"))
    if rows:
        print("\n--- Lista de Produtos ---")
        for produto in rows:
            codigo = getattr(produto, 'codigoproduto', None)
            print(f"ID: {produto.id} | Nome: {produto.nome} | Código: {codigo} | Preço: {produto.preco} | Estoque: {produto.estoque}")
        print("-------------------------\n")
    else:
        print("Nenhum produto encontrado.")

def buscar_produto_id(session):
    codigoProduto = input("Digite o codigo do produto: ").strip()
    try:
        produto = session.execute("SELECT * FROM mercadolivre.produtos WHERE codigoproduto = %s", [int(codigoProduto)]).one()
        if produto:
            codigo = getattr(produto, 'codigoproduto', None)
            print('\n--- Detalhes do Produto ---')
            print(f'| ID: {produto.id}')
            print(f'| Nome: {produto.nome}')
            print(f'| Código: {codigo}')
            print(f'| Descrição: {produto.descricao}')
            print(f'| Preço: {produto.preco}')
            print(f'| Estoque: {produto.estoque}')
            print(f'| Vendedor ID: {produto.vendedor_id}\n')
        else:
            print("Produto não encontrado.")
    except (ValueError, TypeError):
        print("ID de produto inválido.")