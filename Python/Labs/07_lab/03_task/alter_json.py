import json


def main():
    with open("ex_3.json", "r") as f, open("new.json", "w") as output:
        data = json.load(f)
        
        new_invoice = {"id":3, "total":0.0, "items":[]}
        
        item_4 = {"name":"item 4", "quantity":5, "price":278.0}  
        new_invoice["items"].append(item_4)
        item_5 = {"name":"item 5", "quantity":3, "price":182.0}
        new_invoice["items"].append(item_5)

        for item in new_invoice["items"]:
            new_invoice["total"] += item["price"] * item["quantity"]

        data["invoices"].append(new_invoice)

        json.dump(data, output, indent=2)


if __name__ == "__main__":
    main()
