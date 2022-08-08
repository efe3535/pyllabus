from datetime import datetime
from telegram import Update, ForceReply, update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import APIKEY

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
dayst = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
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
except IndexError: # Weekend
    f.seek(0)
    todays_classes = f.readlines()[4].split()

cikarilacaklar = []
odd_c = []
koyulacaklar = []
odd_k = []
printed = []

f.seek(0)

for lesson in todays_classes:
    if lesson not in tomorrows_classes:
        cikarilacaklar.append(lesson)

for lesson in tomorrows_classes:
    if lesson not in todays_classes:
        koyulacaklar.append(lesson)
def rmodd(x):
  return list(dict.fromkeys(x))
def hprogram(update: Update, context: CallbackContext):
    j=""
    for i in range(0,5):
        j+=dayst[i]+': '+f.readline()
    update.message.reply_text(f"Haftalık ders programı:\n{j}")
def gprogram(update: Update, context: CallbackContext):
    for i in range(0, dayindex-2):
        f.readline()
    j = f.readline() 
    j = j.replace(' ', '\n')
    update.message.reply_text(f"Bu günün dersleri:\n{j}")
        
def ders_command(update: Update, context: CallbackContext):
    koyulacaklar_formatted = "".join([x  + "\n" for x in rmodd(koyulacaklar)])
    cikarilacaklar_formatted = "".join([y  + "\n" for y in rmodd(cikarilacaklar)])
    update.message.reply_text(f"Tomorrow's books:\n{koyulacaklar_formatted}\nBooks you don't need anymore:\n{cikarilacaklar_formatted}")

# print(rmodd(koyulacaklar), rmodd(cikarilacaklar))

updater = Updater(APIKEY)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("dersprogrami", ders_command))
dispatcher.add_handler(CommandHandler("haftalikprogram", hprogram))
dispatcher.add_handler(CommandHandler("gunlukprogram", gprogram))
updater.start_polling()
updater.idle()
