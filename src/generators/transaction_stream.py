import random
import uuid
from datetime import datetime,timezone
from faker import Faker


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

def transactionStream():
    
    # print(location)
    while True:
        location=fake.local_latlng(country_code='IN', coords_only=False)
        current_time=datetime.now(timezone.utc)
        yield {
        "transaction_id": str(uuid.uuid4()),
        "user_id": random.choice(USERS),
        "event_timestamp": current_time.isoformat(),
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
        "amount": round(random.uniform(1000,10000),2),
        "currency": random.choice(currency),
        "location": {
            "latitude": float(location[0]),
            "longitude": float(location[1])
        },
        "channel": "pos_chip",
        "action": "purchase"
    }


if __name__ == "__main__":
    
    stream=transactionStream()
    for _ in range(3):
        print(next(stream))
