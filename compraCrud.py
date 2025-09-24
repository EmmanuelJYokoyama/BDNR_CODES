from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre

key = 0
sub = 0

def delete_compra(nome, sobrenome):
    mycol = db.compras
    myquery = {"usuario.usu_nome": nome, "usuario.usu_sobrenome": sobrenome}
    mydoc = mycol.delete_one(myquery)
    print("Deletado o usuário ",mydoc)

def create_compra():
    compras_col = db.compras    
    usuarios_col = db.usuario
    produtos_col = db.produto
    print("\nInserindo uma nova compra")
    cpf = input("Digite seu CPF: ")
    usuario = usuarios_col.find_one({"usu_cpf": cpf})
    if not usuario:
        print("CPF não cadastrado como usuário.")
        return

    dataCompra = input("Data da compra (DD-MM-YYYY): ")
    try:
        data_compra_dt = datetime.strptime(dataCompra, "%d-%m-%Y")
    except ValueError:
        print("Data de compra inválida. Use o formato DD-MM-YYYY.")
        return

    dataEntrega = input("Data da entrega (DD-MM-YYYY, deixe vazio se não entregue): ")
    if dataEntrega.strip():
        data_entrega_dt = datetime.strptime(dataEntrega, "%d-%m-%Y")
        while data_entrega_dt < data_compra_dt:
            dataEntrega = input("Data de entrega não pode ser antes da data de compra. Insira a data novamente: ")
    else:
        dataEntrega = None

    valor = 0
    prod = []
    key = 'S'
    while key == 'S':
        codigo_str = input("Código do produto: ").strip()
        if not codigo_str:
            print("Código do produto não pode ser vazio.")
            continue
        try:
            produtoCod = int(codigo_str)
        except ValueError:
            print("Código do produto deve ser numérico.")
            continue

        produto = (produtos_col.find_one({"prod_cod": produtoCod})
                   or produtos_col.find_one({"prod_id": produtoCod}))
        if not produto:
            print("Produto não encontrado! Informe um código válido.")
            continue

        print(f"Produto: {produto.get('prod_nome')} - Valor: {produto.get('prod_valor')} - Quantidade disponível: {produto.get('prod_quantidade')}")
        try:
            produtoQuantidade = int(input("Quantidade do produto: "))
        except ValueError:
            print("Quantidade inválida.")
            continue
        if produtoQuantidade <= 0:
            print("Quantidade deve ser maior que zero.")
            continue
        if produtoQuantidade > produto.get('prod_quantidade', 0):
            print("Quantidade solicitada maior que a disponível!")
            continue

        valor += float(produto.get('prod_valor', 0)) * produtoQuantidade
        produtosObj = {
            "prod_id": produto.get("prod_id", produto.get("prod_cod")),
            "prod_nome": produto.get("prod_nome"),
            "prod_valor": produto.get("prod_valor"),
            "prod_quantidade": produtoQuantidade
        }

        filtro_update = {"prod_cod": produto["prod_cod"]} if "prod_cod" in produto else {"prod_id": produto.get("prod_id", produtoCod)}
        nova_quantidade = produto.get('prod_quantidade', 0) - produtoQuantidade
        produtos_col.update_one(filtro_update, {"$set": {"prod_quantidade": nova_quantidade}})

        prod.append(produtosObj)
        key = input("Deseja cadastrar um novo produto (S/N)? ").strip().upper()

    compra_doc = {
        "comp_valor": valor,
        "comp_data": dataCompra,
        "comp_dataentrega": dataEntrega,
        "usuario": {
            "usu_cpf": usuario.get("usu_cpf"),
            "usu_nome": usuario.get("usu_nome"),
            "usu_email": usuario.get("usu_email")
        },
        "produtos": prod
    }
    x = compras_col.insert_one(compra_doc)
    print("Documento inserido com ID ",x.inserted_id)

def read_compra(cpf):
    compras_col = db.compras
    cursor = compras_col.find({"usuario.usu_cpf": cpf}).sort("comp_data")

    encontrou = False
    for i, compra in enumerate(cursor, start=1):
        encontrou = True
        u = compra.get("usuario", {}) or {}
        print(f"\nCompra #{i}")
        print(f"Nome: {u.get('usu_nome', '')}")
        print(f"CPF: {u.get('usu_cpf', '')}")
        print(f"Email: {u.get('usu_email', '')}")
        print(f"Data da compra: {compra.get('comp_data', '')}")
        entrega = compra.get("comp_dataentrega")
        print(f"Data da entrega: {entrega if entrega else '(não entregue)'}")

        total = compra.get("comp_valor", 0)
        print(f"Valor total: R$ {total:.2f}" if isinstance(total, (int, float)) else f"Valor total: {total}")

        itens = compra.get("produtos", [])
        if itens:
            print("Produtos:")
            for p in itens:
                nome = p.get("prod_nome", "")
                qtd = p.get("prod_quantidade", 0)
                val = p.get("prod_valor", 0)
                val_str = f"R$ {val:.2f}" if isinstance(val, (int, float)) else str(val)
                subtotal = val * qtd if isinstance(val, (int, float)) else None
                sub_str = f" | Subtotal: R$ {subtotal:.2f}" if subtotal is not None else ""
                print(f"  - Nome: {nome} | Qtd: {qtd} | Valor: {val_str}{sub_str}")
        else:
            print("Produtos: (nenhum)")
        print("-" * 40)

    if not encontrou:
        print("Nenhuma compra encontrada para esse CPF.")

def update_compra(nome):
    mycol = db.compras
    myquery = {"usuario.usu_nome": nome}
    mydoc = mycol.find_one(myquery)
    print("Dados do usuário: ",mydoc)
    nome = input("Mudar Nome:")
    if len(nome):
        mydoc["usuario"]["usu_nome"] = nome

    email = input("Mudar Email:")
    if len(email):
        mydoc["usuario"]["usu_email"] = email

    newvalues = { "$set": mydoc }
    mycol.update_one(myquery, newvalues)