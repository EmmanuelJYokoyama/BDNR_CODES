import uuid


def buscar_vendedores(session):
    rows = session.execute("SELECT * FROM vendedor.vendedores")
    print("\n--- Lista de Vendedores ---")
    for row in rows:
        print(f"ID: {row.id} | Nome: {row.nome}")
    print("---------------------------\n")


def buscar_vendedor_cnpj(session):
    cnpj_vendedor = input(str("Digite o CNPJ do vendedor para a busca: "))
    
    # The query must include ALLOW FILTERING because 'cnpj' is not a primary key.
    query = "SELECT * FROM vendedor.vendedores WHERE cnpj = %s ALLOW FILTERING"
    
    vendedor = session.execute(query, [cnpj_vendedor]).one()

    if vendedor:
        print('\n--- Detalhes do Vendedor Encontrado ---')
        print(f'| id: {vendedor.id}')
        print(f'| nome: {vendedor.nome}')
        print(f'| email: {vendedor.email}')
        print(f'| cnpj: {vendedor.cnpj}')
        print(f'| telefone: {vendedor.telefone}')
        print(f'| endereco: {vendedor.endereco}\n')
    else:
        print("\nVendedor com o CNPJ fornecido não foi encontrado.\n")