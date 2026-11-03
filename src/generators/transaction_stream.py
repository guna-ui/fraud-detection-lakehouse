import pathlib
import json
import random
import uuid
from datetime import datetime,timezone,timedelta
from faker import Faker
from pathlib import Path

USERS=['user_1', 'user_2', 'user_3', 'user_4', 'user_5', 'user_6', 'user_7', 'user_8', 'user_9', 'user_10', 'user_11', 'user_12', 'user_13', 'user_14', 'user_15', 'user_16', 'user_17', 'user_18', 'user_19', 'user_20', 'user_21', 'user_22', 'user_23', 'user_24', 'user_25', 'user_26', 'user_27', 'user_28', 'user_29', 'user_30', 'user_31', 'user_32', 'user_33', 'user_34', 'user_35', 'user_36', 'user_37', 'user_38', 'user_39', 'user_40', 'user_41', 'user_42', 'user_43', 'user_44', 'user_45', 'user_46', 'user_47', 'user_48', 'user_49', 'user_50']
category = [
    "Swiggy",    "Zomato","A2B (Adyar Ananda Bhavan)","Starbucks Coffee",
    "Thalappakatti Biryani","Blinkit","Zepto","BigBasket","Reliance Smart",
    "Uber India","Ola Cabs","Namma Yatri","MakeMyTrip","IRCTC","Amazon India",
    "Flipkart","Myntra","TANGEDCO (Electricity)","Airtel Postpaid","Netflix India",
    "BookMyShow","Indian Oil Corporation","Bharat Petroleum","Apollo Pharmacy","Pharmeasy"
]
currency=['INR', 'USD', 'EUR', 'GBP']

merchant=['merchant_1', 'merchant_2', 'merchant_3', 'merchant_4', 'merchant_5', 'merchant_6', 'merchant_7', 'merchant_8', 'merchant_9', 'merchant_10', 'merchant_11', 'merchant_12', 'merchant_13', 'merchant_14', 'merchant_15', 'merchant_16', 'merchant_17', 'merchant_18', 'merchant_19', 'merchant_20', 'merchant_21', 'merchant_22', 'merchant_23', 'merchant_24', 'merchant_25']


fake=Faker()

def rapid_velocity(userid,timestamp):
    for i in range(0,4):
        event_time=timestamp+timedelta(seconds=i*5)
        yield  build_transaction(user_id=userid,event_time=event_time.isoformat())


def travel_fraud(userid,timestamp,country_code=None):
    country_code1,country_code2=random.sample(population=['IN', 'US', 'GB', 'AU'],k=2)
    country_code=[country_code1,country_code2]
    for i in range(0,2):
            event_time=timestamp+timedelta(minutes=i*2)
            yield  build_transaction(user_id=userid,event_time=event_time.isoformat(),country_code=country_code[i])


def multi_currency(userid,timestamp,currency=None):
    currency=random.sample(population=['INR', 'USD', 'EUR', 'GBP'],k=3)
    
    for i in range(0,3):
        amount=round(random.uniform(8000.0,9999.99),2)
        event_time=timestamp+timedelta(seconds=i*30)
        yield  build_transaction(user_id=userid,event_time=event_time.isoformat(),currency_code=currency[i],amount=amount)


def transactionStream():
    while True:
      record=random.choices(['normal', 'velocity', 'travel', 'currency','corrupt'], weights=[80, 1, 1, 1,17], k=1)[0]
      userid=random.choice(USERS)
      timestamp=datetime.now(timezone.utc)
      if record=='normal':
        yield build_transaction()
      if record=='velocity':
        yield from rapid_velocity(userid=userid,timestamp=timestamp)
      if record=='travel':
        yield from travel_fraud(userid=userid,timestamp=timestamp)
      if record=='currency':
        yield from multi_currency(userid=userid,timestamp=timestamp)
      if record=='corrupt':
        yield  corrupted_transaction(user_id=None,event_time=timestamp)


def build_transaction(user_id=None,event_time=None,country_code='IN',currency_code=None,amount=None):
     location=fake.local_latlng(country_code=country_code, coords_only=False)

     return {
        "transaction_id": str(uuid.uuid4()),
        "user_id": user_id or random.choice(USERS),
        "event_timestamp": event_time or datetime.now(timezone.utc).isoformat(),
        "merchant": {
            "merchant_id": random.choice(merchant),
            "category": random.choice(category),
            "city": location[2],
            "country": location[3] 
        },
        "device": {
            "ip_address": fake.ipv4(),
            "device_id": str(uuid.uuid4())
        },
        "amount":  amount or round(random.uniform(1000,10000),2),
        "currency":currency_code or  random.choice(currency),
        "location": {
            "latitude": float(location[0]),
            "longitude": float(location[1])
        },
        "channel": "pos_chip",
        "action": "purchase"
    }

def corrupted_transaction(user_id=None,event_time=None,country_code='IN',currency_code=None,amount=None):
     location=fake.local_latlng(country_code=country_code, coords_only=False)

     return {
        "transaction_id": str(uuid.uuid4()),
        "user_id": None,
        "event_timestamp": "INVALID_TIMESTAMP",
        "merchant": {
            "merchant_id": random.choice(merchant),
            "category": random.choice(category),
            "city": location[2],
            "country": location[3] 
        },
        "device": {
            "ip_address": fake.ipv4(),
            "device_id": str(uuid.uuid4())
        },
        "amount": -round(random.uniform(1000,10000),2),
        "currency":currency_code or  random.choice(currency),
        "location": {
            "latitude": float(location[0]),
            "longitude": float(location[1])
        },
        "channel": "pos_chip",
        "action": "purchase"
    }


if __name__ == "__main__":
       
    stream=transactionStream()
    output_dir = pathlib.Path(r"D:\fraud-detection-pipeline\data\raw") 
    output_dir.parent.mkdir(parents=True,exist_ok=True)
    file_path=output_dir/'transactions.jsonl'
    with open(file=file_path,mode='a',encoding='utf-8') as f:
       print(f"Saving the records to {file_path}")
       for _ in range(100):
         f.write(json.dumps(next(stream))+'\n')
       

