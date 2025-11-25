from vendedor.select import buscar_vendedores
import uuid

def atualizar_vendedor(session):
    buscar_vendedores(session)
    id_vendedor_str = input(str("Digite o id do vendedor que deseja atualizar: "))
    try:
        id_vendedor = uuid.UUID(id_vendedor_str)
        if not session.execute("SELECT id FROM vendedor.vendedores WHERE id = %s", [id_vendedor]).one():
            print("\nVendedor não encontrado.\n")
            return
        
        nome = input(str("Digite o novo nome: "))
        email = input(str("Digite o novo email: "))
        cnpj = input(str("Digite o novo CNPJ: "))
        telefone = input(str("Digite o novo telefone: "))
        endereco = input(str("Digite o novo endereço: "))

        query = "UPDATE vendedor.vendedores SET nome=%s, email=%s, cnpj=%s, telefone=%s, endereco=%s WHERE id=%s"
        session.execute(query, (nome, email, cnpj, telefone, endereco, id_vendedor))
        print("\nVendedor atualizado com sucesso.\n")

    except (ValueError, TypeError):
        print("ID de vendedor inválido.")
