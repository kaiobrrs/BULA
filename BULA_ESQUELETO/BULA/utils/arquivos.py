from pathlib import Path

PASTA_DATABASE = Path("database")


def preparar_arquivos():
    PASTA_DATABASE.mkdir(exist_ok=True)
    for nome in ("usuarios.txt", "medicamentos.txt", "horarios.txt"):
        (PASTA_DATABASE / nome).touch(exist_ok=True)


def ler_registros(caminho):
    """Lê os registros de usuários do arquivo TXT."""
    registros = []
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(";")
                if len(partes) == 6:
                    registros.append({
                        "id": partes[0], "nome": partes[1],
                        "telefone": partes[2], "email": partes[3],
                        "senha_hash": partes[4], "perfil": partes[5]
                    })
    except FileNotFoundError:
        pass
    return registros


def salvar_registro(caminho, registro):
    """Salva um registro de usuário no arquivo TXT."""
    campos = [registro[chave] for chave in
              ("id", "nome", "telefone", "email", "senha_hash", "perfil")]
    with open(caminho, "a", encoding="utf-8") as arquivo:
        arquivo.write(";".join(str(campo) for campo in campos) + "\n")
