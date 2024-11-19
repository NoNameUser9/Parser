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

def make_soup(url: str, num_of_pages: int):
    soup = BeautifulSoup(requests.get(url=url + str(num_of_pages), headers=headers).text, "html.parser")
    return soup

def parse_page(url: str, PAGEN: str):
    soup = make_soup(url + PAGEN, 0)

    # Ищем блок с классом wrap-paging
    pagination = soup.find("div", class_="wrap-paging")
    last_page: int
    # Если блок пагинации найден, ищем максимальный номер страницы
    if pagination:
        # Находим все ссылки внутри блока пагинации
        pages = pagination.find_all("a", class_="btn")

        # Извлекаем номера страниц и находим максимальный
        last_page = max(int(page.text) for page in pages if page.text.isdigit())

        print(f"Общее количество страниц: {last_page}")
    else:
        print("Блок пагинации не найден")

    open(file_path, 'w').close()  # Открываем в режиме 'w' и сразу закрываем, чтобы очистить содержимое

    for i in range(1, last_page + 1):
        soup = make_soup(url + PAGEN, i)
        items = soup.find_all("div", {"class": "product-item"})
        product_data = []
        for item in items:
            title = item.find("a", {"class": "product-item-title"}).text.strip()
            price = item.find("span", {"class": "product-item-price-current"}).text.strip()
            link = (url.replace("/catalog/napolnyy-plintus", "")
                    + item.find("a", {"class": "product-item-title"}).get("href").strip())
            product_data.append({'Название': title, 'Цена': price, 'Ссылка': link})

        df = pd.DataFrame(product_data)
        # Добавлять в файл в режиме 'a' (append) и отключить запись заголовков, начиная со второй итерации
        df.to_csv(file_path, mode='a', header=(i == 0), index=False)
        print(f"Complete:{i}")


if __name__ == '__main__':
    url = "https://dplintus.ru/catalog/napolnyy-plintus"
    PAGEN  = "/?PAGEN_78="
    parse_page(url, PAGEN)
