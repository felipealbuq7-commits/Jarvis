import datetime
from voice import falar, ouvir


def saudar() -> None:
    """Cumprimenta o usuário de acordo com o horário do dia."""
    hora = datetime.datetime.now().hour

    if 5 <= hora < 12:
        saudacao = "Bom dia"
    elif 12 <= hora < 18:
        saudacao = "Boa tarde"
    else:
        saudacao = "Boa noite"

    falar(f"{saudacao}! Eu sou o JARVIS. Como posso ajudar?")


def processar_comando(comando: str) -> bool:
    """
    Recebe um comando em texto e executa a ação correspondente.
    Retorna False se o comando for para encerrar o programa.
    """

    # --- Saudações ---
    if any(palavra in comando for palavra in ["olá", "ola", "oi", "bom dia", "boa tarde", "boa noite"]):
        falar("Olá! Estou aqui. Como posso ajudar?")

    # --- Horas ---
    elif any(palavra in comando for palavra in ["horas", "hora", "que horas"]):
        agora = datetime.datetime.now()
        falar(f"São {agora.hour} horas e {agora.minute} minutos.")

    # --- Data ---
    elif any(palavra in comando for palavra in ["data", "dia", "que dia"]):
        hoje = datetime.datetime.now()
        falar(f"Hoje é dia {hoje.day} do {hoje.month} de {hoje.year}.")

    # --- Encerrar ---
    elif any(palavra in comando for palavra in ["sair", "encerrar", "fechar", "tchau", "até logo"]):
        falar("Encerrando. Até logo!")
        return False  # sinaliza para o loop parar

    # --- Comando não reconhecido ---
    else:
        falar("Desculpe, não entendi o comando.")

    return True  # continua o loop


def main():
    saudar()

    while True:
        comando = ouvir()

        if comando is None:
            # Não ouviu nada — continua aguardando
            continue

        continuar = processar_comando(comando)

        if not continuar:
            break


if __name__ == "__main__":
    main()
