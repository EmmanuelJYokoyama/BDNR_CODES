from datetime import timedelta
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import redis
import time

# --- Conexão Mongo (padrão do projeto) ---
mongo_uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri, server_api=ServerApi('1'))
db = client.mercado_livre  # use o mesmo DB do resto do projeto

SESSION_KEY = "session:cpf"
SESSION_TTL = 15  # segundos

def exportar_usuarios_mongodb_para_redis(uri, redis_host, redis_port, redis_password, redis_username=None, redis_ssl=False):
    # Usa o 'db' global já conectado
    colecao_usuario_mongo = db.usuario

    # Conectar ao Redis (com username e ssl opcionais)
    cliente_redis = redis.StrictRedis(
        host=redis_host,
        port=redis_port,
        username=redis_username,
        password=redis_password,
        decode_responses=True,
        ssl=redis_ssl,
    )

    # Obter todos os documentos da coleção no MongoDB
    documentos_mongo = colecao_usuario_mongo.find()

    # Iterar e armazenar no Redis usando o CPF como chave
    for documento in documentos_mongo:
        login_usuario = documento.get('login', '')
        id_usuario = str(documento.get('_id', ''))
        nome_usuario = documento.get('nome', '')
        sobrenome_usuario = documento.get('sobrenome', '')
        cpf_usuario = documento.get('cpf', '')
        senha_usuario = documento.get('senha', '')

        chave_redis = f"Usuario:CPF:{cpf_usuario}"
        # hmset é deprecado; use hset com mapping
        cliente_redis.hset(
            chave_redis,
            mapping={
                '_id': id_usuario,
                'nome': nome_usuario,
                'sobrenome': sobrenome_usuario,
                'cpf': cpf_usuario,
                'login': login_usuario,
                'senha': senha_usuario
            }
        )

    cliente_redis.close()
    print("Exportação de usuários concluída com sucesso")

def listar_e_autenticar_usuarios(redis_host, redis_port, redis_password, redis_username=None, redis_ssl=False):
    cliente_redis = redis.StrictRedis(
        host=redis_host,
        port=redis_port,
        username=redis_username,
        password=redis_password,
        decode_responses=True,
        ssl=redis_ssl,
    )

    chaves_usuarios = cliente_redis.keys("Usuario:CPF:*")

    if not chaves_usuarios:
        print("Nenhum usuário cadastrado.")
    else:
        print("Selecione um usuário:")
        for i, chave_usuario in enumerate(chaves_usuarios, start=1):
            dados_usuario = cliente_redis.hgetall(chave_usuario)
            print(f"{i}. Nome: {dados_usuario.get('nome','')} {dados_usuario.get('sobrenome','')}, CPF: {dados_usuario.get('cpf','')}")

        try:
            indice_selecionado = int(input("Digite o número correspondente ao usuário que deseja autenticar: "))
        except ValueError:
            print("Entrada inválida. Digite um número válido.")
            cliente_redis.close()
            return

        if 1 <= indice_selecionado <= len(chaves_usuarios):
            chave_usuario_selecionado = chaves_usuarios[indice_selecionado - 1]
            dados_usuario = cliente_redis.hgetall(chave_usuario_selecionado)

            print(f"\nNome do usuário: {dados_usuario.get('nome','')} {dados_usuario.get('sobrenome','')}")
            print(f"CPF: {dados_usuario.get('cpf','')}")
            
            login_digitado = input("Digite o login: ")
            senha_digitada = input("Digite a senha: ")

            if login_digitado == dados_usuario.get('login') and senha_digitada == dados_usuario.get('senha'):
                print("Autenticação bem-sucedida.")
                # inicia/renova sessão de 15s e retorna ao menu (sem bloquear)
                cpf = dados_usuario.get('cpf')
                if cpf:
                    cliente_redis.set(SESSION_KEY, cpf, ex=SESSION_TTL)
                # opcional: também expirar a chave do usuário, se quiser simular sessão por usuário
                # cliente_redis.expire(chave_usuario_selecionado, SESSION_TTL)
            else:
                print("Login ou senha inválidos.")

    cliente_redis.close()

def verifcaLogin(r, db_ignorado):
    # Se já há sessão, renova e autoriza
    if r.get(SESSION_KEY):
        r.expire(SESSION_KEY, SESSION_TTL)
        return True

    # Sem sessão: abre o fluxo de login
    params = r.connection_pool.connection_kwargs
    listar_e_autenticar_usuarios(
        redis_host=params.get("host"),
        redis_port=params.get("port"),
        redis_password=params.get("password"),
        redis_username=params.get("username"),
        redis_ssl=params.get("ssl", False),
    )

    # Após tentar autenticar, verifica novamente
    if r.get(SESSION_KEY):
        r.expire(SESSION_KEY, SESSION_TTL)
        return True

    return False

def get_usuario_logado(r, db_ignorado):
    cpf = r.get(SESSION_KEY)
    if not cpf:
        return None
    return db.usuario.find_one({"usu_cpf": cpf})

def logout(r):
    r.delete(SESSION_KEY)
    print("Logout efetuado.")