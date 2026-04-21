import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates

ensemble = pd.read_excel('data/series_offres_difusees_T32025.xlsx', sheet_name=None)
total = ensemble["Total"]
contrat = ensemble["Contrat"]
metier = ensemble["Metier"]


total["Mois"] = total["Mois"].astype(str)
total["Mois"].dtypes

total["Année"] = total["Année"].astype(str)
total["Année"].dtypes

total["Date"] = pd.to_datetime(dict(
    year=total["Année"],
    month=total["Mois"],
    day=1)
)
total


total[total["Année"]>"2020"]

total["Semestre"] = total["Trimestre"]
total["Semestre"] =total["Semestre"].apply(lambda x: "S1" if x=="T1" or x=="T2" else "S2")

base = total[total["Date"] == pd.Timestamp("2021-01-01")]["Nombre d'offres diffusées"].values[0]
print(base)

total["index"] = total["Nombre d'offres diffusées"] / base * 100

# plot
plt.figure()
plt.plot(total[total["Date"] >= pd.Timestamp("2021-01-01")]["Date"], 
         total[total["Date"] >= pd.Timestamp("2021-01-01")]["index"])

plt.title("Offres d'emploi en France (Index 100 en Janvier 2021)")
plt.xlabel("Date")
plt.ylabel("Index")
plt.grid()
plt.gca().xaxis.set_major_locator(dates.MonthLocator(interval=6))
plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m'))
plt.show()

# total.groupby("Année")["Nombre d'offres diffusées"].sum().plot(kind='bar')
# plt.title("Nombre d'offres diffusées par année")
# plt.xlabel("Année")
# plt.ylabel("Nombre d'offres diffusées") 
# plt.show()