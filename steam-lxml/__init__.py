import requests
import lxml.html

urls = {
    "explore_new": "https://store.steampowered.com/explore/new/",
}

xpaths = {
    "new_releases": '//div[@id="tab_newreleases_content"]',
    "new_releases__item_name": './/div[@class="tab_item_name"]/text()',
    "new_releases__item_price": './/div[@class="discount_final_price"]/text()',
    "new_releases__item_tag": './/div[@class="tab_item_top_tags"]',
    "new_releases__platform": './/div[@class="tab_item_details"]',
}


def get_html(url):
    return requests.get(url)


def get_doc(html):
    return lxml.html.fromstring(html.content)


def main():
    doc = get_doc(get_html(urls["explore_new"]))
    new_releases_el = doc.xpath(xpaths["new_releases"])[0]

    names = new_releases_el.xpath(xpaths["new_releases__item_name"])
    print(f"Names: {names[:3]}...\n")

    prices = new_releases_el.xpath(xpaths["new_releases__item_price"])
    print(f"Prices: {prices[:3]}...\n")

    tag_els = new_releases_el.xpath(xpaths["new_releases__item_tag"])
    print(f"Tag Els: {tag_els[:3]}...\n")

    tags = [el.text_content() for el in tag_els]
    tags = [tag.split(", ") for tag in tags]
    print(f"Tags: {tags[:3]}...\n")


if __name__ == "__main__":
    main()
