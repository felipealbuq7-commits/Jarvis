"""
interface.py — Servidor web local do JARVIS.

Abre um servidor Flask na porta 5000 e usa WebSocket (Socket.IO)
para comunicar em tempo real com a interface HTML.

Como funciona:
- O navegador se conecta em http://localhost:5000
- O main.py chama as funções emit_* daqui para atualizar a tela
- O navegador pode enviar comandos de texto via socket
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit as socketio_emit
import threading
import webbrowser
import time

app = Flask(
    __name__,
    template_folder=".",   # index.html está na mesma pasta
    static_folder="."      # style.css e script.js também
)
app.config["SECRET_KEY"] = "jarvis-secret"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# Callback registrado pelo main.py para processar comandos vindos da interface
_comando_callback = None


def registrar_callback(fn):
    """
    Registra a função que será chamada quando o usuário enviar
    um comando de texto pela interface.
    """
    global _comando_callback
    _comando_callback = fn


# ── Funções chamadas pelo main.py para atualizar a interface ──────────────────

def emit_status(status: str):
    """
    Atualiza o status exibido na interface.
    status: 'ouvindo' | 'processando' | 'falando' | 'aguardando'
    """
    socketio.emit("status", {"valor": status})


def emit_mensagem_usuario(texto: str):
    """Exibe o que o usuário disse na tela."""
    socketio.emit("mensagem_usuario", {"texto": texto})


def emit_mensagem_jarvis(texto: str):
    """Exibe o que o JARVIS respondeu na tela."""
    socketio.emit("mensagem_jarvis", {"texto": texto})


def emit_encerrar():
    """Avisa a interface que o JARVIS está encerrando."""
    socketio.emit("encerrar", {})


# ── Rotas Flask ───────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


# ── Eventos Socket.IO ─────────────────────────────────────────────────────────

@socketio.on("connect")
def on_connect():
    print("Interface conectada.")
    socketio_emit("status", {"valor": "aguardando"})


@socketio.on("comando_texto")
def on_comando_texto(data):
    """Recebe um comando digitado pelo usuário na interface."""
    texto = data.get("texto", "").strip().lower()
    if texto and _comando_callback:
        threading.Thread(target=_comando_callback, args=(texto,), daemon=True).start()


# ── Inicialização ─────────────────────────────────────────────────────────────

def iniciar_servidor(abrir_navegador: bool = True):
    """
    Inicia o servidor em uma thread separada para não bloquear o main.py.
    """
    def _run():
        socketio.run(app, host="127.0.0.1", port=5000, use_reloader=False, log_output=False)

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()

    # Aguarda o servidor subir antes de abrir o navegador
    time.sleep(1.5)

    if abrir_navegador:
        webbrowser.open("http://localhost:5000")

    print("Interface disponível em: http://localhost:5000")
