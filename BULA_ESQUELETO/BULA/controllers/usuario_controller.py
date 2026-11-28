from getpass import getpass
from models.usuario_model import criar_usuario
from utils.arquivos import ler_registros, salvar_registro
from utils.validacoes import validar_email, validar_nome, validar_telefone, validar_senha
from hashlib import sha256

ARQUIVO = "database/usuarios.txt"


def gerar_id(registros):
    maior = 0
    for registro in registros:
        try:
            maior = max(maior, int(registro["id"]))
        except (KeyError, ValueError):
            pass
    return str(maior + 1)


def cadastrar_usuario():
    print("\n--- CADASTRO DE USUÁRIO ---")
    nome = input("Nome completo: ").strip()
    while not validar_nome(nome):
        print("Informe um nome válido.")
        nome = input("Nome completo: ").strip()

    telefone = input("Telefone: ").strip()
    while not validar_telefone(telefone):
        print("Telefone inválido. Informe DDD e número.")
        telefone = input("Telefone: ").strip()

    email = input("E-mail: ").strip().lower()
    while not validar_email(email):
        print("E-mail inválido.")
        email = input("E-mail: ").strip().lower()

    registros = ler_registros(ARQUIVO)
    while any(r["email"] == email for r in registros):
        print("Já existe um cadastro com esse e-mail.")
        email = input("Informe outro e-mail: ").strip().lower()
        while not validar_email(email):
            email = input("E-mail inválido. Digite novamente: ").strip().lower()

    print("\nPerfil de utilização:")
    print("1 - Vou gerenciar meus próprios medicamentos")
    print("2 - Vou gerenciar medicamentos de outra pessoa")
    print("3 - Posso fazer as duas coisas")
    perfil = input("Escolha: ").strip()
    while perfil not in ("1", "2", "3"):
        perfil = input("Digite 1, 2 ou 3: ").strip()
    perfil = {"1": "proprio", "2": "cuidador", "3": "ambos"}[perfil]

    senha = getpass("Crie uma senha (mínimo 6 caracteres): ")
    while not validar_senha(senha):
        print("A senha precisa ter pelo menos 6 caracteres.")
        senha = getpass("Crie uma senha: ")
    confirmar = getpass("Confirme a senha: ")
    while senha != confirmar:
        print("As senhas não coincidem.")
        senha = getpass("Digite a senha novamente: ")
        confirmar = getpass("Confirme a senha: ")

    usuario = criar_usuario(
        gerar_id(registros), nome, telefone, email,
        sha256(senha.encode("utf-8")).hexdigest(), perfil
    )
    salvar_registro(ARQUIVO, usuario)
    print(f"Cadastro realizado! Seu identificador é {usuario['id']}.")


def autenticar_usuario():
    print("\n--- ENTRAR ---")
    email = input("E-mail: ").strip().lower()
    senha = getpass("Senha: ")
    senha_hash = sha256(senha.encode("utf-8")).hexdigest()

    for usuario in ler_registros(ARQUIVO):
        if usuario["email"] == email and usuario["senha_hash"] == senha_hash:
            print(f"Bem-vindo(a), {usuario['nome']}!")
            return usuario

    print("E-mail ou senha incorretos.")
    return None


def listar_usuarios():
    usuarios = ler_registros(ARQUIVO)
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    for usuario in usuarios:
        print(f"ID: {usuario['id']} | Nome: {usuario['nome']} | Perfil: {usuario['perfil']}")
