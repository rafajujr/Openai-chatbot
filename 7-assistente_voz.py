import openai
import speech_recognition as sr
from playsound import playsound
from pathlib import Path
from io import BytesIO
import io


client = openai.Client(
    api_key=
    "OPENAI_API_KEY"
    )

arquivo_audio = 'hello.mp3'

recognizer = sr.Recognizer()

def grava_audio():
    """Captura áudio do microfine e retrona áudio gravado"""
    with sr.Microphone(0) as source:
        print('Ouvindo...')
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    return audio

def transcricao_audio(audio):
    """Retorna a transcricao do áudio"""
    try:
        wav_data = audio.get_wav_data()
        buffer = io.BytesIO(wav_data)
        buffer.name = 'audio.wav'
        transcricao = client.audio.transcriptions.create(
            model='whisper-1',
            file=buffer
        )
        print(transcricao.text)
        return transcricao.text
    except Exception as e:
        print(f'Ocorreu um erro ao transcrever o áudio: {e}')
        return ''
    
def completa_texto(mensagens):
    """Gera uma com base no histórico de mensagens usando o GPT 3.5"""
    try:
        resposta = client.chat.completions.create(
            messages=mensagens,
            model='gpt-3.5-turbo-0125',
            max_tokens=1000,
            temperature=0
        )
        return resposta.choices[0].message.content
    except Exception as e:
        print(f'Ocorreu um erro ao completar o texto: {e}')
        return 'Desculpe não consegui entender'

def cria_audio(texto):
    """Cria áudio a partir de texto usando a api do TTS"""
    if Path(arquivo_audio).exists():
        Path(arquivo_audio).unlink()
    try:
        resposta = client.audio.speech.create(
            model='tts-1',
            voice='alloy',
            input=texto
        )
        resposta.write_to_file(arquivo_audio)
    except Exception as e:
        print(f'Ocorreu um erro ao criar o áudio: {e}')


def roda_audio():
    """Reproduz o arquivo de áudio"""
    if Path(arquivo_audio).exists():
        playsound(arquivo_audio)
    else:
        print('Arquivo de áudio nao encontrado')


def main():
    """Função principal para executar o assistente de voz"""
    mensagens = []
    while True:
        audio = grava_audio()
        texto = transcricao_audio(audio)

        if not texto:
            print('Não foi possivel transcrever o áudio')
            continue
        mensagens.append({"role": "user", "content": texto})
        print(f"User: {mensagens[-1]["content"]}")

        resposta = completa_texto(mensagens)
        mensagens.append({"role": "assistant", "content": resposta})
        print(f"Bot: {mensagens[-1]["content"]}")

        cria_audio(resposta)
        roda_audio()


if __name__ == '__main__':
    main()