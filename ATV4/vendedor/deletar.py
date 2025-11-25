from vendedor.select import buscar_vendedores
import uuid

def excluir_vendedor(session):
    buscar_vendedores(session)
    id_vendedor_str = input(str('Digite o id do vendedor que deseja excluir: '))
    
    try:
        id_vendedor = uuid.UUID(id_vendedor_str)
        if session.execute("SELECT id FROM vendedor.vendedores WHERE id = %s", [id_vendedor]).one():
            session.execute("DELETE FROM vendedor.vendedores WHERE id = %s", [id_vendedor])
            print(f'\nVendedor de id {id_vendedor} excluído com sucesso.\n')
        else:
            print("Vendedor não encontrado.")
    except (ValueError, TypeError):
        print("ID de vendedor inválido.")