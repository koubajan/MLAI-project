<div align="center">
  <h1 align="center">Odhad ceny Bitcoinu - Fáze 1 (Sběr dat)</h1>
</div>

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Data Source](https://img.shields.io/badge/Data_API-Binance_REST-yellow?style=for-the-badge&logo=binance&logoColor=black)
![Pandas](https://img.shields.io/badge/Data_Processing-Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

---

Tento repozitář představuje první část ročníkového softwarového projektu. Cílem této úvodní fáze je vytvoření vlastního, nezávislého datasetu pro následné trénování modelu strojového učení, a to extrakcí reálných tržních dat.

Projekt v této fázi neobsahuje předpřipravené datasety (jako např. z portálu Kaggle), ale implementuje vlastní proces získávání dat přes veřejné aplikační rozhraní obchodní burzy Binance.

## Zdroj a podoba dat

Zdrojem dat je oficiální a volně dostupné [Binance REST API](https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data). Volání probíhá bez nutnosti autentizace nebo API klíčů.

Sběr je zaměřen na denní obchodní svíčky měnového páru `BTC/USDT`. Skript stahuje minimálně 2 000 po sobě jdoucích záznamů, přičemž překonává limit 1 000 záznamů na jeden API dotaz automatickým zřetězením požadavků do minulosti podle časového razítka posledního staženého bloku.

**Z každého záznamu je extrahováno pět sledovaných atributů:**
- Otevírací cena (Open)
- Maximální cena (High)
- Minimální cena (Low)
- Zavírací cena (Close)
- Objem obchodů (Volume)

## Struktura souborů

- `data_scraping/binance_scraper.py` - Hlavní skript v jazyce Python obstarávající komunikaci s API, stránkování a uložení nezpracovaných dat.
- `data/btc_raw_data.csv` - Datový soubor ve formátu CSV generovaný knihovnou Pandas na základě výstupu scraperu. Představuje základnu pro další datovou transformaci.
- `requirements.txt` - Seznam prerekvizit a knihoven jazyka Python určený pro instalatér balíčků `pip`. Dvě hlavní závislosti jsou knihovny `requests` a `pandas`.

## Lokální spuštění

Ke stažení a kompilaci vlastního CSV souboru přímo pomocí zdrojového kódu postačí několik příkazů na příkazové řádce:

1. Vytvoření uzavřeného virtuálního prostředí (doporučeno):
```bash
python -m venv venv
venv\Scripts\activate
```

2. Instalace závislostí:
```bash
pip install -r requirements.txt
```

3. Spuštění stahování:
```bash
python data_scraping/binance_scraper.py
```

Skript po dokončení stáhne a rozčlení požadovaný počet záznamů a potvrdí vytvoření dokumentu CSV uvnitř domovského repozitáře. Data jsou pak plně nachystána ke vstupu do další vývojové fáze.
