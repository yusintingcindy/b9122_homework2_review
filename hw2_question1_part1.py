from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

seed_url = "https://press.un.org/en"

urls = [seed_url]
seen = [seed_url]
opened = []

pr_list = []

max_pr = 10

while len(urls) > 0 and len(pr_list) < max_pr:
    try:
        curr_url = urls.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= " + curr_url)
        response = requests.get(curr_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = response.content
        opened.append(curr_url)

    except:
        continue

    soup = BeautifulSoup(webpage)
    check_pr = soup.find("a", {"href": "/en/press-release", "hreflang": "en"}, text="Press Release")
    check_page = soup.find("h1", text="Press Release")
    if check_pr is not None:
        print("found press release")
        press_release = soup.find(class_="col-md-9 mb-2 panel-panel radix-layouts-main-column").text
        if "crisis".lower() in press_release.lower():
            print("found press release with crisis")
            pr_list.append(press_release)
    elif (curr_url == seed_url) or (check_page is not None):
        for tag in soup.find_all("a", href=True):
            childUrl = tag["href"]
            childUrl = urljoin(curr_url, childUrl)
            if childUrl not in seen:
                urls.append(childUrl)
                seen.append(childUrl)

pr_list
