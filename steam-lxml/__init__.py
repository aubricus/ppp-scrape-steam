import requests
import lxml.html
import functools
import json
from pprint import pp
from lib import scrape_steam

urls = {
    "explore_new": "https://store.steampowered.com/explore/new/",
}

def main():
    url = urls["explore_new"]
    results = scrape_steam(url)
    for result in results:
        print(
            f"Title: {result["title"]}\n- Price: {result["price"]}\n- Tags: {", ".join(result["tags"])}\n- Platforms: {", ".join(result["platforms"])}\n"
        )


if __name__ == "__main__":
    main()
