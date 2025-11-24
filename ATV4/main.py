from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from menus.menu_usuario import menu_usuario
from menus.menu_produto import menu_produto
from menus.menu_vendedor import menu_vendedor
from menus.menu_compra import menu_compra

cloud_config= {
  'secure_connect_bundle': 'secure-connect-mercadolivrecassandra.zip'
}
auth_provider = PlainTextAuthProvider('muwrDkFqmfxlEgwuGRCgPKiO', 'IiaWvnKmZS_uQZ2WkxfZ6n+HrMxmRhANS,P.62dOSGm_GuEj6dE8MhsdOLylhQpdtBL1SueEJgKx7sbTQk4YupaSTDH7CcFFTtkOMsQngOpoprFYtkvMolsOLel60aW3')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('mercadolivreCassandra')

row = session.execute("select release_version from system.local").one()

if row:
    print("Conexão bem sucedida...")
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