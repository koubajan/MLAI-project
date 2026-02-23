import requests
import pandas as pd
import datetime
import time
import os

# Konfigurace pro Binance API
SYMBOL = "BTCUSDT"
INTERVAL = "1d"  # Denní svíčky
LIMIT = 1000  # Binance API dovoluje max 1000 záznamů na jeden request
API_URL = "https://api.binance.com/api/v3/klines"

def fetch_binance_data(symbol, interval, limit, total_records):
    """
    Stáhne historická data z Binance. Protože limit je 1000, budeme stránkovat
    do minulosti, dokud nenasbíráme požadovaný počet záznamů (total_records).
    """
    print(f"Stahování dat pro {symbol}, interval {interval}...")
    
    all_klines = []
    end_time = int(time.time() * 1000)  # Aktuální čas v milisekundách
    
    while len(all_klines) < total_records:
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
            "endTime": end_time
        }
        
        response = requests.get(API_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if not data:
                break # Žádná další data nejsou k dispozici
                
            # Přidáme data do celkového seznamu (z nejnovějších k nejstarším)
            all_klines = data + all_klines
            
            # Nastavíme endTime pro další iteraci na začátek nejstarší svíčky ze současné dávky minus 1 ms
            end_time = data[0][0] - 1
            
            print(f"Staženo {len(all_klines)} záznamů. Původ nejstaršího záznamu z dávky: {datetime.datetime.fromtimestamp(data[0][0]/1000).strftime('%Y-%m-%d')}")
            time.sleep(0.5) # Ochrana proti rate-limitingu
        else:
            print(f"Chyba při komunikaci s API: {response.text}")
            break
            
    # Odřízneme data na přesný požadovaný počet, pokud jsme jich stáhli příliš mnoho
    if len(all_klines) > total_records:
        all_klines = all_klines[-total_records:]
        
    return all_klines

def process_data(raw_klines):
    """
    Zpracuje syrová data z Binance do Pandas DataFrame.
    """
    # Sloupce definované dokumentací Binance API
    columns = [
        "Open_time", "Open", "High", "Low", "Close", "Volume",
        "Close_time", "Quote_asset_volume", "Number_of_trades",
        "Taker_buy_base_asset_volume", "Taker_buy_quote_asset_volume", "Ignore"
    ]
    
    df = pd.DataFrame(raw_klines, columns=columns)
    
    # Vybereme jen to, co nás zajímá (zde je min 5 atributů, které požaduje zadání!)
    df = df[["Open_time", "Open", "High", "Low", "Close", "Volume"]]
    
    # Přetypování dat
    df["Open"] = df["Open"].astype(float)
    df["High"] = df["High"].astype(float)
    df["Low"] = df["Low"].astype(float)
    df["Close"] = df["Close"].astype(float)
    df["Volume"] = df["Volume"].astype(float)
    
    # Konverze času
    df["Date"] = pd.to_datetime(df["Open_time"], unit='ms')
    df.drop("Open_time", axis=1, inplace=True)
    
    # Nastavení data jako prvního sloupce pro přehlednost
    cols = ['Date'] + [col for col in df if col != 'Date']
    df = df[cols]
    
    return df

def main():
    # Požadavek: Minimálně 1500 záznamů. Stáhneme jich 2000 (cca posledních 5,5 let)
    TOTAL_REQUESTED = 2000 
    
    klines = fetch_binance_data(SYMBOL, INTERVAL, LIMIT, TOTAL_REQUESTED)
    
    if klines:
        df = process_data(klines)
        print(f"\nTabulka vytvořena. Počet záznamů: {len(df)}")
        print(df.head())
        
        # Zajištění existence složky 'data'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        data_dir = os.path.join(project_root, "data")
        os.makedirs(data_dir, exist_ok=True)
        
        file_path = os.path.join(data_dir, "btc_raw_data.csv")
        df.to_csv(file_path, index=False)
        print(f"\nData úspěšně uložena do: {file_path}")
        print("Tímto je doloženo odkud data pochází (automatický sběr z Binance API) dle podmínek zadání projektu.")
    else:
        print("Nepodařilo se stáhnout žádná data.")

if __name__ == "__main__":
    main()
