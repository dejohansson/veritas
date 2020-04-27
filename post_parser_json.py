import json
import os

order_path = "./parser_orders/*.json"

with open("./parser_menus/menu.json", "r") as f:
    menu = json.load(f)

file_count = 0
for root, _, files in os.walk(order_path):
    file_count += 1
    if file_count % 10000 == 0:
        print("Parsed files:", str(file_count), "\r", end="")
