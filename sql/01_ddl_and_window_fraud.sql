
CREATE TABLE raw_transactions (
    transaction_id UUID PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    merchant_id VARCHAR(100) NOT NULL,
    amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    currency CHAR(3) NOT NULL CHECK (char_length(currency) = 3),
    ip_address INET NOT NULL,
    device_id VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(50),
    event_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    user_id VARCHAR(100) PRIMARY KEY,
    home_country VARCHAR(50) NOT NULL,
    credit_limit NUMERIC(12, 2) NOT NULL CHECK (credit_limit >= 0),
    account_status VARCHAR(20) NOT NULL CHECK (account_status IN ('ACTIVE', 'FROZEN', 'CLOSED')),
    avg_30d_spend NUMERIC(12, 2) DEFAULT 0
);

CREATE TABLE merchants (
    merchant_id VARCHAR(100) PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL
);


CREATE TABLE ip_blacklist (
    ip_address INET PRIMARY KEY,
    threat_score INTEGER NOT NULL CHECK (threat_score > 0 AND threat_score <= 100),
    added_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fx_rates (
    currency CHAR(3) PRIMARY KEY,
    rate_to_usd NUMERIC(12, 6) NOT NULL CHECK (rate_to_usd > 0),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

SELECT 
    transaction_id, 
    user_id, 
    amount,
    COUNT(transaction_id) OVER (
        PARTITION BY user_id 
        ORDER BY event_timestamp 
        RANGE BETWEEN INTERVAL '10 minutes' PRECEDING AND CURRENT ROW
    ) AS recent_swipe_count
FROM raw_transactions;


WITH location_deltas AS (
    SELECT 
        transaction_id, 
        user_id, 
        city,
        country,
        event_timestamp,
        LAG(city, 1) OVER (PARTITION BY user_id ORDER BY event_timestamp) AS prev_city,
        LAG(country, 1) OVER (PARTITION BY user_id ORDER BY event_timestamp) AS prev_country,
        EXTRACT(EPOCH FROM (
            event_timestamp - LAG(event_timestamp, 1) OVER (
                PARTITION BY user_id ORDER BY event_timestamp
            )
        )) AS seconds_since_last_swipe
    FROM raw_transactions
)
SELECT * 
FROM location_deltas 
WHERE seconds_since_last_swipe < 300 
  AND city != prev_city               
  AND prev_city IS NOT NULL;

WITH usd_normalized_swipes AS (
    SELECT 
        rt.transaction_id,
        rt.user_id,
        rt.currency,
        rt.event_timestamp,
        (rt.amount * fx.rate_to_usd) AS amount_usd
    FROM raw_transactions rt
    JOIN fx_rates fx ON rt.currency = fx.currency
)
SELECT 
    user_id,
    COUNT(DISTINCT currency) AS unique_currencies_used,
    SUM(amount_usd) AS total_usd_volume,
    MIN(event_timestamp) AS burst_start,
    MAX(event_timestamp) AS burst_end
FROM usd_normalized_swipes
GROUP BY user_id
HAVING COUNT(DISTINCT currency) >= 3 
   AND SUM(amount_usd) > 5000
   AND EXTRACT(EPOCH FROM (MAX(event_timestamp) - MIN(event_timestamp))) <= 600; 