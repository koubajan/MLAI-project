<br />
<div align="center">
  <h1 align="center">📈 <b>AI Project: Bitcoin Price Prediction (Phase 1)</b> 📈</h1>
  <p align="center">
    <i>Školní ročníkový projekt aplikované AI a strojového učení (Sběrová & Analytická Fáze)</i>
    <br />
    <br />
  </p>
</div>

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Data Source](https://img.shields.io/badge/Data_API-Binance_REST-yellow?style=for-the-badge&logo=binance&logoColor=black)
![Pandas](https://img.shields.io/badge/Data_Processing-Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

---

## 🚀 O Projektu

Tento repozitář obsahuje **Fázi 1** uceleného AI projektu pro odhad cílové prodejní ceny tržního aktiva (v tomto případě kryptoměny Bitcoin). 

Zadáním práce bylo sestavit projekt pro trénování umělé inteligence tak, aby byl zcela **nezávislý na generických a předpřibravených datech** dostupných veřejně (např. platformy Kaggle nebo databáze Iris). Data proto získáváme živě od poskytovatele formou API komunikace a posléze z nich extrahujeme potřebné suroviny pro naši budoucí síť, případně klasifikátor / regresi.

Záměrem první fáze je dokázat funkční cyklus *Data Mining* $\rightarrow$ *Pre-processing* $\rightarrow$ *Persistent Storage*.

---

## 📊 Zdroj a Struktura Dat (API)

Aplikace neshromažďuje data nelegálním "crawlingem" (html scraping bez svolení majitele DOM). Místo toho se dotazuje bezplatného, veřejně otevřeného [Binance REST API v3](https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data).

**Charakteristika získaných dat:**
*   **Velikost:** Minimálně garantovaných **2000 unikátních záznamů** (denní svíčky).
*   **Atributy:** Z celkového JSON dumpu je datovým procesorem vyseparováno nadstandardních **5 požadovaných analytických atributů pro regresní trénink**: 
    1.  Otevírací denní cena (`Open`)
    2.  Maximální denní cena (`High`)
    3.  Minimální denní cena (`Low`)
    4.  Uzavírací denní cena (`Close`)
    5.  Zobchodovaný denní objem mincí (`Volume`)

---

## ⚙️  Soubory repozitáře a Prerekvizity

### <code>data_scraping/binance_scraper.py</code>
Stěžejní komponenta první fáze projektu. Python program je navržen tak, aby obešel hardcordovaný limit 1000 řádků od poskytovatele. Dokáže cyklit a posouvat časová okna přes Timestampy napříč dlouhými lety do minulosti.

### <code>data/btc_raw_data.csv</code>
Surová výstupní databáze po zpracování knihovnou *[Pandas](https://pandas.pydata.org/)*. Tyto uložené informace v sobě obsahují časovou řadu (Time Series) bitcoinu ze všech předchozích cyklů API a neobsahují složitá vnoření do slovníků na rozdíl od originálního JSON formátu. 

> [!NOTE] 
> Pokud ve složce `data` soubor není, můžete ho pro svou potřebu vygenerovat příkazem přes Python konzoli, viz níže.

---

## 🛠 Jak zkompilovat Phase 1 na vlastním PC

Instalace celého nástroje v rámci Fáze 1 se skládá ze tří lehkých kroků postavených čistě na systémovém CLI:

**1. Vytvoření virtuálního prostředí a instalace balíčků:**
Ujišťujeme se tak, že nezašpiníme Váš globální python cache. Závislosti tlouští pouze dvě kritické knihovny a nacházejí se v dokumentu `requirements.txt`.
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**2. Příkaz ke spuštění stahovací sekvence:**
```bash
python data_scraping/binance_scraper.py
```

*Výstup na konzoli bude zhruba následovný:*
```text
Stahování dat pro BTCUSDT, interval 1d...
Staženo 1000 záznamů. Původ nejstaršího záznamu z dávky: 2021-06-25
Staženo 2000 záznamů. Původ nejstaršího záznamu z dávky: 2018-09-29

Tabulka vytvořena. Počet záznamů: 2000
        Date     Open     High      Low    Close       Volume  
0 2018-09-29  6600.86  6638.99  6444.02  6529.56  24255.48512
...
```

**3. Kontrola formátu CSV tabulek:**
Výsledek bude úspěšně vyexportován uvnitř repozitáře v podadresáři `data/` pro pozdější trénování a testovací cyklus sítě, případně libovolného Decision Tree stromu / Neural Network vrstvy ve **Fázi 2**.

---
<div align="center">
  <i>Tato repozitářová větev je zamčena pouze pro pre-procesovou datovou složku za účelem hodnocení částí PV Projektů na vrstvě dolování (Data Mining).</i>
</div>
