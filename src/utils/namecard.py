import json
import random

with open("store/namecards.json") as file:
    data = json.load(file)


def random_namecard():
    key = random.choice(list(data.keys()))
    url = f"https://enka.network/ui/{data[key]['icon']}.png"

    return url
