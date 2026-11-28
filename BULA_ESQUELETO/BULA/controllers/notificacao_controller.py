from datetime import date, datetime
from pathlib import Path
from controllers.horario_controller import carregar_horarios
from controllers.medicamento_controller import carregar_medicamentos


def verificar_notificacoes(usuario=None):
    horarios = carregar_horarios()
    hoje = date.today()
    medicamentos = {m["id"]: m["nome"] for m in carregar_medicamentos()
                    if usuario is None or m["usuario_id"] == usuario["id"]}
    ativos = []
    for h in horarios:
        if usuario is not None and h["usuario_id"] != usuario["id"]:
            continue
        try:
            inicio = date.fromisoformat(h["data_inicio"])
            fim = date.fromisoformat(h["data_fim"]) if h["data_fim"] else None
            hora = datetime.strptime(h["hora"], "%H:%M").time()
        except ValueError:
            continue
        if inicio <= hoje and (fim is None or hoje <= fim):
            ativos.append((hora, h))
    ativos.sort(key=lambda item: item[0])
    print("\n--- LEMBRETES DE HOJE ---")
    if not ativos:
        print("Nenhum horário ativo encontrado para hoje.")
        return
    for hora, h in ativos:
        nome = medicamentos.get(h["medicamento_id"], "medicamento cadastrado")
        print(f"Lembrete: {nome} às {hora.strftime('%H:%M')}.")


def menu_notificacoes(usuario=None):
    while True:
        print("\n--- NOTIFICAÇÕES ---")
        print("1 - Verificar lembretes de hoje")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            verificar_notificacoes(usuario)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
