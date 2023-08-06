import pathlib
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

COMMENT_ITEMS_LOCATORS = (
    "body > div > div.box > div > div.componentContainer > div.CommentList > div.listContainer > div.comment_item"
)
VIEW_ALL_BTN = (By.CSS_SELECTOR, "div.pcscorecommentlistcard span[data-v-892a7f08]")
USERNAME_SELECTOR = "div.userName"
DATE_SELECTOR = "div.right > div.part_top > div > div.deviceName > div"
COMMENT_SELECTOR = "div.right > div"
STARS_SELECTOR = "div.newStarBox.starBox > img"


def driver_setup(app_id: str) -> webdriver.Chrome:
    cwd = pathlib.Path.cwd()
    options = Options()
    options.add_argument("--headless")
    driver_service = Service(executable_path=f"{cwd}/chromedriver")
    driver = webdriver.Chrome(service=driver_service, options=options)
    driver.get(f"https://appgallery.huawei.com/app/{app_id}")
    driver.maximize_window()
    sleep(10)
    return driver


def click_view_all(driver) -> None:
    view_all_button = driver.find_element(*VIEW_ALL_BTN)
    view_all_button.click()


def load_source(driver) -> str:
    act = ActionChains(driver)
    # TODO: scroll to the end of the page, now it is just 3 times
    for i in range(1, 4):
        print("scroll number:", i)
        act.send_keys(Keys.END).perform()
        sleep(5)
    return driver.page_source


def get_comment_items(soup: BeautifulSoup) -> list[dict]:
    def _is_star_colored(star) -> bool:
        return star.get("src").endswith("Pgo8L3N2Zz4=")

    reviews_items = soup.select(COMMENT_ITEMS_LOCATORS)
    reviews_data: list = []
    for review_item in reviews_items:
        review_data: dict = {
            "username": review_item.select_one(USERNAME_SELECTOR).text.strip(),
            "date": review_item.select_one(DATE_SELECTOR).text,
            "comment": review_item.select(COMMENT_SELECTOR)[1].text.strip(),
            "rating": sum(1 for star in review_item.select(STARS_SELECTOR) if _is_star_colored(star)),
        }
        reviews_data.append(review_data)
    return reviews_data


def crawl(app_id: str) -> None:
    driver = driver_setup(app_id)
    click_view_all(driver)
    html = load_source(driver)
    soup = BeautifulSoup(html, "html.parser")
    reviews_data = get_comment_items(soup)
    print(reviews_data)
    driver.quit()
