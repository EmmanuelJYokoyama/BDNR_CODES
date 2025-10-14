import json

def sync_mongo_to_redis(db, r):
    # Vendedores
    for v in db.vendedor.find({}):
        r.hset(f"vendedor:{v['ven_cnpj']}", mapping={
            "ven_nome": v.get("ven_nome",""),
            "ven_cnpj": v.get("ven_cnpj",""),
            "ven_email": v.get("ven_email",""),
        })
    # Produtos
    for p in db.produto.find({}):
        vend = p.get("vendedor", {}) or {}
        r.hset(f"produto:{p['prod_cod']}", mapping={
            "prod_cod": p.get("prod_cod"),
            "prod_nome": p.get("prod_nome",""),
            "prod_descricao": p.get("prod_descricao",""),
            "prod_valor": float(p.get("prod_valor",0)),
            "prod_quantidade": int(p.get("prod_quantidade",0)),
            "ven_id": vend.get("ven_id",""),
            "ven_nome": vend.get("ven_nome",""),
            "ven_numero": vend.get("ven_numero",""),
        })
    print("Sincronização Mongo -> Redis concluída.")

def _int_or(s, default=0):
    try:
        return int(s)
    except Exception:
        return default

def _float_or(s, default=0.0):
    try:
        return float(s)
    except Exception:
        return default

def sync_redis_to_mongo(db, r):
    # Vendedores
    for key in r.scan_iter(match="vendedor:*"):
        hv = r.hgetall(key)
        if not hv: 
            continue
        db.vendedor.update_one(
            {"ven_cnpj": hv.get("ven_cnpj")},
            {"$set": {
                "ven_nome": hv.get("ven_nome",""),
                "ven_cnpj": hv.get("ven_cnpj",""),
                "ven_email": hv.get("ven_email",""),
            }},
            upsert=True
        )

    # Produtos
    for key in r.scan_iter(match="produto:*"):
        hp = r.hgetall(key)
        if not hp:
            continue
        doc = {
            "prod_cod": _int_or(hp.get("prod_cod") or key.split(":")[-1]),
            "prod_nome": hp.get("prod_nome",""),
            "prod_descricao": hp.get("prod_descricao",""),
            "prod_valor": _float_or(hp.get("prod_valor", 0)),
            "prod_quantidade": _int_or(hp.get("prod_quantidade", 0)),
            "vendedor": {
                "ven_id": hp.get("ven_id",""),
                "ven_nome": hp.get("ven_nome",""),
                "ven_numero": hp.get("ven_numero",""),
            }
        }
        db.produto.update_one(
            {"prod_cod": doc["prod_cod"]},
            {"$set": doc},
            upsert=True
        )

    print("Sincronização Redis -> Mongo concluída.")