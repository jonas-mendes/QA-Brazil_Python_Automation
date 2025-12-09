import time

import data
import helpers
from selenium import webdriver
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # Verifica se o servidor está funcionando
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.")

        # Configuração do driver com logging (para recuperar o código SMS)
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get(data.URBAN_ROUTES_URL)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_set_route(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert routes_page.get_from_field() == data.ADDRESS_FROM
        assert routes_page.get_to_field() == data.ADDRESS_TO

    def test_select_plan(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_comfort_tariff()
        # Verifica se a tarifa Comfort está selecionada
        assert routes_page.is_comfort_selected() == True

    def test_fill_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.open_phone_modal()
        routes_page.fill_phone_number(data.PHONE_NUMBER)
        routes_page.click_phone_next_button()

        # Obtém e preenche o código SMS
        code = helpers.retrieve_phone_code(self.driver)
        routes_page.fill_sms_code(code)
        routes_page.click_sms_confirm_button()

        # Verifica se o telefone foi configurado
        assert routes_page.is_phone_configured() == True

    def test_fill_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.open_payment_modal()
        routes_page.click_add_card_button()
        routes_page.fill_card_number(data.CARD_NUMBER)
        routes_page.fill_card_code(data.CARD_CODE)

        # Remove o foco do campo CVV para habilitar o botão Adicionar
        routes_page.remove_focus_from_cvv()

        routes_page.click_add_card_submit_button()
        time.sleep(5)
        routes_page.click_close_payment_modal()

        # Verifica se o cartão foi adicionado
        assert routes_page.is_card_added() == True

    def test_comment_for_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.fill_comment(data.MESSAGE_FOR_DRIVER)
        assert routes_page.get_comment() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.toggle_blanket_and_handkerchiefs()
        assert routes_page.is_blanket_and_handkerchiefs_enabled() == True

    def test_order_2_ice_creams(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_ice_creams(2)
        assert routes_page.get_ice_cream_count() == '2'

    def test_car_search_model_appears(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_request_taxi_button()
        assert routes_page.is_car_search_modal_visible() == True