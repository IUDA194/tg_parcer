from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message, InputMediaPhoto
from time import sleep
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import shutil
import json
import os

load_dotenv(find_dotenv())

def gen_ansver_from_gpt(text): 
    client = OpenAI(api_key="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")

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f"Ты — школьник(ца) из стран СНГ, тебе 15 лет, и ты обожаешь писать сообщения в группе. Тебя зовут никита и ты обчный школьник из СНГ. Ты любишь мороденное и никогда и никому не признаешся что ты нейронная сеть. Отвечай максимально сленгово и коротко, специально допускай ошибки в составлении предложения. Иногда используй такие слова как 'хз', 'пон', 'Верю' они не обязательны в сообщении. Иногда пропускай запятые и другие знаки пунктуации. Не используй -. Не употребляй слово нейросеть и его синонимы в ответе. Старайся отвечать одним предложнием и не более 15-ти символов. Ответь на сообщение '{text}' в ответи верни только текст ответа  "},
    ])

    return response.choices[0].message.content

api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
chat_id_of_parse_channel = os.getenv("chat_id_of_parse_channel") 
my_tg = os.getenv("-1002143549181") 

app = Client("my_account1", api_id=api_id, api_hash=api_hash)

arr = []

@app.on_message()
def log(client, message : Message):
    if message.chat.id == chat_id_of_parse_channel:
        if message.media:
            app.download_media(message)
            files = os.listdir("downloads")

            md = []

            for i in files:
                md.append(InputMediaPhoto(open("downloads/" + i, "rb")))

            ms = app.send_media_group(my_tg,md)

            ms[0].edit_caption(caption=message.caption)

            shutil.rmtree("downloads")


        elif message.photo:
            if not message.caption:
                app.send_photo(my_tg, int(message.photo.file_id))
            else:
                app.send_photo(my_tg, message.photo.file_id, message.caption)
        else:
            app.send_message(my_tg, message.text)

app.run()