#!/usr/bin/env python3
from argparse import ArgumentParser
import requests
import sys

parser = ArgumentParser(description="Command line client for The Items Service.")

parser.add_argument('url', help="The URL the service is available at. "
                                "E.g.: http://127.0.0.1:8000/items")
cmd_group = parser.add_mutually_exclusive_group(required=True)
cmd_group.add_argument('-c', '--create', nargs=2, metavar=('name', 'description'),
                       help="Create a new item.")
cmd_group.add_argument('-q', '--query', metavar='name',
                       help="Query the description of an item.")
cmd_group.add_argument('-u', '--update', nargs=2, metavar=('name', 'description'),
                       help="Update an item's description.")
cmd_group.add_argument('-d', '--delete', metavar='name', help="Delete an item.")
cmd_group.add_argument('-l', '--list', action='store_true', help="List all items.")
parser.add_argument('-t', '--timeout', default=5, help="Timeout in seconds.")

def get_error(response):
    return (
        "Ooops! Something went wrong: {reason} ({code})".format(
            reason=response.reason,
            code=response.status_code
        ),
        response.status_code
    )
    
def create_item(service_url, timeout, name, description):
    resp = requests.post(service_url, timeout=timeout,
                         json={'name': name, 'description': description})
    if resp.status_code == 200:
        return "Item created successfully.", 0
    elif resp.status_code == 409:
        return "An item with this name already exists.", 1
    else:
        return get_error(resp)

def query_item(service_url, timeout, name):
    resp = requests.get(service_url, timeout=timeout, json={'name': name})
    if resp.status_code == 200:
        return "Description: {description}".format(**resp.json()), 0
    elif resp.status_code == 404:
        return "Item not found.", 1
    else:
        return get_error(resp)

def update_item(service_url, timeout, name, description):
    resp = requests.put(service_url, timeout=timeout,
                        json={'name': name, 'description': description})
    if resp.status_code == 200:
        return "Item updated successfully.", 0
    elif resp.status_code == 404:
        return "Item not found.", 1
    else:
        return get_error(resp)

def delete_item(service_url, timeout, name):
    resp = requests.delete(service_url, timeout=timeout, json={'name': name})
    if resp.status_code == 200:
        return "Item deleted successfully.", 0
    elif resp.status_code == 204:
        return "Item not found.", 1
    else:
        return get_error(resp)

def list_items(service_url, timeout):
    resp = requests.get(service_url, timeout=timeout)
    if resp.status_code == 200:
        items = resp.json()['items']
        if items:
            return (
                "Items:\n" + "\n".join("- {name}".format(**item)
                                       for item in items),
                0
            )
        else:
            return "No items to show.", 0
    else:
        return get_error(resp)

if __name__ == '__main__':
    cmd_args = parser.parse_args()

    service_url = cmd_args.url
    timeout = cmd_args.timeout

    if cmd_args.create:
        msg, code = create_item(service_url, timeout, *cmd_args.create)
    elif cmd_args.query:
        msg, code = query_item(service_url, timeout, cmd_args.query)
    elif cmd_args.update:
        msg, code = update_item(service_url, timeout, *cmd_args.update)
    elif cmd_args.delete:
        msg, code = delete_item(service_url, timeout, cmd_args.delete)
    elif cmd_args.list:
        msg, code = list_items(service_url, timeout)
    else:
        msg, code = parser.format_help(), -1

    print(msg)
    sys.exit(code)
