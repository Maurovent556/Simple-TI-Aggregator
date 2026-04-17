#  Simple TI Aggregator (OSINT)

Un tool in Python leggero e automatizzato per raccogliere, filtrare e arricchire Indicatori di Compromissione (IoC) sfruttando fonti OSINT gratuite.

##  Scopo del Progetto
Questo progetto è stato sviluppato come Proof of Concept (PoC) durante il mio stage per automatizzare il processo di Threat Intelligence. Estrae gli IP legati alle campagne malevole più recenti, elimina i duplicati e ne verifica l'effettiva pericolosità incrociando i dati di due provider diversi.

##  Funzionalità
* **Estrazione:** Recupera le ultime campagne (Pulses) da AlienVault OTX.
* **Deduplicazione:** Isola solo gli indirizzi IPv4 e rimuove i doppioni.
* **Arricchimento:** Interroga l'API di AbuseIPDB per ottenere l'Abuse Confidence Score, la nazione e l'ISP dell'IP sospetto.
* **Reportistica:** Genera automaticamente un file CSV pronto per essere analizzato o importato su un SIEM/Firewall.

## Prerequisiti
Per utilizzare questo script è necessario avere Python 3.8+ e le seguenti API Keys gratuite:
* [AlienVault OTX Account](https://otx.alienvault.com/)
* [AbuseIPDB Account](https://www.abuseipdb.com/)

##  Installazione e Utilizzo

1. Clona la repository:
   ```bash
   git clone [https://github.com/tuo-username/Simple-TI-Aggregator.git](https://github.com/tuo-username/Simple-TI-Aggregator.git)
