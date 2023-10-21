from selenium import webdriver
import time

driver = webdriver.Chrome()
seed_url = "https://www.europarl.europa.eu/news/en/press-room"

urls = []
seen = set()
opened = []

pr_list = []

max_pr = 10

driver.get(seed_url)
main_page = driver.page_source
main_soup = BeautifulSoup(main_page)
for tag in main_soup.find_all(class_="ep_gridcolumn ep-m_product ep-layout_linkmode"):
    url = tag.find("a")["href"]
    if url not in seen:
        urls.append(url)
        seen.add(url)

while len(pr_list) < max_pr:

    if len(urls) > 0:

        try:
            curr_url = urls.pop(0)
            response = requests.get(curr_url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = response.content
            opened.append(curr_url)

        except:
            continue

        soup = BeautifulSoup(webpage)
        check_plenary = soup.find("span", {"class": "ep_name"}, text="Plenary session")
        if check_plenary is not None:
            heading = soup.find("h1")
            date = soup.find(class_="ep-p_text ep-layout_date")
            bullets = soup.find(class_="ep-a_facts")
            summary = soup.find(class_="ep-a_text ep-layout_chapo")
            content = soup.find_all(class_="ep-a_text")[1]
            pr = {}
            if heading is not None:
                pr['Heading'] = heading.text
            if date is not None:
                pr['Date'] = date.text
            if bullets is not None:
                pr['Bullets'] = bullets.text
            if summary is not None:
                pr['Summary'] = summary.text
            if content is not None:
                pr['Content'] = content.text
            if any("crisis".lower() in value.lower() for value in pr.values()):
                pr_list.append(curr_url)

    elif (len(urls) == 0) and (main_soup.find(id="continuesLoading_button") is not None):

        load_more = driver.find_element("id", "continuesLoading_button")
        driver.execute_script('arguments[0].click()', load_more)
        time.sleep(5)
        main_page = driver.page_source
        main_soup = BeautifulSoup(main_page)
        for tag in main_soup.find_all(class_="ep_gridcolumn ep-m_product ep-layout_linkmode"):
            url = tag.find("a")["href"]
            if url not in seen:
                urls.append(url)
                seen.add(url)

driver.quit()

pr_list
