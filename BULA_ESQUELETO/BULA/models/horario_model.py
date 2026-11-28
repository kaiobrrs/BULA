def criar_horario(identificador, medicamento_id, hora, data_inicio, data_fim):
    return {
        "id": identificador,
        "medicamento_id": medicamento_id,
        "hora": hora,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }
