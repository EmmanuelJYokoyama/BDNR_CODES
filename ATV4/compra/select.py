import json
import uuid

def buscar_compras(session):
    rows = list(session.execute("SELECT * FROM mercadolivre.compras"))
    if rows:
        print("\n--- Histórico de Compras ---")
        for c in rows:
            # Exibe o nome; se não houver (registro antigo), exibe o ID
            nome_comprador = getattr(c, 'nomecomprador', c.comprador_id)
            nome_produto = getattr(c, 'nomeproduto', f"ID: {c.produto_id}")
            numid_str = f"Cód. Compra: {c.numid}" if hasattr(c, 'numid') else f"ID: {c.id}"
            
            print(f"{numid_str} | Comprador: {nome_comprador} | Produto: {nome_produto} | Total: {c.preco_total}")
        print("----------------------------\n")
    else:
        print("Nenhuma compra encontrada.")

def buscar_compra_id(session):
    buscar_compras(session)
    numid_str = input("Digite o CÓDIGO da compra que deseja buscar: ").strip()

    try:
        numid = int(numid_str)
        compra = session.execute("SELECT * FROM mercadolivre.compras WHERE numid = %s ALLOW FILTERING", [numid]).one()
        
        if compra:
      
            nome_comprador = getattr(compra, 'nomecomprador', f"ID: {compra.comprador_id}")
            nome_produto = getattr(compra, 'nomeproduto', f"ID: {compra.produto_id}")
            nome_vendedor = getattr(compra, 'nomevendedor', f"ID: {compra.vendedor_id}")

            print("\n--- Detalhes da Compra ---")
            print(f"ID da Compra: {compra.id}")
            if hasattr(compra, 'numid'):
                print(f"Código da Compra: {compra.numid}")
            
            print(f"\n--- Comprador ---")
            print(f"Nome: {nome_comprador}")
            
            print(f"\n--- Produto ---")
            print(f"Nome: {nome_produto}")
            if hasattr(compra, 'codigoproduto'):
                print(f"Código do Produto: {compra.codigoproduto}")
            
            print(f"\n--- Vendedor ---")
            print(f"Nome: {nome_vendedor}")

            print(f"\n--- Detalhes do Pedido ---")
            print(f"Quantidade: {compra.quantidade}")
            print(f"Preço total: R$ {compra.preco_total}")
            print(f"Data: {compra.data_compra}\n")
        else:
            print("Compra não encontrada.")
            
    except ValueError:
        print("Código de compra inválido. Por favor, insira um número.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")