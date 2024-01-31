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

    @pytest.mark.parametrize("case_no, date_from, days, headcount, breakfast, early_checkin, sightseeing, username, contact, total,tel_number,email_address", datalist)
    def test_hotel_reservation_data_driven(self, case_no, date_from, days, headcount, breakfast, early_checkin, sightseeing, username, contact, total, tel_number, email_address):

        page = self.page
        form_page = form.FormPageObject(page)
        confirm_page = confirm.ConfirmPageObject(page)

        # 待機
        form_page.form_wait_display()

        # 宿泊日の入力
        form_page.input_date(date_from)

        # 宿泊日数入力
        form_page.input_term_day(days)

        # 宿泊人数入力
        form_page.input_number_of_people(headcount)

        # プランの選択（朝食,昼からチェックイン,観光）
        if breakfast == "あり":
            plan_breakfast = True
        elif breakfast == "なし":
            plan_breakfast = False

        if early_checkin == "あり":
            plan_early = True
        elif early_checkin == "なし":
            plan_early = False

        if sightseeing == "あり":
            plan_sight = True
        elif sightseeing == "なし":
            plan_sight = False

        form_page.select_plan(plan_breakfast, plan_early, plan_sight)

        # 氏名の入力
        form_page.input_name(username)

        # 確認の連絡の有無を選択（"no"、"tel"、"email"から選択,電話を選択した場合は電話番号,メールを選択した場合はメールアドレスを入力）
        form_page.select_contact(contact, tel_number, email_address)

        # 「予約内容を確認する」ボタンをクリック
        form_page.click_submit()

        # 待機
        form_page.form_wait_display()

        # スクリーンショット
        page.screenshot(path="./output/test_hotel_reservation_data_driven_"+str(case_no)+".png")
        # 予約確認画面の合計金額、人数、お名前の確認
        assert confirm_page.get_total_bill() == "合計 "+total+"円（税込み）", "予約確認画面に表示されている合計金額が"+total+"円であること"
        assert confirm_page.get_number_of_people() == headcount+"名様", "予約確認画面に表示されている人数が"+headcount+"人であること"
        assert confirm_page.get_name() == username+"様", "予約確認画面に表示されているお名前が"+username+"様であること"