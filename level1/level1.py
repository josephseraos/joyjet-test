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
        condition = lambda article: article['id'] == id
        found = list(filter(condition, articles))
        return found and found[0] or None
    
    # calculate total using list comprehension
    results = [{
        "id": cart['id'],
        "total": sum([
                    (find(item['article_id'], data['articles'])['price'] * item['quantity'])
                    for item in cart['items']
                ])
    } for cart in data['carts']]

    # store results in output.json
    with open('output.json', 'w') as f:
        f.write(json.dumps({'carts': results}, indent=2))

    return 0

if __name__ == "__main__":
    sys.exit(main())
