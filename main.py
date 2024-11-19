import pandas as pd, requests
from bs4 import BeautifulSoup

file_path = 'resulted_data.csv'
st_accept = "text/html"
st_useragent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_1) AppleWebKit/605.1.15"
                " (KHTML, like Gecko) Version/18.0 Safari/605.1.15")
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}

def make_soup(url: str, page_number: int):
    response = requests.get(url=f"{url}{page_number}", headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def parse_page(url: str, PAGEN: str):
    soup = make_soup(url + PAGEN, 0)

    # Find the number of pages
    pagination = soup.find("div", class_="wrap-paging")
    last_page: int
    if pagination:
        pages = pagination.find_all("a", class_="btn")
        last_page = max(int(page.text) for page in pages if page.text.isdigit())
        print(f"Number of pages: {last_page}")
    else:
        print("Paginaiton not found")

    # Create a list to store the data
    data = []
    # Iterate over the pages

    open(file_path, 'w').close()  # Открываем в режиме 'w' и сразу закрываем, чтобы очистить содержимое

    # Iterate over the items and extract the data
    for page_number in range(1, last_page + 1):
        soup = make_soup(url + PAGEN, page_number)
        items = soup.find_all("div", class_="product-item")
        for item in items:
            title = item.find("a", class_="product-item-title").text.strip()
            price = item.find("span", class_="product-item-price-current").text.strip()
            link = (url.replace("/catalog/napolnyy-plintus", "")
                    + item.find("a", class_="product-item-title").get("href").strip())
            data.append({"title": title, "price": price, "link": link})
            # df.to_csv(file_path, mode='a', header=(page_number == 0), index=False)
        print(f"Complete:{page_number}")

    # Save the data to a CSV file
    df = pd.DataFrame(data)
    df.to_csv(file_path, mode='a', index=False)

    print(f"Data saved to {file_path}")


if __name__ == '__main__':
    url = "https://dplintus.ru/catalog/napolnyy-plintus"
    PAGEN  = "/?PAGEN_78="
    parse_page(url, PAGEN)
