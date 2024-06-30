import http.client
import json
import os

api_key = os.environ.get("SERPER_API_KEY")

def getClinic(query: str):
  conn = http.client.HTTPSConnection("google.serper.dev")
  payload = json.dumps({
    "q": query
  })
  headers = {
    'X-API-KEY': api_key,
    'Content-Type': 'application/json'
  }
  conn.request("POST", "/places", payload, headers)
  res = conn.getresponse()
  data = res.read()
  return data