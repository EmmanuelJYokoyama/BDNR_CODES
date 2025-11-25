from vendedor.select import buscar_vendedores
import uuid

def excluir_vendedor(session):
    buscar_vendedores(session)
    cnpj_vendedor = input(str('Digite o cnpj do vendedor que deseja excluir: '))
    
    try:
        row = session.execute("SELECT id FROM vendedor.vendedores WHERE cnpj = %s ALLOW FILTERING", [cnpj_vendedor]).one()
        if not row:
            print("\nVendedor não encontrado.\n")
            return
        id_vendedor = row.id
        session.execute("DELETE FROM vendedor.vendedores WHERE id = %s", [id_vendedor])
        print(f'\nVendedor de id {id_vendedor} excluído com sucesso.\n')
    except (ValueError, TypeError):
        print("ID de vendedor inválido.")