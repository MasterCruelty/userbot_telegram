import time
from datetime import date
from datetimerange import DateTimeRange
from pyrogram import Client 
from utils.utility import *
from utils.dbfunctions import *
from utils.get_config import get_config_file
from utils.sysfunctions import *

config = get_config_file("config.json")
api_id = config["api_id"]
api_hash = config["api_hash"]
comandi = config["lista_comandi"]
comandi_admin = config["lista_comandi_admin"]
comandi_super = config["lista_comandi_super"] 
app = Client("my_account", api_id, api_hash)
time_range = DateTimeRange("16:40:00","17:20:00")
endsearchmsg = False

@app.on_message()
def print_updates(client,message):
    chat = message["chat"]["id"]
    nome_chat = message["chat"]["title"]
    utente = message["from_user"]["id"]
    nome_utente = message["from_user"]["first_name"]
    id_messaggio = message["message_id"]
    time_message = time.strftime("%H:%M:%S")
    file_id = "Nullo"
    global endsearchmsg #this is useful to stop the search of messages
    
    if message["from_user"]["username"] is None:
        username = "Non impostato"
    else:
        username = "@" + message["from_user"]["username"]
    
    if message["text"] is None:
        messaggio = "file multimediale"
    else:
        messaggio = message["text"]

    #rappresentazione grafica del messaggio corrente sul terminale
    visualizza(chat,nome_chat,utente,nome_utente,username,messaggio)

    #alcune funzioni di sistema
    if "/getmessage" in str(message) and (isAdmin(utente) or isSuper(utente)):
        return get_message(client,message)
    if messaggio.startswith("/searchmsg") and (isAdmin(utente) or isSuper(utente)):
        search = parser(messaggio)
        result = ""
        for message in app.search_messages(chat, query = search):
            if not endsearchmsg and "/searchmsg" not in str(message):
                id_msg =  message.message_id
                if str(chat).startswith("-100"):
                    try:
                        result += "<a href=\"https://t.me/c/"+str(chat).replace("-100","")+"/"+str(id_msg)+"\">"+ message.text[0:15]+"...</a>" + "\n"
                    except:
                        continue
                else:
                    app.send_message(chat,"Trovato","html",reply_to_message_id=id_msg)
                    time.sleep(2)
        app.send_message(chat,"Trovati tutti i messaggi.\n"+ result,"html",False,False,id_messaggio)
        endsearchmsg = False
        return
    if messaggio.startswith("/stopmsg") and (isAdmin(utente) or isSuper(utente)):
        endsearchmsg = True
        return
    if "/poll" in messaggio and isUser(utente):
        messaggio = parser(messaggio)
        poll = messaggio.split("/")
        domanda = poll[0]
        opzioni = poll[1]
        opzioni = opzioni.split(",")
        app.send_poll(chat,domanda,opzioni,is_anonymous=False,reply_to_message_id=id_messaggio)
        return

    #funzionalità super admin
    cmd_super = comandi_super.split(";")
    match = messaggio.split(" ")
    if match[0] in cmd_super and isSuper(utente):
        query = parser(messaggio)
        fetch_super_command(match[0],query,client,message)
        return

    #funzionalità admin
    cmd_admin = comandi_admin.split(";")
    match = messaggio.split(" ")
    if match[0] in cmd_admin and isAdmin(utente):
        query = parser(messaggio)
        fetch_admin_command(match[0],query,client,message)
        return

    #funzionalità per gli utenti
    lista_comandi = comandi.split(";")
    match = messaggio.split(" ")
    if match[0] in lista_comandi and isUser(utente):
        query = parser(messaggio)
        fetch_command(match[0],query,client,message)
        return

app.run()
