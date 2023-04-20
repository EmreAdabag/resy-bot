from resy_api_plus_utils import check_availability, get_slots, slot_is_ok, book_slot
from venues import venue_list, venue_dict
from datetime import datetime
import random
import time
import traceback

def log_entry(logstr):
    time = datetime.now().strftime("%H:%M:%S")
    log_entry = f"{time}: {logstr}\n"
    
    with open("output.log", "a") as f:
        f.write(log_entry)

def thething(venue, range_start, range_end, party_size):

    # print("looking for reservations at {}".format(venue_dict[venue]))
    open_dates = check_availability(venue, party_size)

    for day in open_dates:
        slots = get_slots(day, party_size, venue)

        for slot in slots:
            if slot_is_ok(range_start, range_end, slot["time"]):
                log_entry("eligible reservation found: [ {} ] on [ {} ] at [ {} ], attempting to book".format(slot["time"], slot["date"], venue_dict[venue]))
                booked = book_slot(party_size, slot)
                if booked:
                    log_entry("booked!")
                    return 1
                else:
                    log_entry("booking failed")
            # else:
            #     log_entry("ineligible reservation found: [ {} ] on [ {} ] at [ {} ]".format(slot["time"], slot["date"], venue_dict[venue]))
    
    return 0
            




def main():

    party_size = 2
    range_start = "18:00:00"
    range_end = "20:30:00"


    print("starting search for party size: [ {} ] between [ {} ] and [ {} ]".format(party_size, range_start, range_end))

    try:
        for iter in range(1500):

            for venue in venue_list:
                booked = thething(venue, range_start, range_end, party_size)
                if booked:
                    return
            
            time.sleep(random.uniform(0, 60))
            if iter%15==0:
                print(f"status: running iter [ {iter} ]")

    except Exception as e:
        traceback.print_tb()
        return



if __name__ == "__main__":
    main()
