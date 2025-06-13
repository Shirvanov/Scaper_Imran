"""
Scaper_Imran.py: WebScaper volby Prostějov

author: Imran Shirvanov
email: vertimop@seznam.cz
discord: -------
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys

obce_data = []
vysledky_stran = []
nazvy_stran_set = set()

def ziskat_data_z_url(url):
    odpoved = requests.get(url)
    return BeautifulSoup(odpoved.text, "html.parser")

def stahni_seznam_obci(hlavni_url):
    soup = ziskat_data_z_url(hlavni_url)
    cisla = [td.text for td in soup.find_all("td", class_="cislo")]
    nazvy = [td.text for td in soup.find_all("td", class_="overflow_name")]
    return list(zip(cisla, nazvy))

def stahni_podrobnosti_obce(kod_obce):
    detail_url = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec={kod_obce}&xvyber=7103"
    soup = ziskat_data_z_url(detail_url)

    volici = soup.find("td", class_="cislo", headers="sa2")
    obalky = soup.find("td", class_="cislo", headers="sa5")
    platne = soup.find("td", class_="cislo", headers="sa6")

    volici_text = volici.text.replace('\xa0', ' ') if volici else "N/A"
    obalky_text = obalky.text.replace('\xa0', ' ') if obalky else "N/A"
    platne_text = platne.text.replace('\xa0', ' ') if platne else "N/A"

    return volici_text, obalky_text, platne_text, soup

def extrahuj_vysledky_stran(soup):
    vysledky = {}

    tabulky = [
        ("t1sa1 t1sb2", "t1sa2 t1sb3"),
        ("t2sa1 t2sb2", "t2sa2 t2sb3")
    ]

    for hlavy, hlasy in tabulky:
        jmena = soup.find_all("td", class_="overflow_name", headers=hlavy)
        pocty = soup.find_all("td", class_="cislo", headers=hlasy)

        for j, jmeno in enumerate(jmena):
            nazev = jmeno.text.strip()
            hlasu = pocty[j].text.replace('\xa0', ' ') if j < len(pocty) else "N/A"
            vysledky[nazev] = hlasu
            nazvy_stran_set.add(nazev)

    return vysledky

def uloz_do_csv(nazev_souboru):
    hlavicky = ["Cislo Obce", "Nazev Obce", "Pocet Volicu", "Pocet Obalek", "Pocet Validnich Obalek"]
    hlavicky.extend(sorted(nazvy_stran_set))

    try:
        with open(nazev_souboru, mode="w", encoding="utf-8", newline="") as vystup:
            zapisovac = csv.DictWriter(vystup, fieldnames=hlavicky, restval="0")
            zapisovac.writeheader()

            for idx, obec in enumerate(obce_data):
                zaznam = {
                    "Cislo Obce": obec["kod"],
                    "Nazev Obce": obec["nazev"],
                    "Pocet Volicu": obec["volici"],
                    "Pocet Obalek": obec["obalky"],
                    "Pocet Validnich Obalek": obec["platne"]
                }

                zaznam.update(vysledky_stran[idx])
                zapisovac.writerow(zaznam)

        print(f"\nVýsledky úspěšně zapsány do souboru: {nazev_souboru}")

    except Exception as chyba:
        print(f"Chyba při zápisu do souboru: {chyba}")

def main():
    if len(sys.argv) != 3:
        print("Použití: python skript.py <url> <soubor.csv>")
        return

    vstupni_url = sys.argv[1]
    vystupni_csv = sys.argv[2]

    if not vystupni_csv.endswith(".csv"):
        vystupni_csv += ".csv"

    seznam_obci = stahni_seznam_obci(vstupni_url)

    for poradi, (kod, jmeno) in enumerate(seznam_obci, start=1):
        print(f"({poradi}) Zpracovávám: {kod} - {jmeno}")
        volici, obalky, platne, soup_detail = stahni_podrobnosti_obce(kod)
        vysledky = extrahuj_vysledky_stran(soup_detail)

        obce_data.append({
            "kod": kod,
            "nazev": jmeno,
            "volici": volici,
            "obalky": obalky,
            "platne": platne
        })

        vysledky_stran.append(vysledky)

    uloz_do_csv(vystupni_csv)

if __name__ == "__main__":
    main()
