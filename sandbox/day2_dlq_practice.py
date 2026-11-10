from time import timezone
from datetime import datetime,timezone
import logging
from src.pyclass import Transaction
import json
from pydantic import ValidationError
from pathlib import Path

sample_records = [
    # 1. Valid Transaction Record
    {
        "transaction_id": "550e8400-e29b-41d4-a716-446655440000",
        "user_id": "user_12",
        "event_timestamp": "2026-11-10T14:30:00+00:00",
        "merchant": {
            "merchant_id": "merchant_5",
            "category": "Swiggy",
            "city": "Chennai",
            "country": "IN"
        },
        "device": {
            "ip_address": "192.168.1.101",
            "device_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
        },
        "amount": 2450.75,
        "currency": "INR",
        "location": {
            "latitude": 13.0827,
            "longitude": 80.2707
        },
        "channel": "pos_chip",
        "action": "purchase"
    },
    # 2. Corrupt Transaction Record (Multiple Schema Violations)
    {
        "transaction_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "user_id": None,
        "event_timestamp": "INVALID_TIMESTAMP",
        "merchant": {
            "merchant_id": "merchant_9",
            "category": "Amazon India",
            "city": "Mumbai",
            "country": "in"
        },
        "device": {
            "ip_address": "999.999.999.999",
            "device_id": "111e8400-e29b-41d4-a716-446655440999"
        },
        "amount": -4500.00,
        "currency": "INR",
        "location": {
            "latitude": 19.0760,
            "longitude": 72.8777
        },
        "channel": "pos_chip",
        "action": "purchase"
    }
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s|%(levelname)s|%(message)s"
)

logger=logging.getLogger(__name__)

for item in sample_records:
    try:
        clean_item=Transaction.model_validate(item)
    except ValidationError as e:
        logger.warning(f"Transaction validation failed: {e.errors()}")
        filepath=Path(__file__).resolve().parent
        saved_file=filepath/'dlq.jsonl'
        dlq_payload={
            'raw_record':item,
            "error_details":e.errors(),
            "failed_at":datetime.now(timezone.utc).isoformat()
        }
        with open(file=saved_file,mode='a',encoding='utf-8') as f:
            f.write(json.dumps(dlq_payload,default=str)+'\n')
        
       