from playwright.sync_api import Page

class LoginPageObject():

    def __init__(self, page: Page):
        self.page = page

    def login_flow(self, email, password):
        page = self.page
        page.click("#login-holder > a")
        page.fill("#email", email)
        page.fill("#password", password)
        page.click("#login-button")

    def check_member_rank_at_my_page(self):
        page = self.page
        return page.text_content("#rank")
