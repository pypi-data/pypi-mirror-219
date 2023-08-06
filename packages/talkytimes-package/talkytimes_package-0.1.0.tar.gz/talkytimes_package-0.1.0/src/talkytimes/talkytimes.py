import time

from selenium.webdriver.common.by import By

from talkytimes.base import AbstractAutomation


class TalkyTimesAutomation(AbstractAutomation):
    table = "users_info"

    def login_task(self, *, user: str, pw: str) -> None:
        user_input = "/html/body/div[1]/div/div[1]/main/div/div/div/div/div[1]/div/div[1]/form/div/div[1]/div/input"
        pw_input = "/html/body/div[1]/div/div[1]/main/div/div/div/div/div[1]/div/div[1]/form/div/div[2]/div/input"
        login_button = "/html/body/div[1]/div/div[1]/main/div/div/div/div/div[1]/div/div[2]/button"
        self.driver.get(f"{self.url}/auth/login")
        time.sleep(2)
        self.driver.find_element(by=By.XPATH, value=user_input).send_keys(user)
        self.driver.find_element(by=By.XPATH, value=pw_input).send_keys(pw)
        self.driver.find_element(by=By.XPATH, value=login_button).click()
        time.sleep(2)
        print("profile logged")

    def save_users(self, *, count: int) -> None:
        next_button = "/html/body/div[1]/div/div[1]/main/div/div/div[1]/div/div[4]/button[12]"
        element_button = self.driver.find_element(by=By.CLASS_NAME, value='next')
        page_count = 0
        while element_button.is_enabled() and count > 0:
            try:
                page_count += 1
                time.sleep(2)
                users_list = self.driver.find_elements(By.CLASS_NAME, value="person-card")
                for _user in users_list:
                    if not count > 0:
                        break
                    user_url = _user.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
                    user_id = user_url.split("/")[-1]
                    status = _user.find_element(
                        by=By.CSS_SELECTOR,
                        value=".person-card__name svg"
                    ).value_of_css_property("fill")
                    status = True if status.__contains__("65") else False
                    self.db.create_or_update(external_id=user_id, status=str(status))
                    count -= 1
                time.sleep(2)
                self.driver.find_element(by=By.XPATH, value=next_button).click()
                element_button = self.driver.find_element(by=By.CLASS_NAME, value='next')
            except Exception as e:
                print("Error get users page", page_count, e)
                break
