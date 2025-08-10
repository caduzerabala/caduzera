import sys
import os

# Adiciona o src ao PYTHONPATH temporariamente
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from caduzera.social.telegram.sender import send_text_once
from caduzera.social.telegram.receiver import Receiver

def main():
    social_telegram_send_message()
    # social_telegram_receive_from_channel()

def social_telegram_send_message():
    send_text_once("🚀 Mensagem de teste do caduzera bala!")

def social_telegram_receive_from_channel():
    receiver = Receiver(social_telegram_did_receive_telegram_message)
    receiver.start()

def social_telegram_did_receive_telegram_message(mensagem):
    print(f"💬 Nova mensagem recebida:", mensagem['text'])

if __name__ == "__main__":
    main()