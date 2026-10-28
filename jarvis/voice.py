import pyttsx3
import speech_recognition as sr

# Inicializa o mecanismo de voz
engine = pyttsx3.init()

# Configura a velocidade e o volume da voz
engine.setProperty("rate", 175)    # velocidade da fala (padrão ~200)
engine.setProperty("volume", 1.0)  # volume: 0.0 a 1.0


def falar(texto: str) -> None:
    """Faz o JARVIS falar o texto em voz alta."""
    print(f"JARVIS: {texto}")
    engine.say(texto)
    engine.runAndWait()


def ouvir() -> str | None:
    """
    Captura o áudio do microfone e retorna o texto reconhecido.
    Retorna None se não entender ou ocorrer algum erro.
    """
    reconhecedor = sr.Recognizer()

    with sr.Microphone() as fonte:
        print("Ouvindo...")
        reconhecedor.adjust_for_ambient_noise(fonte, duration=0.5)
        try:
            audio = reconhecedor.listen(fonte, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return None

    try:
        texto = reconhecedor.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {texto}")
        return texto.lower()
    except sr.UnknownValueError:
        # Não conseguiu entender o áudio
        return None
    except sr.RequestError as e:
        print(f"Erro ao conectar ao serviço de reconhecimento: {e}")
        return None
