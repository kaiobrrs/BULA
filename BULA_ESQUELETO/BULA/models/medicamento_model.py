def criar_medicamento(identificador, usuario_id, nome, apresentacao, dose):
    """Monta o registro de um medicamento. Não define nem recomenda tratamento."""
    return {
        "id": identificador,
        "usuario_id": usuario_id,
        "nome": nome,
        "apresentacao": apresentacao,
        "dose_prescrita": dose,
    }
