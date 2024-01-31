from playwright.sync_api import Page


class FormPageObject:

    # 初期化
    def __init__(self, page: Page):
        self.page = page

    # 待機
    def form_wait_display(self):
        self.page.wait_for_load_state("networkidle")

    # 宿泊日の入力
    def input_date(self, date):
        self.page.fill("#date", date)
        self.page.press("#date", "Tab")

    # 宿泊日数の入力
    def input_term_day(self, term_day):
        self.page.fill("#term", term_day)

    # 宿泊人数の入力
    def input_number_of_people(self, number_of_people):
        self.page.fill("#head-count", number_of_people)

    # プランの選択
    def select_plan(self, breakfast, early, sight):
        plan_breakfast = self.page.locator("#breakfast")
        if plan_breakfast.is_checked() != breakfast:
            plan_breakfast.click()
        plan_early = self.page.locator("#early-check-in")
        if plan_early.is_checked() != early:
            plan_early.click()
        plan_sight = self.page.locator("#sightseeing")
        if plan_sight.is_checked() != sight:
            plan_sight.click()

    # 氏名の入力
    def input_name(self, name):
        self.page.fill("#username", name)

    # 確認の連絡の有無
    def select_contact(self, contact, tel, email):
        self.page.select_option("#contact", label=contact)

        if contact == "電話でのご連絡":
            self.page.fill("#tel", tel)
        elif contact == "メールでのご連絡":
            self.page.fill("#email", email)

    # 「予約内容を確認する」ボタンをクリック
    def click_submit(self):
        self.page.click("#submit-button")