from compra.select import buscar_compras
import uuid

def excluir_compra(session):
    buscar_compras(session)
    numCompra_str = input('Digite o CÓDIGO da compra que deseja excluir: ').strip()
    
    try:
        numCompra = int(numCompra_str)
        
        compra_para_excluir = session.execute(
            "SELECT id FROM mercadolivre.compras WHERE numid = %s ALLOW FILTERING", [numCompra]
        ).one()

        if compra_para_excluir:
            id_da_compra = compra_para_excluir.id
            session.execute("DELETE FROM mercadolivre.compras WHERE id = %s", [id_da_compra])
            print(f'\nCompra de código {numCompra} excluída com sucesso.\n')
        else:
            print("Compra não encontrada.")
            
    except ValueError:
        print("Código de compra inválido. Por favor, insira um número.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
