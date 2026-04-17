import requests
import csv
from datetime import datetime

# 1. Le tue chiavi di accesso
OTX_API_KEY = "INSERISCI_QUI_LA_TUA_CHIAVE_ALIENVAULT"
ABUSE_API_KEY = "INSERISCI_QUI_LA_TUA_CHIAVE_ABUSEIPDB"

# Setup per il file CSV
nome_file_csv = "report_minacce.csv"
data_odierna = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- PARTE 1: ESTRAZIONE DA ALIENVAULT ---
url_otx = "https://otx.alienvault.com/api/v1/pulses/subscribed?limit=10"
headers_otx = {"X-OTX-API-KEY": OTX_API_KEY}

ip_malevoli_unici = set()

print("1. Scaricamento IP da AlienVault in corso...")
response_otx = requests.get(url_otx, headers=headers_otx)

if response_otx.status_code == 200:
    dati = response_otx.json()
    for pulse in dati.get("results", []):
        for indicatore in pulse.get("indicators", []):
            if indicatore.get("type") == "IPv4":
                ip_malevoli_unici.add(indicatore.get("indicator"))

    lista_ip = list(ip_malevoli_unici)
    print(f"✅ Trovati {len(lista_ip)} IP unici.\n")

    # --- PARTE 2: ARRICCHIMENTO E SALVATAGGIO ---
    print("2. Arricchimento dati e generazione del file CSV in corso...")
    url_abuse = "https://api.abuseipdb.com/api/v2/check"
    headers_abuse = {'Accept': 'application/json', 'Key': ABUSE_API_KEY}

    # Apriamo un file CSV e prepariamoci a scrivere
    with open(nome_file_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')  # Usiamo il punto e virgola per separare le colonne
        # Scriviamo la riga di intestazione (i titoli delle colonne)
        writer.writerow(["Data Rilevamento", "Indirizzo IP", "Punteggio AbuseIPDB", "Nazione", "ISP"])

        # Ora passiamo tutti gli IP al setaccio
        for ip in lista_ip:
            parametri = {'ipAddress': ip, 'maxAgeInDays': '90'}
            response_abuse = requests.get(url_abuse, headers=headers_abuse, params=parametri)

            if response_abuse.status_code == 200:
                dati_abuse = response_abuse.json()['data']
                score = dati_abuse['abuseConfidenceScore']
                nazione = dati_abuse['countryCode']
                isp = dati_abuse['isp']

                # Scriviamo i dati di questo IP nel file CSV!
                writer.writerow([data_odierna, ip, f"{score}%", nazione, isp])
            else:
                writer.writerow([data_odierna, ip, "Errore API", "N/A", "N/A"])

    print(f"🎉 Finito! È stato creato il file: {nome_file_csv}")
    print("Aprilo dal pannello di sinistra di PyCharm o dalla cartella del tuo computer.")

else:
    print("❌ Errore durante la connessione ad AlienVault.")