import telebot
import os

def getbot():
    return telebot.TeleBot(os.getenv("TELEGRAM_BOT"), parse_mode=None)

bot = getbot()

class TelegramBot:
    def __init__(self):
        self.bot = getbot()
        self.bot.polling()

    @bot.message_handler(commands=["pizza"])
    def pizza(self, mensagem):
        self.bot.send_message(mensagem.chat.id,
                        "Saindo a pizza pra sua casa: Tempo de espera em 20min")


    @bot.message_handler(commands=["hamburguer"])
    def hamburguer(self, mensagem):
        self.bot.send_message(mensagem.chat.id, "Saindo o Brabo: em 10min chega ai")


    @bot.message_handler(commands=["salada"])
    def salada(self, mensagem):
        self.bot.send_message(mensagem.chat.id,
                        "Não tem salada não, clique aqui para iniciar: /iniciar")


    @bot.message_handler(commands=["opcao1"])
    def opcao1(self, mensagem):
        texto = """
        O que você quer? (Clique em uma opção)
        /pizza Pizza
        /hamburguer Hamburguer
        /salada Salada"""
        self.bot.send_message(mensagem.chat.id, texto)


    @bot.message_handler(commands=["opcao2"])
    def opcao2(self, mensagem):
        self.bot.send_message(
            mensagem.chat.id, "Para enviar uma reclamação, mande um e-mail para reclamação@balbalba.com")


    @bot.message_handler(commands=["opcao3"])
    def opcao3(self, mensagem):
        self.bot.send_message(mensagem.chat.id, "Valeu! Lira mandou um abraço de volta")


    def verificar(self, mensagem):
        return True


    @bot.message_handler(func=verificar)
    def responder(self, mensagem):
        texto = """
        Escolha uma opção para continuar (Clique no item):
        /opcao1 Fazer um pedido
        /opcao2 Reclamar de um pedido
        /opcao3 Mandar um abraço pro Lira
    Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
        self.bot.reply_to(mensagem, texto)



if __name__ == '__main__':
    TelegramBot()