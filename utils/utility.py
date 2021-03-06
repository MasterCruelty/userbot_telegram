import time
import os
from pyrogram import Client
import utils_config
import modules.wiki
import modules.gmaps
import modules.lyrics
import modules.atm_feature
import modules.covid
import utils.dbfunctions
import utils.sysfunctions
import utils.get_config

"""
Questa funzione prende come argomento il match e la richiesta dal main e dirotta la richiesta sul file dedicato a quel comando
"""
def fetch_command(match,query,client,message):
    if match == "/wiki" and check_group(client,message):
        return modules.wiki.execute_wiki(query,client,message)
    if match == "/map" and check_group(client,message):
        return modules.gmaps.showmaps(query,client,message)
    if match == "/km" and check_group(client,message):
        return modules.gmaps.execute_km(query,client,message)
    if match == "/route":
        return modules.gmaps.execute_route(query,client,message)
    if match == "/lyrics" and check_group(client,message):
        return modules.lyrics.execute_lyrics(query,client,message)
    if match == "/atm" and check_group(client,message):
        return modules.atm_feature.get_stop_info(query,client,message)
    if match == "/geoatm" and check_group(client,message):
        return modules.atm_feature.geodata_stop(query,client,message)
    if match == "/edatm" and check_group(client,message):
        return modules.atm_feature.get_rivendita_info(query,client,message)
    if match == "/searchatm" and check_group(client,message):
        return modules.atm_feature.search_line(client,message,query)
    if match == "/covid" and check_group(client,message):
        return modules.covid.covid_cases(client,message,query)
    if match == "/poll" and check_group(client,message):
        return utils.sysfunctions.poll_function(client,message,query)
    if match == "/help" and check_group(client,message):
        return utils.sysfunctions.help(client,message,query)

"""
Analogamente a fetch_command ma per i comandi esclusivi degli utenti admin
"""
def fetch_admin_command(match,query,client,message):
    #system functions
    if match == "/hcount":
        return utils.sysfunctions.count_messages(client,message)
    if match == "/id":
        return utils.sysfunctions.id_chat(client,message)
    if match == "/getid":
        return utils.sysfunctions.get_id(client,message)
    if match == "/getuser":
        return utils.sysfunctions.get_user(client,message,query)
    if match == "/getmessage" and check_group(client,message):
        return utils.sysfunctions.get_message(client,message)
    if match == "/playlotto":
        return utils.sysfunctions.play_lotto(client,message)
    if match == "/searchmsg":
        return utils.sysfunctions.search_msg(client,message,query)
    if match == "/stopmsg":
        return utils.dbfunctions.stop_msg_true()
    if match == "/ping":
        return utils.sysfunctions.ping(client,message)

"""
Analogamente a fetch_command ma per i comandi esclusivi del super admin
"""
def fetch_super_command(match,query,client,message):
    #db functions
    if match == "/setuser":
        return utils.dbfunctions.set_user(client,message,query)
    if match == "/deluser":
        return utils.dbfunctions.del_user(client,message,query)
    if match == "/listuser":
        return utils.dbfunctions.list_user(client,message)
    if match == "/alluser":
        return utils.dbfunctions.all_user(client,message)
    if match == "/setadmin":
        return utils.dbfunctions.set_admin(client,message,query)
    if match == "/deladmin":
        return utils.dbfunctions.del_admin(client,message,query)
    if match == "/listadmin":
        return utils.dbfunctions.list_admin(client,message)
    if match == "/alladmin":
        return utils.dbfunctions.all_admin(client,message)
    if match == "/ipbanned":
        return showIpBanned(client,message)

"""
controlla che robbot non sia nella stessa chat, altrimenti esegue il comando
"""
@Client.on_message()
def check_group(client,message):
    try:
        check = client.get_chat_member(utils.get_config.get_chat(message),133326326)
        return False
    except:
        return True

"""
funzione che aiuta a parsare i comandi nel sorgente principale senza sporcare troppo in giro
"""
def parser(message):
    temp = message.split(" ",1)
    try:
        result = temp[1]
    except:
        result = temp[0]
    return result

"""
	funzione che salva su file il json del messaggio Telegram in arrivo
"""
def save_json(message):
    nome_file = "json_message.json"
    save = open(nome_file,'w')
    save.write(str(message))
    save.close()
"""
	funzione che esegue uno script shell per recuperare gli ip bannati sul raspberry pi
"""
@Client.on_message()
def showIpBanned(client,message):
    os.system("chmod +x full_path/ip_banned.sh|sh full_path/ip_banned.sh")
    utils.get_config.sendMessage(client,message,"Sto inviando il file...")
    return client.send_document(utils.get_config.get_chat(message),"ip_banned.txt","html")

"""
	funzione per visualizzare a schermo i dati principali del messaggio in arrivo
"""
def visualizza(chat,nome_chat,utente,nome_utente,username,messaggio):
    print("id_utente: " + str(utente) + "\nnome_utente: " + nome_utente + "\nusername: " + username)
    try:
        print("chat_id: " + str(chat) + "\nnome_chat: " + nome_chat)
    except:
        print("messaggio ricevuto da un channel o chat privata")
    print("\n\nMessaggio: " + messaggio + "\n" )
    print("**************************************************************************************")
    if str(chat):
        return "nome_chat: " + str(chat) +"id_utente: " + str(utente) + "\nnome_utente: " + nome_utente + "\nusername: " + username + "\n\n" + "Messaggio: " + messaggio
"""
    da rifattorizzare: funzione per recuperare il file id del messaggio corrente
    plus: per rendere la funzione utile si dovrebbe gestire anche il parametro file_ref
"""
def recuperaFileID(message):
    try:
        try:
            file_id = message["photo"]["file_id"]
        except:
            try:
                file_id = message["animation"]["file_id"]
            except:
                try:
                    file_id = message["video_note"]["file_id"]
                except:
                    file_id = message["video"]["file_id"]
    except:
        print("formato multimediale non supportato da questa app")
        file_id = "Non supportato"
    print(">>>>file_id recuperato correttamente<<<< => " + file_id)
    return file_id
