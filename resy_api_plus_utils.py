import requests
import json
from datetime import datetime, timedelta
import sys
from urls import *

# 5769 Au Cheval
# 834 Charles Prime Rib
# 6194 Carbone
# 1505 Don Angie
# 64593 Torrisi
# 2567 Via Carota
# 58848 Laser Wolf
# 418 Lilia
# 5771 Rezdora
# 42534 Double Chicken Please

def get_num_days(venue, party_size):
    today = datetime.today()
    ytd = today + timedelta(days=365)
    num_days_url = num_days_url_unformatted.format(venue, party_size, today.strftime('%Y-%m-%d'), ytd.strftime('%Y-%m-%d'))
    
    response = requests.get(num_days_url, headers=query_headers)
    
    last_date_str = json.loads(response.text)["last_calendar_day"]
    last_date = datetime.strptime(last_date_str, '%Y-%m-%d')
    return (last_date.date() - today.date()).days + 1


def next_n_days(venue, party_size):
    
    N = get_num_days(venue, party_size)
    
    dates = []
    for i in range(N):
        # Get the date for the next day
        date = datetime.today() + timedelta(days=i)
        # Format the date as a string in the "YYYY-MM-DD" format
        formatted_date = date.strftime('%Y-%m-%d')
        # Add the formatted date to the list of dates
        dates.append(formatted_date)
    return dates

def parse_slots_json(response_json):
    open_times = []
    slot_list = response_json["results"]["venues"][0]["slots"]
    for slot in slot_list:
        start = slot["date"]["start"].split()
        config_id = slot["config"]["token"]
        open_times.append({"time": start[1], "date": start[0], "config":config_id})

    return open_times


def get_slots(date, party_size, venue):
    query_url = query_url_unformatted.format(date, party_size, venue)
    r = requests.get(query_url, headers=query_headers)
    return parse_slots_json(json.loads(r.text))


def book_slot(party_size, slot):
    day = slot["date"]
    config = slot["config"]
    book_token_payload = json.dumps({"commit":1, "config_id": config, "day": day, "party_size": party_size})

    try:
        resp = requests.post(book_token_url, headers=book_token_headers, data=book_token_payload)
        book_token = json.loads(resp.text)["book_token"]["value"]
    except:
        print("getting book token failed with response:")
        print(resp.text)
        return False

    booking_payload = json.dumps({"book_token": book_token, "source_id": "resy.com-venue-details"})
    
    try:
        resp = requests.post(booking_url, headers=book_token_headers, data=booking_payload)
    except:
        print("booking failed with response:")
        print(resp.text)
        return False




def slot_is_ok(start, end, slot):
    time_format = '%H:%M:%S'
    start_time = datetime.strptime(start, time_format).time()
    end_time = datetime.strptime(end, time_format).time()
    slot_time = datetime.strptime(slot, time_format).time()

    return start_time <= slot_time <= end_time



if __name__ == '__main__':
    
    venue = 42534
    party_size = 2
    range_start = "06:00:00"
    range_end = "8:30:00"
    booked = False
    # sys.stdout = open('output.log', 'w')
    # sys.stderr = open('output.log', 'w')
    

    try:    
        days = next_n_days(venue, party_size)
        # print("{} reservable dates".format(len(days)))

        for ind, day in enumerate(days):        
            slots = get_slots(day, party_size, venue)        
            # print("day: [ {} ], open reservations: [ {} ]".format(ind, len(slots)))
            
            for slot in slots:
                if slot_is_ok(range_start, range_end, slot["time"]):
                    print("eligible reservation found: [ {} ] on [ {} ], attempting to book".format(slot["time"], slot["date"]))
                    booked = book_slot(party_size, slot)
                    if booked: 
                        print("booked!") 
                        booked = True
                        break
                    else: 
                        print("couldn't book")
                   
                # else:
                    # print("reservation not eligible: [ {} ] on [ {} ]".format(slot["time"], slot["date"]))
            
            if booked:
                break
    
    except Exception as e:
        print(str(e))
    
    
    