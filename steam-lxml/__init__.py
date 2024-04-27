import requests
import lxml.html
import functools
import json
from pprint import pp

urls = {
    "explore_new": "https://store.steampowered.com/explore/new/",
}

xpaths = {
    "new_releases": '//div[@id="tab_newreleases_content"]',
    "new_releases__item_name": './/div[@class="tab_item_name"]/text()',
    "new_releases__item_price": './/div[@class="discount_final_price"]/text()',
    "new_releases__item_tag": './/div[@class="tab_item_top_tags"]',
    "new_releases__platform": './/div[@class="tab_item_details"]',
    "new_releases__platform__platform_img": './/span[contains(@class, "platform_img")]',
}


def get_html(url):
    return requests.get(url)


@functools.lru_cache()
def get_doc(url):
    return lxml.html.fromstring(get_html(url).content)


@functools.lru_cache()
def get_releases_el(url):
    return get_doc(url).xpath(xpaths["new_releases"])[0]


def get_releases(url):
    return get_releases_el(url).xpath(xpaths["new_releases__item_name"])


def get_prices(url):
    return get_releases_el(url).xpath(xpaths["new_releases__item_price"])


def get_tags(url):
    els = get_releases_el(url).xpath(xpaths["new_releases__item_tag"])
    return [tag.split(", ") for tag in [el.text_content() for el in els]]


def get_platforms(url):
    els = get_releases_el(url).xpath(xpaths["new_releases__platform"])
    memo = []
    for el in els:
        platform_imgs = el.xpath(xpaths["new_releases__platform__platform_img"])
        platforms = [img.get('class').split(" ")[-1] for img in platform_imgs]
        if("hmd_separator" in platforms):
            platforms.remove("hmd_separator")
        memo.append(platforms)
    return memo


def scrape_steam(url):
    memo = []
    for i in zip(get_releases(url), get_prices(url), get_tags(url), get_platforms(url)):
        data = {
            "title": i[0],
            "price": i[1],
            "tags": i[2],
            "platforms": i[3]
        }
        memo.append(data)
    return memo


def main():
    url = urls["explore_new"]
    results = scrape_steam(url)
    for result in results:
        print(
            f"Title: {result["title"]}\n- Price: {result["price"]}\n- Tags: {", ".join(result["tags"])}\n- Platforms: {", ".join(result["platforms"])}\n"
        )


if __name__ == "__main__":
    main()
