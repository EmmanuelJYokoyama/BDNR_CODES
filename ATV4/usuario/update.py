from usuario.select import buscar_usuarios
import uuid

def atualizar_usuario(session):
    buscar_usuarios(session)
    id_usuario_str = input(str("Digite o id do usuario que deseja atualizar: "))
    
    try:
        id_usuario = uuid.UUID(id_usuario_str)
        if not session.execute("SELECT id FROM usuarios.usuarios WHERE id = %s", [id_usuario]).one():
            print("\nUsuario não encontrado.\n")
            return

        nome = input(str("Digite o novo nome: "))
        email = input(str("Digite o novo email: "))
        cpf = input(str("Digite o novo cpf: "))
        rg = input(str("Digite o novo rg: "))
        data_nascimento = input(str("Digite a nova data de nascimento: "))
        telefone = input(str("Digite o novo telefone: "))
        endereco = input(str("Digite o novo endereço: "))
        
        query = """
            UPDATE usuarios.usuarios 
            SET nome=%s, email=%s, cpf=%s, rg=%s, data_nascimento=%s, telefone=%s, endereco=%s 
            WHERE id=%s
        """
        session.execute(query, (nome, email, cpf, rg, data_nascimento, telefone, endereco, id_usuario))
        print("\nUsuário atualizado com sucesso.\n")

    except (ValueError, TypeError):
        print("ID de usuário inválido.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")