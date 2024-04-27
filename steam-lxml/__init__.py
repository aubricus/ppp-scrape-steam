import requests
import lxml.html
import functools

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


def main():
    url = urls["explore_new"]
    releases = get_releases(url)
    prices = get_prices(url)
    tags = get_tags(url)
    platforms = get_platforms(url)

    print(f"Releases: {releases[:3]}...({len(releases)} more)")
    print(f"Prices: {prices[:3]}...({len(prices)} more)")
    print(f"Tags: {tags[:3]}...{len(tags)} more")
    print(f"Platforms: {platforms[:3]}...({len(platforms)} more))")


if __name__ == "__main__":
    main()
