#!/usr/bin/env python3
from argparse import ArgumentParser
import requests
import sys

parser = ArgumentParser(description="Command line client for The Items Service.")

parser.add_argument('url', help="The URL the service is available at. E.g.: http://127.0.0.1:8000/items")
cmd_group = parser.add_mutually_exclusive_group(required=True)
cmd_group.add_argument('-c', '--create', nargs=2, metavar=('name', 'description'), help="Create a new item.")
cmd_group.add_argument('-q', '--query', metavar='name', help="Query the description of an item.")
cmd_group.add_argument('-u', '--update', nargs=2, metavar=('name', 'description'), help="Update an item's description.")
cmd_group.add_argument('-d', '--delete', metavar='name', help="Delete an item.")
cmd_group.add_argument('-l', '--list', action='store_true', help="List all items.")

def print_error(response):
    print("Something went wrong: {error} ({code})".format(error=response.text, code=response.status_code))
    sys.exit(1)
    
def create_item(service_url, name, description):
    resp = requests.post(service_url, json={'name': name, 'description': description})
    if resp.status_code == 200:
        print("Item created successfully.")
    else:
        print_error(resp)

def query_item(service_url, name):
    resp = requests.get(service_url, json={'name': name})
    if resp.status_code == 200:
        print("Name: {name}\nDescription: {description}".format(**resp.json()))
    else:
        print_error(resp)

def update_item(service_url, name, description):
    resp = requests.put(service_url, json={'name': name, 'description': description})
    if resp.status_code == 200:
        print("Item updated successfully.")
    else:
        print_error(resp)

def delete_item(service_url, name):
    resp = requests.delete(service_url, json={'name': name})
    if resp.status_code == 200:
        print("Item deleted successfully.")
    elif resp.status_code == 204:
        print("Item missing.")
    else:
        print_error(resp)

def list_items(service_url):
    resp = requests.get(service_url)
    if resp.status_code == 200:
        items = resp.json()
        if items:
            print("Items:")
            for item in items:
                print("- {name}".format(**item))
        else:
            print("No items to show.")
    else:
        print_error(resp)

if __name__ == '__main__':
    cmd_args = parser.parse_args()

    service_url = cmd_args.url

    if cmd_args.create:
        create_item(service_url, *cmd_args.create)
    elif cmd_args.query:
        query_item(service_url, cmd_args.query)
    elif cmd_args.update:
        update_item(service_url, *cmd_args.update)
    elif cmd_args.delete:
        delete_item(service_url, cmd_args.delete)
    elif cmd_args.list:
        list_items(service_url)
    else:
        parser.print_help()

