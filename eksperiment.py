# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 17:57:46 2025

"""

import os
import csv
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'


# 1️  KONFIGURASJON

folder_path = "EksperimentData"

# Finn alle CSV-filer
csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
if not csv_files:
    print("🚫 Ingen CSV-filer funnet i:", folder_path)
    raise SystemExit
else:
    print(f"📂 Fant {len(csv_files)} CSV-filer i {folder_path}\n")


# 2️  HJELPEVARIABLER

per_interface = {}
total_rows = 0


# 3️ LES OG HENT UT DATA

for file_name in csv_files:
    file_path = os.path.join(folder_path, file_name)
    print(f"🔹 Leser {file_name}")

    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            header = [h.strip().lower() for h in header]

            # Sjekk at kolonnene finnes
            if not {"interface", "time_s", "accuracy"}.issubset(header):
                print(f"⚠️ Hopper over {file_name} (mangler kolonner: {header})")
                continue

            i_interface = header.index("interface")
            i_time = header.index("time_s")
            i_acc = header.index("accuracy")

            for row in csv_reader:
                if len(row) < max(i_interface, i_time, i_acc) + 1:
                    continue

                interface = row[i_interface].strip().lower()
                try:
                    time_s = float(row[i_time].replace(",", "."))
                    acc = float(row[i_acc].replace(",", "."))
                except ValueError:
                    continue

                if interface not in per_interface:
                    per_interface[interface] = {"times": [], "acc": []}

                per_interface[interface]["times"].append(time_s)
                per_interface[interface]["acc"].append(acc)
                total_rows += 1

    except Exception as e:
        print(f"⚠️ Feil ved lesing av {file_name}: {e}")

print(f"\n📊 Totalt {total_rows} gyldige oppgaver lest.\n")


# 4️ BEREGN GJENNOMSNITT

summary = []
for interface, vals in per_interface.items():
    if not vals["times"] or not vals["acc"]:
        continue
    avg_time = sum(vals["times"]) / len(vals["times"])
    avg_acc = sum(vals["acc"]) / len(vals["acc"])
    summary.append((interface.capitalize(), avg_time, avg_acc))

if not summary:
    print("🚫 Ingen gyldige data å analysere.")
    raise SystemExit

print("🧭 Oppsummering per metode:\n")
for interface, avg_time, avg_acc in summary:
    print(f"{interface:10s} ⏱️ {avg_time:.2f} sek  🎯 {avg_acc:.2f}%")

# 5️ VIS GRAFER (Plotly)

interfaces = [s[0] for s in summary]
avg_times = [s[1] for s in summary]
avg_accs = [s[2] for s in summary]

# Gjennomsnittlig tid
fig1 = px.bar(
    x=interfaces, y=avg_times, color=interfaces,
    text=[f"{v:.2f}s" for v in avg_times],
    title="⏱️ Gjennomsnittlig tid per metode",
    labels={"x": "Inndatametode", "y": "Tid (sekunder)"}
)
fig1.update_traces(textposition="outside", hovertemplate="%{x}<br>%{y:.2f} sek")
fig1.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
fig1.show()

# Gjennomsnittlig nøyaktighet
fig2 = px.bar(
    x=interfaces, y=avg_accs, color=interfaces,
    text=[f"{v:.2f}%" for v in avg_accs],
    title="🎯 Gjennomsnittlig nøyaktighet per metode",
    labels={"x": "Inndatametode", "y": "Nøyaktighet (%)"}
)
fig2.update_traces(textposition="outside", hovertemplate="%{x}<br>%{y:.2f}%")
fig2.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
fig2.show()

# Kombinert graf (tid + nøyaktighet)
fig3 = px.bar(
    x=interfaces, y=avg_times, color=interfaces,
    title="🧩 Tid og nøyaktighet per metode"
)
fig3.add_scatter(
    x=interfaces, y=avg_accs, mode="lines+markers",
    name="Nøyaktighet (%)", yaxis="y2"
)
fig3.update_layout(
    yaxis=dict(title="Tid (sekunder)"),
    yaxis2=dict(title="Nøyaktighet (%)", overlaying="y", side="right"),
    legend=dict(x=0.8, y=1)
)
fig3.show()
