from datetime import datetime

f=open("classes.txt", "r")

days_and_indexes = {
    'Monday':0,
    'Tuesday':1,
    'Wednesday':2,
    'Thursday':3,
    'Friday':4
}

dayindex = days_and_indexes[datetime.now().strftime("%A")]

tomorrows_classes = []

try:
    f.seek(0)
    tomorrows_classes = f.readlines()[dayindex + 1].split()

except IndexError: # Means that the day is Friday, so it should show the first day: Monday. 
    f.seek(0)
    tomorrows_classes = f.readlines()[0].split()

f.seek(0)

todays_classes = f.readlines()[dayindex].split()

cikarilacaklar = []
odd_c = []
koyulacaklar = []
odd_k = []
printed = []

for lesson in todays_classes:
    if lesson not in tomorrows_classes:
        cikarilacaklar.append(lesson)

for lesson in tomorrows_classes:
    if lesson not in todays_classes:
        koyulacaklar.append(lesson)

def rmodd(x):
  return list(dict.fromkeys(x))

# print(koyulacaklar + odd_k, cikarilacaklar + odd_c)
print(rmodd(koyulacaklar), rmodd(cikarilacaklar))
