import json
import csv
import glob

with open("./parser_menus/menu.json", "r") as f:
    menu = json.load(f)
num_products = len(menu["bundled_products"])

with open("./post_parser_orders/device_time_series.csv", "w") as ts_file:
    ts_writer = csv.writer(ts_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    ts_writer.writerow(["device_id", "date", "store_id", "class", "total_price"] + ["product_"+str(i) for i in range(num_products)])
    g = glob.glob("./parser_orders/*.json")
    total_files = len(g)
    file_count = 0
    missing_keys = set()
    last_id = None
    parsed_rows = []
    for order_file in g:
        if file_count%10000 == 0:
            print("Parsing files:", str(file_count)+"/"+str(total_files), "\r", end="")
        file_count += 1
        spl = order_file[13:].split("_")
        device_id = "_".join(spl[1:len(spl)-1])
        if device_id == "":
            continue
        time_stamp = spl[len(spl)-1][:10]
        with open(order_file, "r") as f:
            order = json.load(f)

        product_vector = [0]*num_products
        for product in order["products"]:
            try:
                product_vector[menu["products_map"][str(product["product_id"])]] += product["quantity"]
            except KeyError as err:
                missing_keys.add(err.args[0])

        parsed_rows.append([device_id, time_stamp, order["store_id"], order["class"], order["price"]//100] + product_vector)
        
        if (last_id is not None and last_id != device_id):
            ts_writer.writerows(parsed_rows)
            parsed_rows = []
            last_id = device_id
        else:
            last_id = device_id
    ts_writer.writerows(parsed_rows)
print("Parsing files:", str(file_count)+"/"+str(total_files), "\r", end="")
print("\nDone! :)")
print("Missing keys:", missing_keys)
