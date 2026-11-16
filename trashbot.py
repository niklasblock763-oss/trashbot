import requests
from icalendar import Calendar
from datetime import datetime, timedelta
import time
import os 

def trash_today():

    url = "http://marburg.mein-abfallkalender.online/ical.ics?sid=5786&cd=inline&ft=6&fu=webcal_other&fp=next_30&wids=137,138,139,148,136,140,141&uid=200646&pwid=7d67950918&cid=22"

    while True:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            cal = Calendar.from_ical(response.content)
            break
        except Exception as e:
            print("Kalender laden fehlgeschlagen, neuer Versuch in 60s:", e)
            time.sleep(60)

    tomorrow = datetime.now().date() + timedelta(days=1)

    bins = []

    for component in cal.walk():
        if component.name == "VEVENT":
            summary = str(component.get("summary"))
            dtstart = component.get("dtstart").dt

            if dtstart == tomorrow:
                clean = summary.split("(")[0].strip()

                if clean not in bins:
                    bins.append(clean)

    return bins



def trash_today2():

    url = "http://marburg.mein-abfallkalender.online/ical.ics?sid=6330&cd=inline&ft=6&fu=webcal_other&fp=next_30&wids=137,138,139,148,136,140,141&uid=200646&pwid=7d67950918&cid=22"

    while True:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            cal = Calendar.from_ical(response.content)
            break
        except Exception as e:
            print("Kalender laden fehlgeschlagen, neuer Versuch in 60s:", e)
            time.sleep(60)

    tomorrow = datetime.now().date() + timedelta(days=1)

    bins = []

    for component in cal.walk():
        if component.name == "VEVENT":
            summary = str(component.get("summary"))
            dtstart = component.get("dtstart").dt

            if dtstart == tomorrow:
                clean = summary.split("(")[0].strip()

                if clean not in bins:
                    bins.append(clean)

    return bins


def check(TOKEN,CHAT_ID): #Bismarck
    bins = trash_today()

    if bins:
        text = "Morgen wird abgeholt: " + ", ".join(bins)
        send_telegram(text,TOKEN,CHAT_ID)
                

def check2(TOKEN,CHAT_ID): #Universitäts
    bins = trash_today2()

    if bins:
        #text = "Morgen wird abgeholt: " + ", ".join(bins)
        #send_telegram(text,TOKEN,CHAT_ID)
        
        text = "Hallo kann mir mal wer privat kurz schreiben ob diese Nachricht ankam? Wenn ja funktioniert der Bot jetzt"
        send_telegram(text,TOKEN,CHAT_ID)
        


def send_telegram(message,TOKEN,CHAT_ID):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    
    requests.post(url, data=data)


    
if __name__ == "__main__":
    TOKEN = os.environ["TOKEN"]
    CHAT_ID = os.environ["CHAT_ID"]
    CHAT_ID2 = os.environ["CHAT_ID2"]
    check(TOKEN, CHAT_ID)
    check2(TOKEN, CHAT_ID2)

