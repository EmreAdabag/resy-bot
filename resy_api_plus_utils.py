import requests
import json
from datetime import datetime, timedelta
import traceback
from urls import *


def check_availability(venue, party_size):
    today = datetime.today()
    ytd = today + timedelta(days=365)
    url = availability_url_unformatted.format(venue, party_size, today.strftime('%Y-%m-%d'), ytd.strftime('%Y-%m-%d'))
    
    available_days = []

    try:
        r = requests.get(url, headers=query_headers)
        r_json = json.loads(r.text)

        schedule = r_json['scheduled']

        for schedule_day in schedule:
            if schedule_day['inventory']['reservation'] != "sold-out":
                available_days.append(schedule_day['date'])
        
        return available_days
    
    except:
        print("error fetching dates, final response:")
        print(r.text)
        traceback.print_exc()
        exit()



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


def book_slot(party_size, slot) -> bool:
    day = slot["date"]
    config = slot["config"]
    book_token_payload = json.dumps({"commit":1, "config_id": config, "day": day, "party_size": party_size})

    try:
        resp = requests.post(book_token_url, headers=book_token_headers, data=book_token_payload)
        resp.raise_for_status()

        book_token = json.loads(resp.text)["book_token"]["value"]
        booking_payload = "book_token=" + book_token + "&source_id=resy.com-venue-details"
        
        
        resp = requests.post(booking_url, headers=booking_headers, data=booking_payload)
        resp.raise_for_status()

    except requests.exceptions.HTTPError as e:
        print("Request failed:", e)
        print(resp.text)
        return False

    return True



def slot_is_ok(start, end, slot):
    time_format = '%H:%M:%S'
    start_time = datetime.strptime(start, time_format).time()
    end_time = datetime.strptime(end, time_format).time()
    slot_time = datetime.strptime(slot, time_format).time()

    return start_time <= slot_time <= end_time



if __name__ == '__main__':

    venue = 5769
    party_size = 2
    range_start = "18:00:00"
    range_end = "20:30:00"
    booked = False


    try:

        open_dates = check_availability(venue, party_size)

        for ind, day in enumerate(open_dates):
            slots = get_slots(day, party_size, venue)
            print("day: [ {} ], open reservations: [ {} ]".format(ind, len(slots)))

            for slot in slots:
                if slot_is_ok(range_start, range_end, slot["time"]):
                    print("eligible reservation found: [ {} ] on [ {} ], attempting to book".format(slot["time"], slot["date"]))
                    # booked = book_slot(party_size, slot)
                    # if booked:
                    #     print("booked!")
                    #     booked = True
                    #     break
                    # else:
                    #     print("couldn't book")

                else:
                    print("reservation not eligible: [ {} ] on [ {} ]".format(slot["time"], slot["date"]))

            if booked:
                break

    except Exception as e:
        print(str(e))



