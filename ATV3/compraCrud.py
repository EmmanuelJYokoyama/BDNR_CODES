from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import redis

uri = "mongodb+srv://admin:admin@cluster0.2ixrw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.mercado_livre

# Conexão local para uso isolado (o menu passa 'r' para create_compra)
r_local = redis.Redis(
    host='redis-15823.crce216.sa-east-1-2.ec2.redns.redis-cloud.com',
    port=15823,
    decode_responses=True,
    username="admin",
    password="Admin1!admin",
)

def delete_compra(nome, sobrenome):
    mycol = db.compras
    myquery = {"usuario.usu_nome": nome, "usuario.usu_sobrenome": sobrenome}
    mydoc = mycol.delete_one(myquery)
    print("Deletado o usuário ", mydoc)

def create_compra(db, r=None):
    # se não veio conexão do menu, usa local
    r = r or r_local

    compras_col = db.compras
    usuarios_col = db.usuario
    produtos_col = db.produto

    print("\nInserindo uma nova compra")
    cpf = input("Digite seu CPF: ").strip()
    usuario = usuarios_col.find_one({"usu_cpf": cpf})
    if not usuario:
        print("CPF não cadastrado como usuário.")
        return

    while True:
        dataCompra = input("Data da compra (DD-MM-YYYY): ").strip()
        try:
            data_compra_dt = datetime.strptime(dataCompra, "%d-%m-%Y")
            break
        except ValueError:
            print("Data de compra inválida. Use o formato DD-MM-YYYY.")

    dataEntrega = None
    raw = input("Data da entrega (DD-MM-YYYY, vazio se não entregue): ").strip()
    if raw:
        try:
            data_entrega_dt = datetime.strptime(raw, "%d-%m-%Y")
            if data_entrega_dt < data_compra_dt:
                print("Data de entrega não pode ser antes da data de compra.")
                return
            dataEntrega = raw
        except ValueError:
            print("Data de entrega inválida. Use o formato DD-MM-YYYY.")
            return

    valor_total = 0.0
    itens = []
    add = 'S'
    while add == 'S':
        cod_input = input("Código do produto (prod_cod): ").strip()
        try:
            cod = int(cod_input)
        except ValueError:
            print("Código inválido.")
            continue

        produto = produtos_col.find_one({"prod_cod": cod})
        if not produto:
            print("Produto não encontrado.")
            continue

        print(f"Produto: {produto['prod_nome']} | Valor: {produto['prod_valor']} | Estoque: {produto['prod_quantidade']}")
        try:
            qtd = int(input("Quantidade: ").strip())
        except ValueError:
            print("Quantidade inválida.")
            continue
        if qtd <= 0:
            print("Quantidade deve ser > 0.")
            continue

        upd = produtos_col.update_one(
            {"prod_cod": cod, "prod_quantidade": {"$gte": qtd}},
            {"$inc": {"prod_quantidade": -qtd}}
        )
        if upd.modified_count == 0:
            print("Estoque insuficiente no momento.")
            continue

        # lê do Mongo o novo estoque e reflete no Redis
        novo_doc = produtos_col.find_one({"prod_cod": cod}, {"prod_quantidade": 1})
        if novo_doc:
            r.hset(f"produto:{cod}", mapping={"prod_quantidade": int(novo_doc["prod_quantidade"])})

        itens.append({
            "prod_cod": produto["prod_cod"],
            "prod_nome": produto["prod_nome"],
            "prod_valor": produto["prod_valor"],
            "prod_quantidade": qtd
        })
        valor_total += produto["prod_valor"] * qtd
        add = input("Adicionar outro produto? (S/N): ").upper()

    if not itens:
        print("Compra vazia. Cancelada.")
        return

    compra_doc = {
        "comp_valor": round(valor_total, 2),
        "comp_data": dataCompra,
        "comp_dataentrega": dataEntrega,
        "usuario": {
            "usu_cpf": usuario.get("usu_cpf"),
            "usu_nome": usuario.get("usu_nome"),
            "usu_email": usuario.get("usu_email")
        },
        "produtos": itens
    }
    x = compras_col.insert_one(compra_doc)
    print("Compra registrada com ID", x.inserted_id)

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