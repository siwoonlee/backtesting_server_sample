import time
import requests
import tqdm
import pandas as pd


if __name__ == "__main__":
	df = pd.read_csv("./crypto_ohlcv.csv")
	rows_to_send = []
	for row in tqdm.tqdm(df.itertuples(), total=len(df)):
		rows_to_send.append(
			{
				"transacted_date": getattr(row, "Date"),
				"ticker": getattr(row, "Ticker"),
				"open_price": getattr(row, "Open"),
				"high_price": getattr(row, "High"),
				"low_price": getattr(row, "Low"),
				"close_price": getattr(row, "Close"),
				"trade_volume": getattr(row, "Volume"),
			}
		)
		if len(rows_to_send) == 200:
			res = requests.post(
				"http://3.38.137.102:8000/insert_row",
				json={"rows": rows_to_send},
			)
			res.raise_for_status()
			rows_to_send.clear()
			time.sleep(0.05)  # AWS t3.micro instance needs cooling time
	res = requests.post(
		"http://3.38.137.102:8000/insert_row",
		json={"rows": rows_to_send},
	)
	res.raise_for_status()