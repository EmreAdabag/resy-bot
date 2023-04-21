#!/usr/local/bin/python3.10
from resy_api_plus_utils import check_availability, get_slots, slot_is_ok, book_slot
from venues import venue_dict, reverse_venue_dict
import sys
import traceback
import time

def snipe(venue, range_start, range_end, weekdays, party_size):
    print("looking for reservations at {}".format(venue_dict[venue]))
    open_dates = check_availability(venue, party_size, weekdays)

    for day in open_dates:
        slots = get_slots(day, party_size, venue)
        print("{} open reservations: [ {} ]".format(day, len(slots)))

        for slot in slots:
            if slot_is_ok(range_start, range_end, slot["time"]):
                print("eligible reservation found: [ {} ] on [ {} ] at [ {} ], attempting to book".format(slot["time"], slot["date"], venue_dict[venue]))
                booked = book_slot(party_size, slot)
                if booked:
                    print("booked!")
                    return
                else:
                    print("couldn't book")
            else:
                print("reservation not eligible: [ {} ] on [ {} ]".format(slot["time"], slot["date"]))


def snipe_d(venue, range_start, range_end, date, party_size):
    print("looking for reservations at {}".format(venue_dict[venue]))

    duration = 15
    starttime = time.time()
    slots = []

    while len(slots) == 0:
        slots = get_slots(date, party_size, venue)
        curtime = time.time()
        if curtime - starttime >= duration:
            break

    # print("{} open reservations: [ {} ]".format(day, len(slots)))

    for slot in slots:
        if slot_is_ok(range_start, range_end, slot["time"]):
            # print("eligible reservation found: [ {} ] on [ {} ] at [ {} ], attempting to book".format(slot["time"], slot["date"], venue_dict[venue]))
            booked = book_slot(party_size, slot)
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
        
        if len(sys.argv) > 3:
            date = sys.argv[3]
        else:
            weekdays = [0,1,2,3,4,5,6]
    except:
        print("usage: ./snipe.py <venue> <party_size> [date]")
        exit()
    
    try:
        if len(sys.argv) > 3:
            snipe_d(venue, range_start, range_end, date, party_size)
        else:
            snipe(venue, range_start, range_end, weekdays, party_size)
    except Exception as e:
        traceback.print_exc()
        print(e)
