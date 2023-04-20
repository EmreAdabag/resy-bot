#!/usr/local/bin/python3.10
from resy_api_plus_utils import check_availability, get_slots, slot_is_ok, book_slot
from venues import venue_list, venue_dict, reverse_venue_dict
import sys
import traceback


def snipe(venue, range_start, range_end, party_size):
    print("looking for reservations at {}".format(venue_dict[venue]))
    open_dates = check_availability(venue, party_size)

    for ind, day in enumerate(open_dates):
        slots = get_slots(day, party_size, venue)
        print("day: [ {} ], open reservations: [ {} ]".format(ind, len(slots)))

        for slot in slots:
            if slot_is_ok(range_start, range_end, slot["time"]):
                print("eligible reservation found: [ {} ] on [ {} ] at [ {} ], attempting to book".format(slot["time"], slot["date"], venue_dict[venue]))
                booked = book_slot(party_size, slot)
                booked = False
                if booked:
                    print("booked!")
                    return
                else:
                    print("couldn't book")
            else:
                print("reservation not eligible: [ {} ] on [ {} ]".format(slot["time"], slot["date"]))





if __name__ == '__main__':
    try:
        venue = int(reverse_venue_dict[sys.argv[1]])
        party_size = sys.argv[2]
        range_start = "18:00:00"
        range_end = "20:30:00"
    except:
        print("args!")
        exit()
    
    try:
        snipe(venue, range_start, range_end, party_size)
    except Exception as e:
        traceback.print_exc()
        print(e)
