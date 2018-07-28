# telepot API: https://github.com/nickoala/telepot
import time
import re
import random
import requests
import telepot
from sets import Set
from pprint import pprint
from telepot.loop import MessageLoop

killed = False
forwardChat = Set([])
keywords = Set([r"uppsala", r"sentinel"])

def on_chat_message(msg):
    global killed
    if killed:
        return
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)
    chat_id, message_id = telepot.message_identifier(msg)   
    # text behavior
    try:
        detected = False
        for key in keywords:
            if re.search(key, msg["text"], re.IGNORECASE):
                detected = True

        if detected:
            for id in forwardChat:
                print("forward to "+str(id))
                print(bot.getChat(chat_id))
                try:
                    bot.sendMessage(id, "A keyword was detected at '"+bot.getChat(chat_id)["title"]+"'")
                except KeyError, e:
                    bot.sendMessage(id, bot.getChat(chat_id)["username"]+" mentioned a keyword")
                print(message_id)
                bot.forwardMessage(chat_id=id, from_chat_id=chat_id, message_id=message_id)
        
        if chat_type <> "private":
            return

        if "/subscribe" in msg["text"]:
            forwardChat.add( chat_id )
            print("subscribed: "+str(chat_id))
            bot.sendMessage(chat_id, "You're subscribed to the bot")

        if "/unsubscribe" in msg["text"]:
            forwardChat.remove( chat_id )
            print("unsubscribed: "+str(chat_id))
            bot.sendMessage(chat_id, "You're unsubscribed from the bot")
        
        if "/list" in msg["text"]:
            s = "Keywords: "
            for key in keywords:
                s += key+", "
            bot.sendMessage(chat_id, s)

        if "/add" in msg["text"]:
            newKeys = msg["text"][4:].split(" ")
            for key in newKeys:
                if key != "":
                    keywords.add(key.lower())
            s = "Keywords: "
            for key in keywords:
                s += key+", "
            bot.sendMessage(chat_id, s)
        
        if "/remove" in msg["text"]:
            keywords.remove( msg["text"][7:].replace(" ",""))
            s = "Keywords: "
            for key in keywords:
                s += key+", "
            bot.sendMessage(chat_id, s)

        if "/kill" in msg["text"]:
            killed = True

    except KeyError, e:
        print("Recieved KeyError: %s" % e)

def get_token(secret_path):
    with open(secret_path) as f:
        return f.read().strip()

def main():
    print("Bot starting")

    MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()
        #'callback_query': on_callback_query,
        #'inline_query': on_inline_query,
        #'chosen_inline_result': on_chosen_inline_result}).run_as_thread()

    #bot.message_loop()
    while True:
        time.sleep(10)

bot = telepot.Bot(get_token(".telegram_bot_secret"))

if __name__ == "__main__":
    main()
