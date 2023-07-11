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
		if len(rows_to_send) == 1000:
			res = requests.post(
				"http://3.35.197.182:8000/insert_row",
				json={"rows": rows_to_send},
			)
			res.raise_for_status()
			rows_to_send.clear()
	res = requests.post(
		"http://3.35.197.182:8000/insert_row",
		json={"rows": rows_to_send},
	)
	res.raise_for_status()