from compra.select import buscar_compras
import uuid

def excluir_compra(session):
    buscar_compras(session)
    id_compra_str = input(str('Digite o id da compra que deseja excluir: '))
    
    try:
        id_compra = uuid.UUID(id_compra_str)
        session.execute("DELETE FROM mercadolivre.compras WHERE id = %s", [id_compra])
        print(f'\nCompra de id {id_compra} excluída com sucesso.\n')
    except ValueError:
        print("ID de compra inválido.")
