# Scaper_Imran
# 🗳️ Scraper volebních výsledků – Okres Prostějov (PS 2017)

Tento Python skript stahuje volební výsledky Parlamentních voleb 2017 pro jednotlivé obce okresu Prostějov z oficiálního webu [volby.cz](https://www.volby.cz).

Výstupem je CSV soubor s detailními výsledky hlasování v jednotlivých obcích, včetně počtu hlasů pro každou politickou stranu.

---

## 📦 Instalace knihoven

Před prvním spuštěním je potřeba nainstalovat závislosti pomocí `pip`:

```bash
pip install -r requirements.txt
```

**Obsah souboru `requirements.txt`:**
```txt
beautifulsoup4==4.13.4
bs4==0.0.2
certifi==2025.4.26
charset-normalizer==3.4.2
idna==3.10
requests==2.32.4
soupsieve==2.7
typing_extensions==4.14.0
urllib3==2.4.0
```

---

## ▶️ Spuštění skriptu

Skript se spouští přes příkazovou řádku:

```bash
python Scaper_Imran.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky.csv
```

### Argumenty:
- První argument: URL na seznam obcí (okres Prostějov).
- Druhý argument: Název výstupního CSV souboru. (Přípona `.csv` bude automaticky přidána, pokud není zadána.)

---

## 💾 Výstup

Výstupní CSV obsahuje:
- číslo a název každé obce,
- počet voličů,
- počet vydaných obálek,
- počet platných hlasů,
- počet hlasů pro každou politickou stranu v dané obci.

### Ukázka výstupu (`vysledky.csv`):

| Cislo Obce | Nazev Obce | Pocet Volicu | Pocet Obalek | Pocet Validnich Obalek | ANO 2011 | ODS | ... |
|------------|-------------|----------------|----------------|--------------------------|-----------|------|------|
| 590849     | Biskupice   | 472            | 311            | 308                      | 105       | 45   | ...  |

---

## 🛠️ Požadavky

- Python 3.7 nebo novější
- Internetové připojení

---

## 👤 Autor

**Jméno:** Imran Shirvanov  
**Email:** vertimop@seznam.cz  
**Discord:** -------
