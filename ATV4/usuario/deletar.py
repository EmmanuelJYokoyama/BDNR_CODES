from usuario.select import buscar_usuarios
import uuid

def excluir_usuario(session):
    buscar_usuarios(session)
    cpf_usuario_str = input(str('Digite o cpf do usuario que deseja excluir: '))
    
    try:
        
        select_query = "SELECT id FROM usuarios.usuarios WHERE cpf = %s ALLOW FILTERING"
        user_to_delete = session.execute(select_query, [cpf_usuario_str]).one()

        if user_to_delete:
            user_id = user_to_delete.id
            delete_query = "DELETE FROM usuarios.usuarios WHERE id = %s"
            session.execute(delete_query, [user_id])
            print(f'\nUsuário de cpf {cpf_usuario_str} excluído com sucesso.\n')
        else:
            print("Usuário com o CPF fornecido não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")