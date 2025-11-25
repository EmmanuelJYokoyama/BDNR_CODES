from usuario.select import buscar_usuarios
import uuid

def atualizar_usuario(session):
    buscar_usuarios(session)
    cpf_usuario = input(str("Digite o CPF do usuario que deseja atualizar: "))
    
    try:
        if not session.execute("SELECT cpf FROM usuarios.usuarios WHERE cpf = %s ALLOW FILTERING", [cpf_usuario]).one():
            print("\nUsuario não encontrado.\n")
            return

        nome = input(str("Digite o novo nome: "))
        email = input(str("Digite o novo email: "))
        rg = input(str("Digite o novo rg: "))
        data_nascimento = input(str("Digite a nova data de nascimento: "))
        telefone = input(str("Digite o novo telefone: "))
        endereco = input(str("Digite o novo endereço: "))
        
        query = """
            UPDATE usuarios.usuarios 
            SET nome=%s, email=%s, rg=%s, data_nascimento=%s, telefone=%s, endereco=%s 
            WHERE cpf=%s ALLOW FILTERING
        """
        session.execute(query, (nome, email, rg, data_nascimento, telefone, endereco, cpf_usuario))
        print("\nUsuário atualizado com sucesso.\n")

    except (ValueError, TypeError):
        print("ID de usuário inválido.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")