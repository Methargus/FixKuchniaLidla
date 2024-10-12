#downloads html files from the web
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import os
import przepisy_listing
import nutrients_parser

max_pages_to_consider = 3 

@dataclass
class Dish:
    link: str
    nutrients: nutrients_parser.Nutrients


def get_recipes_link(przepisy_listing_item):
    soup = BeautifulSoup(przepisy_listing_item, 'html.parser')
    recipes = soup.select(".recipe_box")
    return [recipe.select_one("a")["href"] for recipe in recipes]

def save_recipes_links(recipes_links, i):
    count = len(recipes_links)
    directory_path = os.path.join("przepisy", "lista", str(i))
    os.makedirs(directory_path, exist_ok=True)  # Ensure the directory exists

    path = os.path.join(directory_path, "count.txt")
    with open(path, "w") as f:
        f.write(str(count))

    for recipe_link in recipes_links:
        recipe_link_path = os.path.join(directory_path, recipe_link.split("/")[-1] + ".html")
        recipe = requests.get("https://kuchnialidla.pl/" + recipe_link.split("/")[-1])

        with open(recipe_link_path, "wb") as f:
            f.write(recipe.content)
            

# przepisy_listing.run(max_pages_to_consider)

for i in range(1,max_pages_to_consider+1):
    # przepisy_listing = read_przepisy_listing_item(i)
    przepisy_listing_item = przepisy_listing.read_przepisy_listing_item(i)

    recipes_links = get_recipes_link(przepisy_listing_item)

    save_recipes_links(recipes_links, i)

for i in range(1,max_pages_to_consider+1):
    count = 0
    with open("przepisy/lista/"+str(i)+"/count.txt", "r") as f:
        count = int(f.read())
    
    #get all files in directory
    directory_path = os.path.join("przepisy", "lista", str(i))
    files = os.listdir(directory_path)
    files = [file for file in files if file.endswith(".html")]

    if count != files.count():
        print("Page "+str(i)+" is corrupted, expected "+str(count)+" files, but found "+str(files.count())+" files")

    for file in files:
        with open(os.path.join(directory_path, file), "rb") as f:
            dish = Dish(link="https://kuchnialidla.pl/"+file.removesuffix(".html"), nutrients=nutrients_parser.get_nutrients(f.read()))