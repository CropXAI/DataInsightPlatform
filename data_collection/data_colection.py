import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

data = pd.read_csv('../data/data_fertilizers.csv')
data_uralhim = data.query('Производители == "Уралхим"')

# Читаем файл CSV с данными
df = data_uralhim.copy()
# Имя выходного файла CSV
output_csv_file = "composition_all.csv"

def parse_fertilizer_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Define the rows to search
    search_rows = {
        "Массовая доля общего азота (N)": None,
        "Массовая доля сульфатов в пересчете на S": None,
        "Массовая доля кальция в пересчете на СаО": None
    }

    # Find all table rows
    rows = soup.find_all('tr')

    for row in rows:
        th = row.find('th', scope='row')
        td = row.find('td')

        if th and td:
            th_text = th.get_text(strip=True)
            td_text = td.get_text(strip=True)

            if th_text in search_rows:
                search_rows[th_text] = td_text

    return search_rows

def save_to_csv(data_list, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["Название удобрения", "Азот, %", "Сера, %", "Кальций, %"])
        # Write the data
        for data in data_list:
            writer.writerow([
                data.get("Название удобрения"),
                data.get("Массовая доля общего азота (N)"),
                data.get("Массовая доля сульфатов в пересчете на S"),
                data.get("Массовая доля кальция в пересчете на СаО")
            ])

def process_urls(urls):
    data_list = []
    for url, fertilizer_name in urls:
        result = parse_fertilizer_data(url)
        if result:
            result["Название удобрения"] = fertilizer_name
            data_list.append(result)
    return data_list

# Файл для сохранения результатов
output_csv_file = "uralchem_composition.csv"

# Список ссылок на товары
product_links = data_uralhim["Ссылка на продукцию"]
product_names = data_uralhim["Название"]

# Заголовки для запросов
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Заголовки для запросов
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


urls = zip(product_links, product_names)

data_list = process_urls(urls)

if data_list:
    save_to_csv(data_list, "fertilizer_data.csv")
    print("Data saved to fertilizer_data.csv")

# Записываем в CSV только один раз заголовок
with open(output_csv_file, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)

    # Заголовок CSV
    header_written = False

    # Обрабатываем каждую ссылку
    for _, row in df.iterrows():
        url = row["Ссылка на продукцию"]

        # Заголовки для запроса
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        # Отправляем запрос
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Создаем объект BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Извлекаем название продукта из <meta property="og:title">
            meta_title = soup.find("meta", property="og:title")
            if meta_title:
                product_name = meta_title.get("content").split(":")[0].strip()
            else:
                product_name = "Неизвестный продукт"

            # Ищем контейнер с составом
            composition_container = soup.find("div", class_="product-details-pills")

            if composition_container:
                # Ищем все элементы состава
                items = composition_container.find_all("div", class_="product-details-pills__subitem")

                # Словарь для хранения состава
                composition = {}
                for item in items:
                    # Извлекаем заголовок и значение
                    header = item.find("span", class_="product-details-pills__item-header")
                    content = item.find("span", class_="product-details-pills__item-content")

                    if header and content:
                        composition[header.text.strip()] = content.text.strip()
                    elif content:
                        # Если только значение (например, "в. раств., % от общ.")
                        composition["Дополнительно"] = content.text.strip()

                # Записываем данные в CSV
                if not header_written:
                    # Если заголовок еще не был записан, добавляем его
                    header_row = ["Название продукта"] + list(composition.keys())
                    writer.writerow(header_row)
                    header_written = True

                # Данные для текущего продукта
                data_row = [product_name] + list(composition.values())
                writer.writerow(data_row)

            else:
                print(f"Состав продукта для {url} не найден.")
        else:
            print(f"Ошибка загрузки страницы {url}: {response.status_code}")

print(f"Все данные успешно записаны в файл {output_csv_file}")