from playwright.sync_api import Page
import pytest
from pages import form, confirm
from utilities.read_csv import read_csv_data


class TestDataDriven():
    datalist = read_csv_data('./datadriven/reservation.csv')


    @pytest.fixture(scope="function", autouse=True)
    def page_fixture(self, page: Page):
        self.page = page
        self.page.goto("https://hotel.testplanisphere.dev/ja/reserve.html?plan-id=0", wait_until="networkidle")
        yield
        self.page.close()

    @pytest.fixture(scope="session", autouse=True)
    def browser_context_args(self, browser_context_args):
        return {**browser_context_args, "viewport": {"width": 1520, "height": 1080, }}

    def test_input(self):

        page = self.page
        form_page = form.FormPageObject(page)
        confirm_page = confirm.ConfirmPageObject(page)

        # 待機
        form_page.form_wait_display()

        # 宿泊日の入力
        form_page.input_date("2023/12/01")

        # 宿泊日数入力
        form_page.input_term_day("2")

        # 宿泊人数入力
        form_page.input_number_of_people("3")

        # プランの選択（朝食,昼からチェックイン,観光）
        form_page.select_plan(False, False, True)

        # 氏名の入力
        form_page.input_name("テスト三郎")

        # 確認の連絡の有無を選択
        form_page.select_contact("希望しない", "12345678910", "test@example.com")

        # 「予約内容を確認する」ボタンをクリック
        form_page.click_submit()

        # 待機
        form_page.form_wait_display()

        # スクリーンショット
        page.screenshot(path="./output/test_page_object.png")
        # 合計金額の確認
        assert confirm_page.get_total_bill() == "合計 50,250円（税込み）", "予約確認画面に表示されている合計金額が50250円であること"