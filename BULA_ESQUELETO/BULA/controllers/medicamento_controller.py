from pathlib import Path
from models.medicamento_model import criar_medicamento

ARQUIVO = Path("database/medicamentos.txt")
CAMPOS = ("id", "usuario_id", "nome", "apresentacao", "dose_prescrita")


def carregar_medicamentos():
    medicamentos = []
    if not ARQUIVO.exists():
        return medicamentos
    with ARQUIVO.open("r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(";")
            if len(partes) == 5:
                medicamentos.append({
                    "id": partes[0], "usuario_id": partes[1],
                    "nome": partes[2], "apresentacao": partes[3],
                    "dose_prescrita": partes[4]
                })
    return medicamentos


def salvar_medicamentos(medicamentos):
    """Regrava o arquivo com os registros atuais de medicamentos."""
    ARQUIVO.parent.mkdir(exist_ok=True)
    with ARQUIVO.open("w", encoding="utf-8") as arquivo:
        for medicamento in medicamentos:
            arquivo.write(";".join(str(medicamento[campo]) for campo in CAMPOS) + "\n")


def proximo_id(registros):
    ids = [int(r["id"]) for r in registros if r["id"].isdigit()]
    return str(max(ids, default=0) + 1)


def cadastrar_medicamento(usuario):
    print("\n--- CADASTRO DE MEDICAMENTO ---")
    nome = input("Nome do medicamento: ").strip()
    while not nome:
        print("O nome não pode ficar vazio.")
        nome = input("Nome do medicamento: ").strip()
    apresentacao = input("Apresentação (ex.: comprimido, gotas): ").strip()
    dose = input("Dose conforme a prescrição (ex.: 1 comprimido): ").strip()
    if not apresentacao or not dose:
        print("Apresentação e dose são obrigatórias. Cadastro cancelado.")
        return

    registros = carregar_medicamentos()
    medicamento = criar_medicamento(
        proximo_id(registros), usuario["id"], nome, apresentacao, dose
    )
    registros.append(medicamento)
    salvar_medicamentos(registros)
    print("Medicamento cadastrado com sucesso!")


def listar_medicamentos(usuario):
    medicamentos = [m for m in carregar_medicamentos()
                    if m["usuario_id"] == usuario["id"]]
    print("\n--- MEUS MEDICAMENTOS ---")
    if not medicamentos:
        print("Nenhum medicamento cadastrado.")
        return
    for m in medicamentos:
        print(f"ID: {m['id']} | {m['nome']} | {m['apresentacao']} | Dose: {m['dose_prescrita']}")


def editar_medicamento(usuario):
    medicamentos = carregar_medicamentos()
    meus_medicamentos = [m for m in medicamentos if m["usuario_id"] == usuario["id"]]
    if not meus_medicamentos:
        print("Não há medicamentos para editar.")
        return

    listar_medicamentos(usuario)
    identificador = input("Digite o ID do medicamento que deseja editar: ").strip()
    medicamento = next((m for m in meus_medicamentos if m["id"] == identificador), None)
    if medicamento is None:
        print("Medicamento não encontrado.")
        return

    print("Pressione Enter para manter o valor atual.")
    nome = input(f"Nome [{medicamento['nome']}]: ").strip()
    apresentacao = input(f"Apresentação [{medicamento['apresentacao']}]: ").strip()
    dose = input(f"Dose [{medicamento['dose_prescrita']}]: ").strip()

    medicamento["nome"] = nome or medicamento["nome"]
    medicamento["apresentacao"] = apresentacao or medicamento["apresentacao"]
    medicamento["dose_prescrita"] = dose or medicamento["dose_prescrita"]
    salvar_medicamentos(medicamentos)
    print("Medicamento atualizado com sucesso!")


def excluir_medicamento(usuario):
    medicamentos = carregar_medicamentos()
    meus_medicamentos = [m for m in medicamentos if m["usuario_id"] == usuario["id"]]
    if not meus_medicamentos:
        print("Não há medicamentos para excluir.")
        return

    listar_medicamentos(usuario)
    identificador = input("Digite o ID do medicamento que deseja excluir: ").strip()
    medicamento = next((m for m in meus_medicamentos if m["id"] == identificador), None)
    if medicamento is None:
        print("Medicamento não encontrado.")
        return

    from controllers.horario_controller import carregar_horarios
    horarios_vinculados = [h for h in carregar_horarios()
                           if h["usuario_id"] == usuario["id"]
                           and h["medicamento_id"] == identificador]
    if horarios_vinculados:
        print("Não é possível excluir: existem horários vinculados a este medicamento.")
        print("Exclua primeiro os horários associados e tente novamente.")
        return

    confirmacao = input(f"Confirma a exclusão de {medicamento['nome']}? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Exclusão cancelada.")
        return

    medicamentos = [m for m in medicamentos
                    if not (m["id"] == identificador and m["usuario_id"] == usuario["id"])]
    salvar_medicamentos(medicamentos)
    print("Medicamento excluído com sucesso!")


def menu_medicamentos(usuario):
    while True:
        print("\n--- MEDICAMENTOS ---")
        print("1 - Cadastrar medicamento")
        print("2 - Listar medicamentos")
        print("3 - Editar medicamento")
        print("4 - Excluir medicamento")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            cadastrar_medicamento(usuario)
        elif opcao == "2":
            listar_medicamentos(usuario)
        elif opcao == "3":
            editar_medicamento(usuario)
        elif opcao == "4":
            excluir_medicamento(usuario)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
