import os
import threading
import requests
import tqdm
import pandas as pd


def main(df, print_p_bar):
	for row in (tqdm.tqdm(df.itertuples(), total=len(df)) if print_p_bar else df.itertuples()):
		res = requests.post(
			"http://3.35.197.182:8000/insert_row",
			json={
				"transacted_date": getattr(row, "Date"),
				"ticker": getattr(row, "Ticker"),
				"open_price": getattr(row, "Ticker"),
				"high_price": getattr(row, "High"),
				"low_price": getattr(row, "Low"),
				"close_price": getattr(row, "Close"),
				"trade_volume": getattr(row, "Volume"),
			},
		)
		res.raise_for_status()
		print(res.text)


if __name__ == "__main__":
	df = pd.read_csv("./crypto_ohlcv.csv")
	num_threads: int = int(os.cpu_count())
	threads = []
	for i, df_part_start_idx in enumerate(range(0, len(df), len(df) // num_threads)):
		df_partition = df.iloc[df_part_start_idx: df_part_start_idx + len(df) // num_threads]
		threads.append(threading.Thread(target=main, args=(df_partition, i == 0)))
	# start threads
	for _thread in threads:
		_thread.start()
	for _thread in threads:
		_thread.join()