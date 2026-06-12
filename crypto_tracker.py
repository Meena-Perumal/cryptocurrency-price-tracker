from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import pandas as pd
import os
import time

# Open Chrome
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

# Open CoinMarketCap
driver.get("https://coinmarketcap.com")

# Wait for page loading
time.sleep(10)

# Get rows
rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

crypto_data = []

# Current Date
today = datetime.now().strftime("%Y-%m-%d")

# Top 10 Coins
for row in rows[:10]:

    cols = row.find_elements(By.TAG_NAME, "td")

    if len(cols) > 7:

        coin_name = cols[2].text
        price = cols[3].text
        change_24h = cols[4].text
        market_cap = cols[7].text

        crypto_data.append([
            today,
            coin_name,
            price,
            change_24h,
            market_cap
        ])

driver.quit()

# DataFrame
df = pd.DataFrame(
    crypto_data,
    columns=[
        "Date",
        "Coin Name",
        "Price",
        "24h Change",
        "Market Cap"
    ]
)

# Excel History File
file_name = "crypto_history.xlsx"

# If file exists, append new data
if os.path.exists(file_name):

    old_data = pd.read_excel(file_name)

    updated_data = pd.concat(
        [old_data, df],
        ignore_index=True
    )

    updated_data.to_excel(
        file_name,
        index=False
    )

else:

    df.to_excel(
        file_name,
        index=False
    )

print("Data Saved Successfully!")
print("File Name: crypto_history.xlsx")

input("Press Enter to Close...")