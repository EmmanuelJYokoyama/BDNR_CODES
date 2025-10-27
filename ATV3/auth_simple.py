from typing import Optional

SESSION_KEY = "usuario_logado"
DEFAULT_TTL = 10  # segundos

def cadastrar_usuario(db):
    usuario_col = db.usuario
    email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()
    if not email or not senha:
        print("E-mail e senha são obrigatórios.")
        return
    usuario_col.insert_one({"email": email, "senha": senha})
    print("Usuário registrado com sucesso!")

def login_usuario(db, cache, ttl: int = DEFAULT_TTL) -> bool:
    usuario_col = db.usuario
    email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()
    usuario = usuario_col.find_one({"email": email, "senha": senha})
    if usuario:
        cache.setex(SESSION_KEY, ttl, email)  # cria sessão com TTL
        print("Login realizado com sucesso!")
        return True
    else:
        print("Ocorreu um erro ao realizar login!")
        return False

def verificar_login(cache, renew: bool = True, ttl: int = DEFAULT_TTL) -> bool:
    # -2: não existe (expirada); -1: sem TTL; >=0: segundos restantes
    t = cache.ttl(SESSION_KEY)
    if t == -2:
        print("Sessão expirada! Faça login novamente!")
        return False
    if renew:
        cache.expire(SESSION_KEY, ttl)  # renova o TTL no Redis
    return True

def ttl_restante(cache) -> int:
    t = cache.ttl(SESSION_KEY)
    return 0 if t < 0 else t

def renovar_sessao(cache, ttl: int = DEFAULT_TTL):
    cache.expire(SESSION_KEY, ttl)

def logout(cache):
    cache.delete(SESSION_KEY)
    print("Logout realizado.")