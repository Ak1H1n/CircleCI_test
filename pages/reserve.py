from playwright.sync_api import Page
from datetime import datetime, timedelta


class ReservePageObject():

    def __init__(self, page: Page):
        self.new_page = page

    def get_term_and_1_head_count_total_bill(self):
        new_page = self.new_page
        term_and_1_head_count_total_bill = new_page.text_content("#total-bill")
        term_and_1_head_count_total_bill = term_and_1_head_count_total_bill.replace("円", "").replace(",", "")
        term_and_1_head_count_total_bill = int(term_and_1_head_count_total_bill) * 2
        return term_and_1_head_count_total_bill

    def get_total_bill(self):
        new_page = self.new_page
        total_bill = new_page.text_content("#total-bill")
        total_bill = total_bill.replace("円", "").replace(",", "")
        total_bill = int(total_bill)
        return total_bill

    def tomorrow_calc_and_input_date(self):
        # new_page = self.new_page
        tomorrow = datetime.today() + timedelta(days=1)
        tomorrow = datetime.strftime(tomorrow, '%Y/%m/%d')
        # new_page.fill("#date", tomorrow)
        # new_page.press("#date", "Escape")
        return tomorrow

    def input_date(self):
        new_page = self.new_page
        tomorrow = ReservePageObject(new_page).tomorrow_calc_and_input_date()
        new_page.fill("#date", tomorrow)
        new_page.press("#date", "Escape")
        return tomorrow


    def head_count_10_over_is_error(self):
        new_page = self.new_page
        new_page.click("#head-count")
        return new_page.text_content("#reserve-form > div > div.col-lg-6.ml-auto > div:nth-child(3) > div > div.invalid-feedback")

    def input_term_days(self, term):
        new_page = self.new_page
        new_page.fill("#term", term)

    def input_head_count(self, head_count):
        self.new_page.fill("#head-count", head_count)
        return head_count

    def select_contact(self, contact):
        self.new_page.select_option("#contact", contact)

    def click_submit_button(self):
        self.new_page.click("#submit-button")

    def term_date_format(self):
        new_page = self.new_page
        tomorrow_format = ReservePageObject(new_page).tomorrow_calc_and_input_date()
        # tomorrow_format = tomorrow_format.replace("/", "年").replace("/", "月").replace("/", "日")
        datetime.strptime(tomorrow_format, '%Y年%m月%d日')
        return tomorrow_format

    def confirm_click_button(self):
        self.new_page.click("#confirm > div:nth-child(2) > div > button")

    def close_click_button(self):
        self.new_page.click("#success-modal > div > div > div.modal-footer > button")