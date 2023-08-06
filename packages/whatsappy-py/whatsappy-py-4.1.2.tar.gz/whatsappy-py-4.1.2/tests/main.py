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

def enviar_imagem(group, caption, image) -> None:
    driver = group._whatsapp.driver
    
    driver.find_element(By.CSS_SELECTOR, Selectors.ATTATCHMENT_MENU).click()
    driver.find_element(By.CSS_SELECTOR, Selectors.INPUT_MIDIA).send_keys(image)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.MEDIA_CAPTION)))

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.MEDIA_CAPTION)))
    
    msg_box = driver.find_element(By.CSS_SELECTOR, Selectors.MEDIA_CAPTION)

    pyperclip.copy(caption)
    msg_box.send_keys(Keys.CONTROL, "v")
    
    driver.find_element(By.CSS_SELECTOR, Selectors.SEND_BUTTON).click()

# Inicializa o WhatsApp Web
whatsapp = Whatsapp(data_path="C:\\Whatsappy", visible=True)

# Evento de quando o WhatsApp Web está pronto
@whatsapp.event
def on_ready() -> None:
    print("WhatsApp Web está pronto!")

# Abre o Whatsapp Web
whatsapp.run()

# Abre o grupo desejado
group = whatsapp.open("Nome do grupo")

# Configura o evento de quando uma mensagem é recebida
@group.event
def on_message(msg) -> None:
    # Testa se o bot está lendo as mensagens
    if msg.content == "ping":
        msg.reply("pong")
    else:
        # Coleta o conteúdo da mensagem
        content = msg.content
        image = baixar_imagem(msg._element)
        
        # Abre o outro grupo
        other_group = whatsapp.open("Nome do outro grupo")

        # Envia a mensagem para o outro grupo
        enviar_imagem(other_group, content, image) # Utilize sempre essa função para enviar as mensagens

        # Voltar para o grupo original
        group.open()

input("Pressione ENTER para sair...")

whatsapp.close()