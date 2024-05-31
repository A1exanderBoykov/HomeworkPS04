from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def setup_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver


def search_wikipedia(driver, query):
    url = f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}"
    driver.get(url)
    return driver


def list_paragraphs(driver):
    paragraphs = driver.find_elements(By.XPATH, "//p")
    for i, p in enumerate(paragraphs):
        print(f"Параграф {i + 1}:\n{p.text}\n")
        time.sleep(0.1)


def list_links(driver):
    links = driver.find_elements(By.XPATH, "//div[@id='bodyContent']//a[@href]")
    for i, link in enumerate(links):
        print(f"Ссылка {i + 1}: {link.get_attribute('href')}")
        print(f"Текст: {link.text}\n")
        time.sleep(0.1)  
    return links


def main():
    driver = setup_browser()
    try:
        query = input("Введите ваш запрос для поиска в Википедии: ")
        driver = search_wikipedia(driver, query)

        while True:
            print("\nВыберите действие:")
            print("1. Список параграфов")
            print("2. Перейти на связанную страницу")
            print("3. Выход")
            choice = input("Введите номер вашего выбора: ")

            if choice == "1":
                list_paragraphs(driver)
            elif choice == "2":
                links = list_links(driver)
                link_choice = int(input("Введите номер ссылки для перехода: "))
                if 0 < link_choice <= len(links):
                    driver.get(links[link_choice - 1].get_attribute('href'))
                else:
                    print("Неверный номер ссылки.")
            elif choice == "3":
                break
            else:
                print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()