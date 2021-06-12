import http.client

conn = http.client.HTTPSConnection("morningstar1.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "morningstar1.p.rapidapi.com",
    'x-rapidapi-key': "73889f0ea5msh553da424572dcb0p19b0c2jsnfa9ef38d03d4",
    'accept': "string"
    }

conn.request("GET", "/companies/get-company-profile?Ticker=MSFT&Mic=XNAS", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))