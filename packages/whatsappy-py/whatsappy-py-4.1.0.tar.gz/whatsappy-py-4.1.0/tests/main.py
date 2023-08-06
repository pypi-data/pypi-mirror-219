from whatsappy import Whatsapp
from time import sleep

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
        other_group.send(content, attatchments=[image])

        # Voltar para o grupo original
        group.open()

# Aguarda o usuário pressionar ENTER para finalizar o programa
input("Pressione ENTER para sair...")

whatsapp.close()