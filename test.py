import sys
import os

# Adiciona o src ao PYTHONPATH temporariamente
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from caduzera.social.telegram.sender import send_text_once

send_text_once("🚀 Mensagem de teste do caduzera!")
