def buscar_usuarios(session):
    resultados = session.run("""
    MATCH (u:Usuario)
    OPTIONAL MATCH (u)-[r:COMPROU]->(p:Produto)
    RETURN u, count(r) AS total_compras, 
           collect({codigo: elementId(p), data: r.data_compra}) AS compras
    ORDER BY u.nome
    """)

    print('\nListagem dos usuarios cadastrados no sistema...')

    for r in resultados:
        u = r[0]
        id_parts = u.element_id.split(":")
        compras = [c for c in r["compras"] if c["codigo"] is not None]

        print(f'\nid: {id_parts[-1]}')
        print('nome: {nome}'.format(nome=u._properties['nome']))
        print('email: {email}'.format(email=u._properties['email']))
        print('cpf: {cpf}'.format(cpf=u._properties['cpf']))
        print('rg: {rg}'.format(rg=u._properties['rg']))
        print('data de nascimento: {data_nascimento}'.format(data_nascimento=u._properties['data_nascimento']))
        print('telefone: {telefone}'.format(telefone=u._properties['telefone']))
        print('endereco: {endereco}'.format(endereco=u._properties['endereco']))
        print('realizou compra: {flag}'.format(flag='sim' if r["total_compras"] > 0 else 'não'))

        if compras:
            print('compras:')
            for c in compras:
                print(f'  - produto: {c["codigo"]} | data: {c.get("data", "")}')