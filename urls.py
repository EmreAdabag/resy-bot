from keys import api_key, resy_auth_token

query_url_unformatted = "https://api.resy.com/4/find?lat=0&long=0&day={}&party_size={}&venue_id={}"
num_days_url_unformatted = "https://api.resy.com/4/venue/calendar?venue_id={}&num_seats={}&start_date={}&end_date={}"
book_token_url = "https://api.resy.com/3/details"
booking_url = "https://api.resy.com/3/book"

query_headers = { "authorization": "ResyAPI api_key={}".format(api_key), "cache-control": "no-cache"}

book_token_headers = {
"accept": "application/json, text/plain, */*",
"accept-encoding": "gzip, deflate, br",
"accept-language": "en-US,en;q=0.9",
"authorization": "ResyAPI api_key={}".format(api_key),
"cache-control": "no-cache",
"content-type": "application/json",
"origin": "https://widgets.resy.com",
"referer": "https://widgets.resy.com/",
"sec-ch-ua-mobile": "?0",
"sec-fetch-dest": "empty",
"sec-fetch-mode": "cors",
"sec-fetch-site": "same-site",
"x-origin": "https://widgets.resy.com",
"x-resy-auth-token": resy_auth_token,
"x-resy-universal-auth": resy_auth_token
}