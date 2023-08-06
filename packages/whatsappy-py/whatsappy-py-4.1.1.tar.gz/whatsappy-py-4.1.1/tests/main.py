from whatsappy import Whatsapp
from whatsappy.chat import Selectors
import pyperclip # pip install pyperclip

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def baixar_imagem(element):
    # TODO: Implementar
    ...

# Inicializa o WhatsApp Web
whatsapp = Whatsapp(data_path="C:\\Whatsappy", visible=True)

# Evento de quando o WhatsApp Web está pronto
@whatsapp.event
def on_ready() -> None:
    print("WhatsApp Web está pronto!")

# Abre o Whatsapp Web
whatsapp.run()

# Abre o grupo desejado
group = whatsapp.open("Teste")

# Configura o evento de quando uma mensagem é recebida
@group.event
def on_message(msg) -> None:
    # Testa se o bot está lendo as mensagens
    if msg.content == "ping":
        msg.reply("pong")
    else:
        # Coleta o conteúdo da mensagem
        content = msg.content
        
        # Abre o outro grupo
        other_group = whatsapp.open("Euzinho da silva")

        # Envia a mensagem para o outro grupo
        other_group.send(content)

        # Voltar para o grupo original
        group.open()

input("Pressione ENTER para sair...")

whatsapp.close()