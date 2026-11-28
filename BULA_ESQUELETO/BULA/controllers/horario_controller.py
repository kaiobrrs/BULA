from pathlib import Path
from datetime import date
from models.horario_model import criar_horario
from utils.validacoes import validar_hora
from controllers.medicamento_controller import carregar_medicamentos

ARQUIVO = Path("database/horarios.txt")
CAMPOS = ("id", "usuario_id", "medicamento_id", "hora", "data_inicio", "data_fim")


def carregar_horarios():
    horarios = []
    if not ARQUIVO.exists():
        return horarios
    with ARQUIVO.open("r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(";")
            if len(partes) == 6:
                horarios.append({
                    "id": partes[0], "usuario_id": partes[1],
                    "medicamento_id": partes[2], "hora": partes[3],
                    "data_inicio": partes[4], "data_fim": partes[5]
                })
    return horarios


def salvar_horarios(horarios):
    """Regrava o arquivo com os registros atuais de horários."""
    ARQUIVO.parent.mkdir(exist_ok=True)
    with ARQUIVO.open("w", encoding="utf-8") as arquivo:
        for horario in horarios:
            arquivo.write(";".join(str(horario[campo]) for campo in CAMPOS) + "\n")


def proximo_id(registros):
    ids = [int(r["id"]) for r in registros if r["id"].isdigit()]
    return str(max(ids, default=0) + 1)


def _meus_horarios(usuario):
    return [h for h in carregar_horarios() if h["usuario_id"] == usuario["id"]]


def _meus_medicamentos(usuario):
    return [m for m in carregar_medicamentos() if m["usuario_id"] == usuario["id"]]


def cadastrar_horario(usuario):
    medicamentos = _meus_medicamentos(usuario)
    if not medicamentos:
        print("Cadastre um medicamento antes de adicionar um horário.")
        return
    print("\n--- MEDICAMENTOS CADASTRADOS ---")
    for m in medicamentos:
        print(f"{m['id']} - {m['nome']} ({m['apresentacao']})")
    medicamento_id = input("ID do medicamento: ").strip()
    if not any(m["id"] == medicamento_id for m in medicamentos):
        print("Medicamento não encontrado para este usuário.")
        return

    hora = input("Horário (HH:MM): ").strip()
    while not validar_hora(hora):
        print("Horário inválido. Use o formato HH:MM.")
        hora = input("Horário (HH:MM): ").strip()

    hoje = date.today().isoformat()
    data_inicio = input(f"Data de início (AAAA-MM-DD) [padrão {hoje}]: ").strip() or hoje
    try:
        date.fromisoformat(data_inicio)
    except ValueError:
        print("Data de início inválida. Cadastro cancelado.")
        return

    data_fim = input("Data de término (AAAA-MM-DD) ou Enter se não houver: ").strip()
    if data_fim:
        try:
            if date.fromisoformat(data_fim) < date.fromisoformat(data_inicio):
                print("A data final não pode ser anterior à inicial.")
                return
        except ValueError:
            print("Data de término inválida. Cadastro cancelado.")
            return

    registros = carregar_horarios()
    horario = criar_horario(proximo_id(registros), medicamento_id, hora, data_inicio, data_fim)
    horario["usuario_id"] = usuario["id"]
    registros.append(horario)
    salvar_horarios(registros)
    print("Horário cadastrado com sucesso!")


def listar_horarios(usuario):
    horarios = _meus_horarios(usuario)
    medicamentos = {m["id"]: m["nome"] for m in _meus_medicamentos(usuario)}
    horarios.sort(key=lambda h: h["hora"])
    print("\n--- MEUS HORÁRIOS ---")
    if not horarios:
        print("Nenhum horário cadastrado.")
        return
    for h in horarios:
        nome = medicamentos.get(h["medicamento_id"], "Medicamento não encontrado")
        fim = h["data_fim"] or "sem data final"
        print(f"ID: {h['id']} | {h['hora']} | {nome} | de {h['data_inicio']} até {fim}")


def editar_horario(usuario):
    horarios = carregar_horarios()
    meus_horarios = [h for h in horarios if h["usuario_id"] == usuario["id"]]
    if not meus_horarios:
        print("Não há horários para editar.")
        return

    listar_horarios(usuario)
    identificador = input("Digite o ID do horário que deseja editar: ").strip()
    horario = next((h for h in meus_horarios if h["id"] == identificador), None)
    if horario is None:
        print("Horário não encontrado.")
        return

    medicamentos = _meus_medicamentos(usuario)
    print("Pressione Enter para manter o medicamento atual.")
    for m in medicamentos:
        print(f"{m['id']} - {m['nome']}")
    novo_medicamento = input(f"ID do medicamento [{horario['medicamento_id']}]: ").strip()
    if novo_medicamento:
        if not any(m["id"] == novo_medicamento for m in medicamentos):
            print("Medicamento não encontrado para este usuário. Edição cancelada.")
            return
        horario["medicamento_id"] = novo_medicamento

    nova_hora = input(f"Horário [{horario['hora']}]: ").strip()
    if nova_hora:
        if not validar_hora(nova_hora):
            print("Horário inválido. Edição cancelada.")
            return
        horario["hora"] = nova_hora

    nova_inicio = input(f"Data de início [{horario['data_inicio']}]: ").strip()
    if nova_inicio:
        try:
            date.fromisoformat(nova_inicio)
        except ValueError:
            print("Data de início inválida. Edição cancelada.")
            return
        horario["data_inicio"] = nova_inicio

    atual_fim = horario["data_fim"] or "sem data final"
    novo_fim = input(f"Data de término [{atual_fim}] (Enter mantém; 0 remove): ").strip()
    if novo_fim == "0":
        horario["data_fim"] = ""
    elif novo_fim:
        try:
            date.fromisoformat(novo_fim)
        except ValueError:
            print("Data de término inválida. Edição cancelada.")
            return
        horario["data_fim"] = novo_fim

    if horario["data_fim"] and date.fromisoformat(horario["data_fim"]) < date.fromisoformat(horario["data_inicio"]):
        print("A data final não pode ser anterior à inicial. Edição cancelada.")
        return

    salvar_horarios(horarios)
    print("Horário atualizado com sucesso!")


def excluir_horario(usuario):
    horarios = carregar_horarios()
    meus_horarios = [h for h in horarios if h["usuario_id"] == usuario["id"]]
    if not meus_horarios:
        print("Não há horários para excluir.")
        return

    listar_horarios(usuario)
    identificador = input("Digite o ID do horário que deseja excluir: ").strip()
    horario = next((h for h in meus_horarios if h["id"] == identificador), None)
    if horario is None:
        print("Horário não encontrado.")
        return

    confirmacao = input(f"Confirma a exclusão do horário {horario['hora']}? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Exclusão cancelada.")
        return

    horarios = [h for h in horarios
                if not (h["id"] == identificador and h["usuario_id"] == usuario["id"])]
    salvar_horarios(horarios)
    print("Horário excluído com sucesso!")


def menu_horarios(usuario):
    while True:
        print("\n--- HORÁRIOS ---")
        print("1 - Cadastrar horário")
        print("2 - Listar horários")
        print("3 - Editar horário")
        print("4 - Excluir horário")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            cadastrar_horario(usuario)
        elif opcao == "2":
            listar_horarios(usuario)
        elif opcao == "3":
            editar_horario(usuario)
        elif opcao == "4":
            excluir_horario(usuario)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
