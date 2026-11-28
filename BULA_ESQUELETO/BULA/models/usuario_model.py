def criar_usuario(identificador, nome, telefone, email, senha_hash, perfil):
    """Monta e devolve um dicionário com os dados do usuário."""
    return {
        "id": identificador,
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "senha_hash": senha_hash,
        "perfil": perfil,
    }
