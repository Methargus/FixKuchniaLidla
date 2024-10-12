from dataclasses import dataclass
from bs4 import BeautifulSoup
    
@dataclass
class Nutrients:
    whole_dish_calories: float #kcal
    one_portion_calories: float #kcal
    fat_amount: float #grams
    carbs_amount: float #grams
    protein_amount: float #grams

def read_nutrients(html):
    soup = BeautifulSoup(html, 'html.parser')
    nutrients = soup.select(".skladniki wartosci")
    #find tr which has td with text "na całe danie" and take its td
    whole_dish_calories = nutrients.select_one("tr:has(td:contains('na całe danie')) td:nth-of-type(2)").text
    one_portion_calories = nutrients.select_one("tr:has(td:contains('na 1 porcję')) td:nth-of-type(2)").text
    fat_amount = nutrients.select_one("tr:has(td:contains('Tłuszcz')) td:nth-of-type(2)").text
    carbs_amount = nutrients.select_one("tr:has(td:contains('Węglowodany')) td:nth-of-type(2)").text
    protein_amount = nutrients.select_one("tr:has(td:contains('Białko')) td:nth-of-type(2)").text

    return Nutrients(
        whole_dish_calories = whole_dish_calories,
        one_portion_calories = one_portion_calories,
        fat_amount = fat_amount,
        carbs_amount = carbs_amount,
        protein_amount = protein_amount
    )

#https://www.nal.usda.gov/programs/fnic
def calculate_calories(nutrients: Nutrients):
    calories = 4*nutrients.protein_amount + 4*nutrients.carbs_amount + 9*nutrients.fat_amount
    return calories

def normalize_nutrients(nutrients: Nutrients):
    calories = calculate_calories(nutrients)

    diff_to_whole_dish = abs(nutrients.whole_dish_calories - calories)
    diff_to_serving = abs(nutrients.one_portion_calories - calories)

    if diff_to_whole_dish < diff_to_serving :
        return Nutrients(
            whole_dish_calories = nutrients.whole_dish_calories,
            one_portion_calories = nutrients.one_portion_calories,
            fat_amount = nutrients.fat_amount,
            carbs_amount = nutrients.carbs_amount,
            protein_amount = nutrients.protein_amount
        )
    else:
        servings = nutrients.whole_dish_calories / nutrients.one_portion_calories

        return Nutrients(
            whole_dish_calories = nutrients.whole_dish_calories,
            one_portion_calories = nutrients.one_portion_calories,
            fat_amount = nutrients.fat_amount * servings,
            carbs_amount = nutrients.carbs_amount * servings,
            protein_amount = nutrients.protein_amount * servings
        )

def get_nutrients(html):
    nutrients = read_nutrients(html)
    return normalize_nutrients(nutrients)