import os
import requests

def get_url(index):
    return "https://kuchnialidla.pl/przepisy/"+str(index)+"#lista"

def download_przepisy_listing(index):
    return requests.get(get_url(index))

def save_przepisy_listing(przepisy_html, index):
    with open("przepisy/listing/"+str(index)+".html", "wb") as f:
        f.write(przepisy_html)

def read_przepisy_listing_item(i):
    with open("przepisy/listing/"+str(i)+".html", "rb") as f:
        return f.read()
    
def run(pages_to_consider):
    os.makedirs("przepisy/listing", exist_ok=True)
    
    for i in range(1,pages_to_consider+1):
        przepisy_html = download_przepisy_listing(i).content
        save_przepisy_listing(przepisy_html, i)