#!/usr/bin/env python3

import sys
import json


def main():
    data = None

    # reads data from file data.json
    with open('data.json') as f:
        data = json.loads(f.read())
    
    # select article by ID
    def find(id, articles):
        condition = lambda article: article['id'] == id  # to be used in the filter built-in function
        found = list(filter(condition, articles))
        
        # considering ID is unique, the filter will return just one or zero article
        return found and found[0] or None

    # calculate total using list comprehension
    results = [{
        "id": cart['id'],
        "total": sum([
                    (find(item['article_id'], data['articles'])['price'] * item['quantity'])
                    for item in cart['items']
                ])
    } for cart in data['carts']]

    # select delivery_fee by total
    def calculate_delivery_fee(total, delivery_fees):
        condition = lambda fee: total >= fee['eligible_transaction_volume']['min_price'] and\
                                total < (fee['eligible_transaction_volume']['max_price'] or float("inf"))
                                
        delivery_fee = (list(filter(condition, delivery_fees))[0])['price']
        return delivery_fee
    
    # total with the new value
    results_with_delivery_fee = [{
        "id": result["id"],
        "total": result["total"] + calculate_delivery_fee(result["total"], data['delivery_fees'])
    } for result in results]

    # store result in output.json
    with open('output.json', 'w') as f:
        f.write(json.dumps({'carts': results_with_delivery_fee}, indent=2))

    return 0

if __name__ == "__main__":
    sys.exit(main())
