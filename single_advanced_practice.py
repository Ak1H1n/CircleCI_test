from playwright.sync_api import Page
import pytest
from datetime import datetime, timedelta
from utilities.read_csv import read_csv_data
import os

# file = os.environ.get("matrix.file")
# file_name = int(os.environ.get("filename"))

class TestHotelPlan(object):


    # とりあえず確認用にPlaywright実行用ワークフローに直接環境変数を設定する

    # datalist = read_csv_data(f'.datadriven/test_data_{file}.csv')
    # datalist = read_csv_data('./datadriven/address_new.csv')
    # datalist = read_csv_data(f'./datadriven/data_'+str(file_name)+'.csv')
    datalist = read_csv_data('./datadriven/address.csv')

    @pytest.fixture(scope="function", autouse=True)
    def page_fixture(self,  page: Page):
        self.page = page
        self.page.goto("https://hotel.testplanisphere.dev/ja/index.html", wait_until = "networkidle")
        yield
        self.page.close()

    @pytest.fixture(scope="session", autouse=True)
    def browser_context_args(self, browser_context_args):
        return {**browser_context_args, "viewport": {"width": 1520, "height": 1080, }}

    @pytest.mark.parametrize("case_no, email_address, password", datalist)
    def test_hotel_login_and_booking_normal_rank(self, case_no, email_address, password):
        page = self.page
        page.click("#login-holder > a")
        page.fill("#email", email_address)
        page.fill("#password", password)
        page.click("#login-button")
        page.screenshot(path="./output/check_member_rank_at_my_page"+str(case_no)+".png")
        page.wait_for_load_state()
        assert page.text_content("#rank") == "一般会員", "会員ランクが一般会員ではありません"

        page.wait_for_load_state()

        page.click("#navbarNav > ul > li:nth-child(2) > a")

        page.click("body > div > div:nth-child(2) > div > div > div.card-body > a")

        page.wait_for_timeout(1000)
        new_page = page.context.pages[-1]


        #おすすめプランの予約フォーム
        new_page.bring_to_front()

        new_page.wait_for_selector("#total-bill")
        tomorrow = datetime.today() + timedelta(days=1)
        tomorrow = datetime.strftime(tomorrow, '%Y/%m/%d')

        term_and_1_head_count_total_bill = new_page.text_content("#total-bill")
        term_and_1_head_count_total_bill = term_and_1_head_count_total_bill.replace("円", "").replace(",", "")
        term_and_1_head_count_total_bill = int(term_and_1_head_count_total_bill) * 2

        new_page.fill("#term", "1")

        new_page.fill("#head-count", "10")
        # エラーメッセージの確認のためにtabキーを押下する
        new_page.keyboard.press("Tab")

        new_page.screenshot(path="./output/head_count_10_over_is_error.png")
        new_page.click("#head-count")

        assert new_page.text_content("#reserve-form > div > div.col-lg-6.ml-auto > div:nth-child(3) > div > div.invalid-feedback") == "9以下の値を入力してください。", "9以下の数値を入力してくださいのエラーが表示されていません"

        new_page.fill("#head-count", "2")

        # この辺にコンタクトの選択文
        new_page.select_option("#contact", "no")
        # 合計金額の取得のためにクリック

        new_page.click("#total-bill")
        total_bill = new_page.text_content("#total-bill")
        total_bill = total_bill.replace("円", "").replace(",", "")
        total_bill = int(total_bill)
        new_page.screenshot(path="./output/compare_total_bill.png")

        assert term_and_1_head_count_total_bill == total_bill, "宿泊数1、人数1の2倍の金額になっていません"

        new_page.click("#submit-button")
        new_page.wait_for_load_state()
        # # ここに入力値との一致を確認を入れる
        # tomorrow_format = reserve.ReservePageObject(new_page).term_date_format()

        # assert new_page.text_content("#term") == tomorrow_format+"～", "宿泊日数が入力値と一致してません"
        # # 2024年1月10日 〜 2024年1月11日 1泊
        # assert new_page.text_content("#head-count") == ""+"名様", "宿泊日数"



        # new_page.screenshot(path="./output/reserve_confirm.png")

        # # プラン選択ページを呼び出す
        # page.bring_to_front()
        # page.screenshot(path="./output/complete_close_confirm.png")
        # assert page.url == "https://hotel.testplanisphere.dev/ja/plans.html", "初期画面のプラン選択画面に戻っていません"