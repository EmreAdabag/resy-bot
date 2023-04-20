from keys import api_key, resy_auth_token

availability_url_unformatted = "https://api.resy.com/4/venue/calendar?venue_id={}&num_seats={}&start_date={}&end_date={}"
query_url_unformatted = "https://api.resy.com/4/find?lat=0&long=0&day={}&party_size={}&venue_id={}"
book_token_url = "https://api.resy.com/3/details"
booking_url = "https://api.resy.com/3/book"

query_headers = { "authorization": "ResyAPI api_key={}".format(api_key), "cache-control": "no-cache"}

book_token_headers = {
    "authorization": "ResyAPI api_key={}".format(api_key),
    "origin": "https://widgets.resy.com",
    "referer": "https://widgets.resy.com/",
    "content-type": "application/json",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "x-origin": "https://widgets.resy.com",
    "x-resy-auth-token": resy_auth_token
}

booking_headers = {
    "authorization": "ResyAPI api_key={}".format(api_key),
    "origin": "https://widgets.resy.com",
    "referer": "https://widgets.resy.com/",
    "content-type": "application/x-www-form-urlencoded",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "x-origin": "https://widgets.resy.com",
    "x-resy-auth-token": resy_auth_token
}