from usuario.select import buscar_usuarios
from produto.select import buscar_produtos
from datetime import datetime
import uuid
from decimal import Decimal

def _next_sequence(session, seq_name: str) -> int:
   
    session.execute("UPDATE mercadolivre.sequences SET value = value + 1 WHERE name = %s", [seq_name])
    row = session.execute("SELECT value FROM mercadolivre.sequences WHERE name = %s", [seq_name]).one()
    return int(getattr(row, 'value', 0))

def inserir_compra(session):
    try:
        print('\n--- Registro de Nova Compra ---')
        
        buscar_usuarios(session)
        cpf_cliente = input('Digite o cpf do comprador (usuário): ').strip()
        if not cpf_cliente:
            print("CPF inválido.")
            return


        comprador_row = session.execute("SELECT id, nome FROM usuarios.usuarios WHERE cpf = %s ALLOW FILTERING", [cpf_cliente]).one()
        if not comprador_row:
            print("Comprador não encontrado para o CPF informado.")
            return
        comprador_id = comprador_row.id
        nome_comprador = comprador_row.nome

        buscar_produtos(session)
        codigo_str = input('Digite o código do produto: ').strip()
        codigo_produto = int(codigo_str)


        produto = session.execute(
            "SELECT id, nome, preco, estoque, vendedor_id FROM mercadolivre.produtos WHERE codigoproduto = %s ALLOW FILTERING",
            [codigo_produto]
        ).one()
        if not produto:
            print("Produto não encontrado.")
            return
        
        produto_id = produto.id
        nome_produto = produto.nome
        vendedor_id = produto.vendedor_id


        vendedor_row = session.execute("SELECT nome FROM vendedor.vendedores WHERE id = %s", [vendedor_id]).one()
        nome_vendedor = vendedor_row.nome if vendedor_row else "N/A"

        print(f"Produto selecionado: {nome_produto} | Estoque disponível: {produto.estoque}")
        quantidade = int(input('Digite a quantidade desejada: '))

        if quantidade <= 0 or quantidade > produto.estoque:
            print("Quantidade inválida ou excede o estoque disponível.")
            return

        preco_total = produto.preco * Decimal(quantidade)
        numid = _next_sequence(session, 'compras')

       
        session.execute("""
            INSERT INTO mercadolivre.compras
                (id, numid, comprador_id, nomeComprador, produto_id, nomeProduto, codigoproduto, vendedor_id, nomeVendedor, quantidade, preco_total, data_compra)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (uuid.uuid1(), numid, comprador_id, nome_comprador, produto_id, nome_produto, codigo_produto, vendedor_id, nome_vendedor, quantidade, preco_total, datetime.now())
        )

        
        novo_estoque = produto.estoque - quantidade
        session.execute("UPDATE mercadolivre.produtos SET estoque = %s WHERE id = %s", (novo_estoque, produto_id))

        print('\nCompra registrada com sucesso. Cód. Compra:', numid)

    except (ValueError, TypeError):
        print("Valor inválido. Por favor, insira números/UUIDs corretos.")
    except Exception as e:
        print(f"Ocorreu um erro ao registrar a compra: {e}")