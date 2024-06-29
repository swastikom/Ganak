import http.client
import json


def getClinic(query: str):
  conn = http.client.HTTPSConnection("google.serper.dev")
  payload = json.dumps({
    "q": query
  })
  headers = {
    'X-API-KEY': 'cc1aab846bdfa504db2c521f17b8132075d0be1d',
    'Content-Type': 'application/json'
  }
  conn.request("POST", "/places", payload, headers)
  res = conn.getresponse()
  data = res.read()
  return data