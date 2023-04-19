from resy_api_plus_utils import next_n_days, get_slots, slot_is_ok, book_slot
from venues import venue_list, venue_dict
import random
import time
import sys


def thething(venue, range_start, range_end, party_size):
    
    print("looking for reservations at {}".format(venue_dict[venue]))
    days = next_n_days(venue, party_size)

    for day in days:        
        slots = get_slots(day, party_size, venue)        
        
        for slot in slots:
            if slot_is_ok(range_start, range_end, slot["time"]):
                print("eligible reservation found: [ {} ] on [ {} ] at [ {} ], attempting to book".format(slot["time"], slot["date"], venue_dict[venue]))
                booked = book_slot(party_size, slot)
                if booked: 
                    print("booked!") 
                    return
                else: 
                    print("couldn't book")
    
    


def main():

    party_size = 2
    range_start = "06:00:00"
    range_end = "08:30:00" 

    logfile = open('output.log', 'w')
    sys.stdout = logfile
    sys.stderr = logfile


    print("starting search for party size: [ {} ] between [ {} ] and [ {} ]".format(party_size, range_start, range_end))
    logfile.flush()

    for iter in range(1500):
        try:
            thething(venue_list[iter%len(venue_list)], range_start, range_end, party_size)
            time.sleep(random.uniform(0, 60))
        except Exception as e:
            print(str(e))
        
        logfile.flush()


if __name__ == "__main__":
    main()
