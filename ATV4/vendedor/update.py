from vendedor.select import buscar_vendedores
import uuid

def atualizar_vendedor(session):
    buscar_vendedores(session)
    cnpj_vendedor = input(str("Digite o cnpj do vendedor que deseja atualizar: "))
    try:
        row = session.execute("SELECT id FROM vendedor.vendedores WHERE cnpj = %s ALLOW FILTERING", [cnpj_vendedor]).one()
        if not row:
            print("\nVendedor não encontrado.\n")
            return
        id_vendedor = row.id

        nome = input(str("Digite o novo nome: "))
        email = input(str("Digite o novo email: "))
        telefone = input(str("Digite o novo telefone: "))
        endereco = input(str("Digite o novo endereço: "))

        query = "UPDATE vendedor.vendedores SET nome=%s, email=%s, telefone=%s, endereco=%s WHERE id=%s"
        session.execute(query, (nome, email, telefone, endereco, id_vendedor))
        print("\nVendedor atualizado com sucesso.\n")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
