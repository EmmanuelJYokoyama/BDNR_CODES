import uuid

def buscar_usuarios(session):
    usuarios = session.execute('SELECT * FROM usuarios.usuarios')
    rows = list(usuarios)
    if rows:
        print("\n--- Listagem dos usuários ---")
        for usuario in rows:
            print(f"| ID: {usuario.id} | Nome: {usuario.nome}")
        print("-" * 20)
    else:
        print("Nenhum usuário encontrado...")

def buscar_usuario_cpf(session):
    cpf_usuario = input(str("Digite o CPF do usuario para a busca: "))

    query = "SELECT * FROM usuarios.usuarios WHERE cpf = %s ALLOW FILTERING"
    
    usuario = session.execute(query, [cpf_usuario]).one()

    if usuario:
        print('\n--- Detalhes do Usuário ---')
        print(f'| id: {usuario.id}')
        print(f'| nome: {usuario.nome}')
        print(f'| email: {usuario.email}')
        print(f'| cpf: {usuario.cpf}')
        print(f'| rg: {usuario.rg}')
        print(f'| data_nascimento: {usuario.data_nascimento}')
        print(f'| telefone: {usuario.telefone}')
        print(f'| endereco: {usuario.endereco}\n')
    else:
        print("\nUsuário com o CPF fornecido não foi encontrado.\n")
