SAMPLE_DATA_DDL_QUERY = """
    CREATE TABLE IF NOT EXISTS sample_data (
        sample_data_id BIGINT(20) PRIMARY KEY AUTO_INCREMENT,
        transacted_date TIMESTAMP NOT NULL,
        ticker VARCHAR(255) NOT NULL,
        open_price FLOAT(32) NOT NULL,
        high_price FLOAT(32) NOT NULL,
        low_price FLOAT(32) NOT NULL,
        close_price FLOAT(32) NOT NULL,
        trade_volume FLOAT(32) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	    KEY (transacted_date),
	    KEY (ticker),
        KEY (created_at),
	    KEY (updated_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

INSERT_SAMPLE_DATA_QUERY = """
    INSERT INTO sample_data (
        transacted_date, 
        ticker, 
        open_price,
        high_price,
        low_price,
        close_price,
        trade_volume
    ) VALUES (
        '{transacted_date}',
        '{ticker}', 
        {open_price},
        {high_price},
        {low_price},
        {close_price},
        {trade_volume}
    )
"""

SELECT_DATA_BY_TICKER = """
	SELECT
	    transacted_date
	    , open_price
	    , high_price
	    , low_price
	    , close_price
	    , trade_volume
	FROM sample_data 
	WHERE ticker = '{ticker}' 
	ORDER BY transacted_date
"""

SELECT_ALL_TICKERS = """
	SELECT
	    ticker
	FROM sample_data
	GROUP BY ticker
"""