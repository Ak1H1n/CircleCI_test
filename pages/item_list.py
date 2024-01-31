from playwright.sync_api import Page
from pages import form

class ItemListPageObject(FormPageObject):

    # 初期化
    def __init__(self, page: Page):
        self.page = page

    def sort_out_of_stock(self):
        self.page.click("#d1")
        self.page.click("#sortItem > div > div:nth-child(3) > div > a:nth-child(2)")
    
    def item_cartin(self):
        self.page.click("a.cart-btn")

    def wait_load(self):
        self.page.wait_for_selector("body > div.loader", state="hidden")

    def wait_cart_in(self):
        self.page.wait_for_selector("#toastMe > div > div",state="visible")
        self.page.click("#sticker > div > div.row > div.col-lg-12.col-sm-12.text-center > div > nav > ul > li:nth-child(1)")

    def item_1_click(self):
        self.page.click("#tableProd > div:nth-child(1) > div > div > a > img")