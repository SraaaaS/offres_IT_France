from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY = os.getenv("FT_API_KEY")
CLIENT = os.getenv("CLIENT_ID")
TOKEN_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"
NUM_PAGES = 25

data = {"grant_type": "client_credentials",
        "client_id": CLIENT,
        "client_secret": API_KEY,
        "scope" : "api_offresdemploiv2 o2dsoffre"
        }

response = requests.post(TOKEN_URL, data=data)
#print(response.json())

print(response.status_code, response.text)

TOKEN = response.json().get("access_token")
URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"


CODE_ROME_IT = {"M1805": "Etudes et Développement informatique" , "I1401": "Maintenance informatique et bureautique" , "M1801": "Administration de systèmes d'information",
                "M1803": "Direction des systèmes d'information", "M1806": "Expertise et support technique en systèmes d'information" , 
                "M1810": "Production et exploitation de systèmes d'information" , "M1804": " Études et développement de réseaux de télécoms"}
                
headers = {"Authorization" : f"Bearer {TOKEN}"}

params = {"grandDomaine": "M18"}

# response = requests.get(URL, headers=headers, params=params)
# data = response.json()
# print(data.keys())
# print(len(data["resultats"]))

# nombre = 0
# i = 0
# while True:
#     params = {"grandDomaine": "M18", "range" : f"{i}-{i+149}"}
#     response = requests.get(URL, headers=headers, params=params)
#     data = response.json()
#     print(data)
#     if not data["resultats"]:
#         break
#     nombre += len(data["resultats"])
#     i+=150
#     print(f"Nombre total d'offres M18: {nombre}")
import time

from datetime import datetime, timedelta

total = 0
for i in range(1, 96):
    pages=0
    departement = 0
    while pages<=3000:
        params = {"grandDomaine": "M18", "departement" : f"{i:02d}", "range" : f"{pages}-{pages+149}"}
        response = requests.get(URL, headers=headers, params=params)
        if response.status_code != 200:
                print("Erreur HTTP :", response.status_code)
                print(response.text)
                break
        try:
                data = response.json()
        except:
                print("Reponse non JSON :", response.text)
                break
        if "resultats" not in data:
            print(f"Erreur département {i:02d} :", data)
            break
        departement = len(data["resultats"])
        print(f"nombre d'offres pour le departement {i:02d} : {departement}")

        total += departement
        pages +=150
        time.sleep(0.2)
print(f"Nombre total d'offres M18: {total}")




def count_offres(date_min, date_max):
    total = 0
    i = 0

    while i <= 3000:
        params = {
            "grandDomaine": "M18",
            "minCreationDate": date_min,
            "maxCreationDate": date_max,
            "range": f"{i}-{i+149}"
        }

        response = requests.get(URL, headers=headers, params=params)
        data = response.json()
        print(response.url)

        if "resultats" not in data or not data["resultats"]:
            break

        total += len(data["resultats"])
        i += 150

    return total

start_date = datetime(2021, 1, 1)
end_date = datetime(2026, 1, 1)

current = start_date

while current < end_date:
    week_start = current
    week_end = current + timedelta(days=6)

    total = count_offres(
        week_start.strftime("%Y-%m-%d"),
        week_end.strftime("%Y-%m-%d")
    )

    print(
        f"Semaine {week_start.strftime('%Y-%m-%d')} → "
        f"{week_end.strftime('%Y-%m-%d')} : {total}"
    )

    current += timedelta(days=7)

