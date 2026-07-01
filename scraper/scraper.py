import requests
from bs4 import BeautifulSoup
import json

url = "https://www.shl.com/search/?q=Individual+Test+Solutions"

response = requests.get(url)

print(response.status_code)