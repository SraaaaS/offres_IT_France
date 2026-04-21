from dotenv import load_dotenv
import os
import requests
import time
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from loguru import logger
import pandas as pd

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



def get_offres():
    hexagone = [i for i in range(1,96)]
    outre_mer = [971, 972, 973, 974, 976]
    corse = ["2A", "2B"]

    dates = []
    total = 0
    for i in hexagone + outre_mer + corse :
        pages = 0
        departement = 0
        while True:
            if i in corse + outre_mer : 
                params = {"grandDomaine": "M18", "departement" : f"{i}", "range" : f"{pages}-{pages+149}"}
            else:
                params = {"grandDomaine": "M18", "departement" : f"{i:02d}", "range" : f"{pages}-{pages+149}"}

            response = requests.get(URL, headers=headers, params=params)

            if response.status_code != 206 and response.status_code !=200:    
                logger.info(f"Erreur HTTP : {response.status_code}")
                break    
            
            data = response.json()
            for offre in data["resultats"]:
                #logger.info(offre["dateCreation"].split("T")[0])
                date_obj = datetime.strptime(offre["dateCreation"], "%Y-%m-%dT%H:%M:%S.%fZ")
                date_simple = date_obj.strftime("%Y-%m-%d")
                dates.append(date_simple)

            if not data["resultats"] or "resultats" not in data:
                logger.info(f"Erreur département : {i}")
                break

            departement += len(data["resultats"])
            total += departement

            pages +=150
            time.sleep(0.2)

        logger.info(f"nombre d'offres pour le departement {i} : {departement}")
    logger.info(f"Nombre total d'offres M18: {total}")
    return total, dates

total, dates = get_offres()

dates_series = pd.to_datetime(dates)
print(dates_series)
ax = sns.histplot(dates_series)
ax.set_title("Distribution des offres d'emploi M18 par date de création")
ax.set_xlabel("date de création de l'offre")
ax.set_ylabel("nombre d'offres")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.close()


