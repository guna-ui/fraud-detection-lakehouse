import random
import json
from datetime import datetime,timezone,timedelta
from pathlib import Path

# def burst_readings(sensor_id, start_time):
#   for i in range(3):
#     reading_time=start_time+timedelta(seconds=5*i)
#     yield{
#       'sensor_id':sensor_id,
#       'timestamp':reading_time.isoformat(),
#       'temp_c': random.uniform(80.0,90.0),
#       'type':'burst'
#     }
  
# def sensor_stream():
#   while True:
#     mode=random.choices(["normal", "burst", "corrupt"], weights=[70, 20, 10], k=1)[0]
#     if mode=='normal':
#       yield {
#         'temp_c':random.uniform(20.0,30.0),
#         'type':'normal'
#       }
#     if mode=='burst':
#       yield from burst_readings(sensor_id=random.randint(100,200),start_time=datetime.now())

#     if mode=='corrupt':
#       yield {
#         'sensor_id':None,
#         'temp_c':-9999,
#         'type':'corrupt'
#       }

# if __name__=='__main__':
#   filepath=Path(__file__).resolve().parent
#   print(filepath)
#   actualpath=filepath/'sensor_output.jsonl'
#   stream=sensor_stream()
#   with open(file=actualpath, mode='a', encoding='utf-8') as f:
#    for _ in range(0,15):
#      record=next(stream)
#      f.write(json.dumps(record)+ "\n")
    


# Write a 2-line snippet inside a main generator that:

# Uses random.choices() to pick either standard_ping (80% chance) or diagnostic_burst (20% chance) and stores the function in selected_routine.

# Uses yield from to delegate control to selected_routine().

import random

def standard_ping():
    yield {"type": "GPS_UPDATE"}

def diagnostic_burst():
    yield {"type": "DIAG_START"}
    yield {"type": "DIAG_END"}

def main_stream():
    selected_routine_func = random.choices(
        population=[standard_ping, diagnostic_burst], 
        weights=[0.8, 0.2], 
        k=1
    )[0]
    yield from selected_routine_func()

stream = main_stream()

for i in range(2):
    try:
        print(f"Iteration {i+1}:", next(stream))
    except StopIteration:
        print(f"Iteration {i+1}: Stream ended early (standard_ping was chosen)")
        break
