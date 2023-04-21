from resy_api_plus_utils import check_availability, get_slots, slot_is_ok, book_slot
from venues import venue_list, venue_dict
from datetime import datetime
import random
import time
import sys
import traceback

def log_entry(logstr):
    time = datetime.now().strftime("%H:%M:%S")
    log_entry = f"{time}: {logstr}\n"
    
    with open("output.log", "a") as f:
        f.write(log_entry)

def thething(venue, range_start, range_end, weekdays, party_size):

    open_dates = check_availability(venue, party_size, weekdays)

    for day in open_dates:
        slots = get_slots(day, party_size, venue)

        for slot in slots:
            if slot_is_ok(range_start, range_end, slot["time"]):
                log_entry("eligible reservation found: [ {} ] on [ {} ] at [ {} ], attempting to book".format(slot["time"], slot["date"], venue_dict[venue]))
                booked = book_slot(party_size, slot)
                if booked:
                    log_entry("booked!")
                    return True, True
                else:
                    log_entry("booking failed")
            # else:
            #     log_entry("ineligible reservation found: [ {} ] on [ {} ] at [ {} ]".format(slot["time"], slot["date"], venue_dict[venue]))
    
    return len(open_dates) > 0, False
            




def main():

    party_size = 2
    range_start = "18:00:00"
    range_end = "21:00:00"
    weekdays = [4,5]

    print("starting search for party size [ {} ] between [ {} ] and [ {} ] on weekdays {}".format(party_size, range_start, range_end, weekdays))
    print("venues: ", [venue_dict[venue] for venue in venue_list])
    
    check_venue = [True for i in range(len(venue_list))]

    try:
        for iter in range(1500):

            for ind, venue in enumerate(venue_list):

                if check_venue[ind] == False:
                    check_venue[ind] = True
                    continue

                day_found, booked = thething(venue, range_start, range_end, weekdays, party_size)
                
                if day_found:
                    check_venue[ind] = False        # don't immediately recheck a venue with an open day

                if booked:
                    return
            
            time.sleep(random.uniform(0, 60))
            if iter%5==0:
                print(f"status: running iter [ {iter} ]")
    except KeyboardInterrupt:
        sys.exit(0)

    except Exception as e:
        traceback.print_tb()
        return



if __name__ == "__main__":
    main()
