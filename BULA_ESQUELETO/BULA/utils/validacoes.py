def validar_nome(nome):
    partes = nome.split()
    return len(partes) >= 2 and all(parte.replace("-", "").replace("'", "").isalpha() for parte in partes)


def validar_email(email):
    return "@" in email and "." in email.split("@")[-1] and " " not in email


def validar_telefone(telefone):
    numeros = "".join(caractere for caractere in telefone if caractere.isdigit())
    return len(numeros) in (10, 11)


def validar_senha(senha):
    return len(senha) >= 6


def validar_hora(hora):
    """Aceita o formato HH:MM, de 00:00 até 23:59."""
    if len(hora) != 5 or hora[2] != ":":
        return False
    try:
        horas, minutos = hora.split(":")
        return 0 <= int(horas) <= 23 and 0 <= int(minutos) <= 59
    except ValueError:
        return False
