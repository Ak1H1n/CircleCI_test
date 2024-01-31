from playwright.sync_api import Page


class ConfirmPageObject:

    # 初期化
    def __init__(self, page: Page):
        self.page = page

    # 合計金額の確認
    def get_total_bill(self):
        return self.page.text_content("#total-bill")