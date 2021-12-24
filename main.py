from datetime import datetime
import schedule
from telegram import Update, ForceReply, update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.ext.dispatcher import Dispatcher
from config import APIKEY
from time import sleep

f=open("classes.txt", "r")

days_and_indexes = {
    'Monday':0,
    'Tuesday':1,
    'Wednesday':2,
    'Thursday':3,
    'Friday':4,
    'Saturday':5,
    'Sunday':6
}

dayindex = days_and_indexes[datetime.now().strftime("%A")]

tomorrows_classes = []

try:
    f.seek(0)
    tomorrows_classes = f.readlines()[dayindex + 1].split()

except IndexError: # Means that the day is Friday or weekend, so it should show the first day: Monday. 
    f.seek(0)
    tomorrows_classes = f.readlines()[0].split()

f.seek(0)

todays_classes = f.readlines()[4].split()
# Set Friday as default, if there is an error the day will be set to Friday.

try:
    f.seek(0)
    todays_classes = f.readlines()[dayindex].split()
except IndexError: # Weekend, we need to use the  
    f.seek(0)
    todays_classes = f.readlines()[4].split()

cikarilacaklar = []
odd_c = []
koyulacaklar = []
odd_k = []
printed = []
still_scheduled = True

f.seek(0)

for lesson in todays_classes:
    if lesson not in tomorrows_classes:
        cikarilacaklar.append(lesson)

for lesson in tomorrows_classes:
    if lesson not in todays_classes:
        koyulacaklar.append(lesson)

def rmodd(x):
  return list(dict.fromkeys(x))

def ders_command(update: Update, context: CallbackContext):
    koyulacaklar_formatted = "".join([x  + "\n" for x in rmodd(koyulacaklar)])
    cikarilacaklar_formatted = "".join([y  + "\n" for y in rmodd(cikarilacaklar)])
    update.message.reply_text(f"Cantana koyman gerekenler:\n {koyulacaklar_formatted}\nCantandan cikarman gerekenler:\n {cikarilacaklar_formatted}")

def remind_syllabus(update: Update):    
    print("HEY!")
    dayindex = days_and_indexes[datetime.now().strftime("%A")]

    tomorrows_classes = []

    try:
        f.seek(0)
        tomorrows_classes = f.readlines()[dayindex + 1].split()
    except IndexError: # Means that the day is Friday or weekend, so it should show the first day: Monday. 
        f.seek(0)
        tomorrows_classes = f.readlines()[0].split()
    f.seek(0)

    todays_classes = f.readlines()[4].split()
    # Set Friday as default, if there is an error the day will be set to Friday.

    try:
        f.seek(0)
        todays_classes = f.readlines()[dayindex].split()
    except IndexError: # Weekend, we need to use the  
        f.seek(0)
        todays_classes = f.readlines()[4].split()

    cikarilacaklar = []
    koyulacaklar = []

    for lesson in todays_classes:
        if lesson not in tomorrows_classes:
            cikarilacaklar.append(lesson)

    for lesson in tomorrows_classes:
        if lesson not in todays_classes:
            koyulacaklar.append(lesson)

    koyulacaklar_formatted = "".join([x  + "\n" for x in rmodd(koyulacaklar)])
    cikarilacaklar_formatted = "".join([y  + "\n" for y in rmodd(cikarilacaklar)])
    update.message.reply_text(f"Cantana koyman gerekenler:\n {koyulacaklar_formatted}\nCantandan cikarman gerekenler:\n {cikarilacaklar_formatted}")
        

def dontsend(update: Update, context: CallbackContext):
    still_scheduled = False

def calistir(update):
    while datetime.now().hour != 22:
        sleep(5)

    remind_syllabus(update)

def sendmethesyllabus(update: Update, context: CallbackContext):
    if still_scheduled:
        update.message.reply_text("Tamam, mesaj 22'de gonderiyorum.")
        g = open("subscribers.txt", "a+")
        g.seek(0)
        inlist = False

        for line in g.readlines():
            if str(dict(update.to_dict()['message']["chat"])["title"]) not in line:
                g.write(str(dict(update.to_dict()['message']["chat"])["title"]) + "\n")
                inlist = True

        if inlist:
            update.message.reply_text("Zaten aklimdasin ki :)")
            g.close()
        calistir(update)

def nosyllabuses(update: Update, context: CallbackContext):
    still_scheduled = False
# print(rmodd(koyulacaklar), rmodd(cikarilacaklar))

updater = Updater(APIKEY)
g=open("subscribers.txt", "r")
g.seek(0)

def check(update: Update, context: CallbackContext):    
    print("check")
    for line in g.readlines():
        if str(dict(update.to_dict()['message']["chat"])["title"]) in line:
             calistir(update)
        else:
            print("didnt work")

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.all , check))
dispatcher.add_handler(CommandHandler("dersprogrami", ders_command))
dispatcher.add_handler(CommandHandler("hatirlat", sendmethesyllabus))
dispatcher.add_handler(CommandHandler("hatirlatma", dontsend))
updater.start_polling()
updater.idle()
