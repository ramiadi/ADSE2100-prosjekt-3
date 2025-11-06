# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 17:35:31 2025

@author: ramin
"""
import pandas as pd
import os
import re

folder_path = "EksperimentData"

# ✨ 1. Finn alle CSV-filer i mappen
csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

if not csv_files:
    print("Ingen CSV-filer funnet i EksperimentData.")
    raise SystemExit

# ✨ 2. Les og slå sammen alle CSV-filer til én dataframe
frames = []
for file_name in csv_files:
    file_path = os.path.join(folder_path, file_name)
    df = pd.read_csv(file_path)
    frames.append(df)

df_all = pd.concat(frames, ignore_index=True)

# ✨ 3. Funksjon for å hente q1 og q2
def extract_q(text, key):
    match = re.search(rf"{key}:(\d+)", str(text))
    return int(match.group(1)) if match else None

# ✨ 4. Ekstraher q1 (fornøydhet) og q2 (anstrengelse)
df_all["fornoyd"] = df_all["task"].apply(lambda x: extract_q(x, "q1"))
df_all["anstrengelse"] = df_all["task"].apply(lambda x: extract_q(x, "q2"))

# ✨ 5. Filtrer questionnaire-rader
if "taskType" in df_all.columns:
    df_q = df_all[df_all["taskType"].str.lower() == "questionnaire"]
elif "tasktype" in df_all.columns:
    df_q = df_all[df_all["tasktype"].str.lower() == "questionnaire"]
else:
    print("Ingen taskType/tasktype-kolonne funnet.")
    raise SystemExit

# ✨ 6. Normaliser interface til lowercase
df_q["interface"] = df_q["interface"].str.lower()

# ✨ 7. Gruppér per interface og regn gjennomsnitt
resultat = df_q.groupby("interface")[["fornoyd", "anstrengelse"]].mean()

# ✨ 8. PENT UTSKRIFT FOR RAPPORTEN
print("\n🧠 Gjennomsnittlig fornøydhet og anstrengelse per metode:\n")

navn = {
    "keyboard": "Tastatur",
    "voice": "Tale",
    "touch": "Berøring"
}

for interface, row in resultat.iterrows():
    print(f"{navn.get(interface, interface.capitalize())}:")
    print(f"  😀 Fornøydhet: {row['fornoyd']:.2f} / 5")
    print(f"  💪 Anstrengelse: {row['anstrengelse']:.2f} / 5\n")



