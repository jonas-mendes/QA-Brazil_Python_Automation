import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Localizadores
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[1]/div[3]/div[1]/button")
    comfort_option = (By.XPATH, "//div[contains(@class, 'tcard')]//div[text()='Comfort']")
    phone_button = (By.CLASS_NAME, 'np-button')
    phone_input = (By.ID, 'phone')
    phone_next_button = (By.XPATH, "//button[contains(text(), 'Próximo')]")
    sms_code_input = (By.ID, 'code')
    sms_confirm_button = (By.XPATH, "//button[contains(text(), 'Confirmar')]")
    payment_button = (By.CLASS_NAME, 'pp-button')
    add_card_button = (By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]")
    card_number_input = (By.ID, 'number')
    card_code_input = (By.CSS_SELECTOR, '.card-input#code')
    card_add_button = (By.XPATH, "//button[contains(text(), 'Adicionar')]")
    close_payment_modal_button = (By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[1]/button")
    comment_input = (By.ID, 'comment')
    blanket_switch = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div")
    ice_cream_counter_plus = (By.CSS_SELECTOR, '.counter-plus')
    ice_cream_counter_value = (By.CSS_SELECTOR, '.counter-value')
    final_request_taxi_button = (By.XPATH, "//button[contains(@class, 'smart-button')]")
    car_search_modal = (By.CSS_SELECTOR, '.order-header-title')
    comfort_selected = (By.CSS_SELECTOR, '.tcard.active')
    phone_configured = (By.CSS_SELECTOR, '.np-text')
    card_added = (By.CSS_SELECTOR, '.pp-value')
    blanket_enabled = (By.CSS_SELECTOR, '.switch.active')

    # Métodos
    def set_route(self, address_from, address_to):
        from_element = self.wait.until(EC.element_to_be_clickable(self.from_field))
        from_element.clear()
        from_element.send_keys(address_from)

        to_element = self.wait.until(EC.element_to_be_clickable(self.to_field))
        to_element.clear()
        to_element.send_keys(address_to)

        # Clica no botão para pedir táxi
        self.wait.until(EC.element_to_be_clickable(self.request_taxi_button)).click()

    def get_from_field(self):
        return self.wait.until(EC.visibility_of_element_located(self.from_field)).get_attribute('value')

    def get_to_field(self):
        return self.wait.until(EC.visibility_of_element_located(self.to_field)).get_attribute('value')

    def select_comfort_tariff(self):
        comfort_element = self.wait.until(EC.element_to_be_clickable(self.comfort_option))
        # Verifica se já está selecionado antes de clicar
        if 'tcard-active' not in comfort_element.find_element(By.XPATH, '..').get_attribute('class'):
            comfort_element.click()

    def is_comfort_selected(self):
        try:
            comfort_element = self.wait.until(EC.presence_of_element_located(self.comfort_option))
            parent = comfort_element.find_element(By.XPATH, '..')
            return 'tcard-active' in parent.get_attribute('class')
        except:
            return False

    def open_phone_modal(self):
        self.wait.until(EC.element_to_be_clickable(self.phone_button)).click()

    def fill_phone_number(self, phone_number):
        self.wait.until(EC.visibility_of_element_located(self.phone_input)).send_keys(phone_number)

    def click_phone_next_button(self):
        self.wait.until(EC.element_to_be_clickable(self.phone_next_button)).click()

    def fill_sms_code(self, code):
        self.wait.until(EC.visibility_of_element_located(self.sms_code_input)).send_keys(code)

    def click_sms_confirm_button(self):
        self.wait.until(EC.element_to_be_clickable(self.sms_confirm_button)).click()

    def is_phone_configured(self):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.phone_configured))
            return element.is_displayed()
        except:
            return False

    def open_payment_modal(self):
        self.wait.until(EC.element_to_be_clickable(self.payment_button)).click()

    def click_add_card_button(self):
        self.wait.until(EC.element_to_be_clickable(self.add_card_button)).click()

    def fill_card_number(self, card_number):
        self.wait.until(EC.visibility_of_element_located(self.card_number_input)).send_keys(card_number)

    def fill_card_code(self, card_code):
        element = self.wait.until(EC.visibility_of_element_located(self.card_code_input))
        element.send_keys(card_code)

    def remove_focus_from_cvv(self):
        # Simula o usuário pressionando Tab para remover o foco do campo CVV
        element = self.wait.until(EC.visibility_of_element_located(self.card_code_input))
        element.send_keys(Keys.TAB)

    def click_add_card_submit_button(self):
        self.wait.until(EC.element_to_be_clickable(self.card_add_button)).click()

    def click_close_payment_modal(self):

        time.sleep(2)
        # Fechar o modal de pagamento usando o localizador correto
        self.wait.until(EC.element_to_be_clickable(self.close_payment_modal_button)).click()

    def is_card_added(self):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.card_added))
            return element.is_displayed()
        except:
            return False

    def fill_comment(self, comment):
        self.wait.until(EC.visibility_of_element_located(self.comment_input)).send_keys(comment)

    def get_comment(self):
        return self.wait.until(EC.visibility_of_element_located(self.comment_input)).get_attribute('value')

    def toggle_blanket_and_handkerchiefs(self):
        # Encontra o elemento switch e clica nele
        switch_element = self.wait.until(EC.element_to_be_clickable(self.blanket_switch))
        self.driver.execute_script("arguments[0].click();", switch_element)

    def is_blanket_and_handkerchiefs_enabled(self):
        try:
            switch_element = self.wait.until(EC.presence_of_element_located(self.blanket_switch))
            return switch_element.is_selected()
        except:
            return False

    def add_ice_creams(self, count):
        for _ in range(count):
            self.wait.until(EC.element_to_be_clickable(self.ice_cream_counter_plus)).click()

    def get_ice_cream_count(self):
        return self.wait.until(EC.visibility_of_element_located(self.ice_cream_counter_value)).text

    def click_request_taxi_button(self):
        self.wait.until(EC.element_to_be_clickable(self.final_request_taxi_button)).click()

    def is_car_search_modal_visible(self):
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.car_search_modal))
            return 'Buscar carro' in element.text or 'Procurando carro' in element.text
        except:
            return False