import requests
import lxml.html

URL = "https://store.steampowered.com/explore/new/"


def get_html(url):
    return requests.get(url)


def get_doc(html):
    return lxml.html.fromstring(html.content)


def main():
    doc = get_doc(get_html(URL))
    print(doc)


if __name__ == "__main__":
    main()
