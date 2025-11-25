import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import uuid

from menus.menu_usuario import menu_usuario
from menus.menu_produto import menu_produto
from menus.menu_vendedor import menu_vendedor
from menus.menu_compra import menu_compra

bundle_path = os.path.join(os.path.dirname(__file__), 'secure-connect-mercadolivrecassandra.zip')

cloud_config = {
    'secure_connect_bundle': bundle_path
}
auth_provider = PlainTextAuthProvider('muwrDkFqmfxlEgwuGRCgPKiO', 'IiaWvnKmZS_uQZ2WkxfZ6n+HrMxmRhANS,P.62dOSGm_GuEj6dE8MhsdOLylhQpdtBL1SueEJgKx7sbTQk4YupaSTDH7CcFFTtkOMsQngOpoprFYtkvMolsOLel60aW3')

cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)

session = cluster.connect()

row = session.execute("select release_version from system.local").one()

if row:
    print("Conexão bem sucedida...")

    # Criar tabelas explicitando keyspace.tabela
    session.execute("""
    CREATE TABLE IF NOT EXISTS usuarios.usuarios (
        id UUID PRIMARY KEY,
        nome TEXT,
        email TEXT,
        cpf TEXT,
        rg TEXT,
        data_nascimento TEXT,
        telefone TEXT,
        endereco TEXT
    );
    """)

    session.execute("""
    CREATE TABLE IF NOT EXISTS vendedor.vendedores (
        id UUID PRIMARY KEY,
        nome TEXT,
        email TEXT,
        cnpj TEXT,
        telefone TEXT,
        endereco TEXT
    );
    """)

    session.execute("""
    CREATE TABLE IF NOT EXISTS mercadolivre.produtos (
        id UUID PRIMARY KEY,
        codigoProduto INT,
        nome TEXT,
        descricao TEXT,
        preco DECIMAL,
        vendedor_id UUID,
        estoque INT
    );
    """)

    session.execute("""
    CREATE TABLE IF NOT EXISTS mercadolivre.compras (
        id UUID PRIMARY KEY,
        numid INT,
        comprador_id UUID,
        produto_id UUID,
        codigoproduto INT,
        vendedor_id UUID,
        quantidade INT,
        preco_total DECIMAL,
        data_compra TIMESTAMP
    );
    """)

    # Adicione este bloco para criar a tabela de sequência
    session.execute("""
    CREATE TABLE IF NOT EXISTS mercadolivre.sequences (
        name TEXT PRIMARY KEY,
        value COUNTER
    );
    """)

    print("Tabelas prontas para uso.")

    execucao = True

    while execucao:

        print('''
Opções:
[1] Menu do usuario
[2] Menu do produto
[3] Menu do vendedor
[4] Menu da compra
[0] sair
        ''')

        opcao = input(str('Escolha uma das opções a cima: '))
        match (int(opcao)):
            case 1:
                menu_usuario(session)
            case 2:
                menu_produto(session)
            case 3:
                menu_vendedor(session)
            case 4:
                menu_compra(session)
            case 0:
                print('Até mais...')
                execucao = False
            case _:
                print("Operação não entendida...")

else:
    print("Ocorreu um erro.")