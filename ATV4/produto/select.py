import json
import uuid

def buscar_produtos(session):
    # Corrected to use the 'mercadolivre' keyspace and select existing columns
    produtos = session.execute("SELECT id, nome, preco, estoque, vendedor_id FROM mercadolivre.produtos")
    rows = list(produtos)

    if rows:
        print("\n--- Listagem dos produtos ---")
        for produto in rows:
            print(f"| ID: {produto.id}")
            print(f"| Nome: {produto.nome}")
            print(f"| Preço: {produto.preco}")
            print(f"| Estoque: {produto.estoque}")
            print(f"| Vendedor ID: {produto.vendedor_id}")
            print("-" * 20)
    else:
        print("Nenhum produto encontrado...")

def buscar_produto_id(session):
    buscar_produtos(session)
    id_produto_str = input(str("Digite o id do produto: "))
    
    try:
        # Convert string to UUID object
        id_produto = uuid.UUID(id_produto_str)
        # Use parameterized query
        rows = session.execute("SELECT * FROM mercadolivre.produtos WHERE id = %s", [id_produto])
        produto = rows.one()
        if produto:
            print('\n--- Detalhes do Produto ---')
            print(f'| id: {produto.id}')
            print(f'| nome: {produto.nome}')
            print(f'| descricao: {produto.descricao}')
            print(f'| preco: {produto.preco}')
            print(f'| estoque: {produto.estoque}')
            print(f'| vendedor_id: {produto.vendedor_id}\n')
        else:
            print("Produto não encontrado.")
    except (ValueError, TypeError):
        print("ID de produto inválido.")