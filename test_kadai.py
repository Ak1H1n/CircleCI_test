from playwright.sync_api import Page
import pytest
from datetime import datetime, timedelta

class TestHotelPlanisphere(object):

    @pytest.fixture(scope="function", autouse=True)
    def page_fixture(self, page: Page):
        self.page = page
        self.page.goto("https://hotel.testplanisphere.dev/ja/reserve.html?plan-id=0", wait_until = "networkidle")
        yield
        self.page.close()

    @pytest.fixture(scope="session", autouse=True)
    def browser_context_args(self, browser_context_args):
        return {**browser_context_args, "viewport": {"width": 1520, "height": 1080, }}

    # 当日以前の日付は予約できないこと
    def test_before_today(self):
        page = self.page

        # 前日を宿泊日として入力
        one_day_before = datetime.today() - timedelta(days=1)
        one_day_before = datetime.strftime(one_day_before, '%Y/%m/%d')
        page.fill("#date", one_day_before)
        page.press("#date", "Tab")

        # 宿泊日数入力
        page.fill("#term", "1")

        # 宿泊人数入力
        page.fill("#head-count", "2")

        # 朝食バイキングの選択
        checked = page.is_checked("#breakfast")
        if checked is False:
            page.check("#breakfast")

        # 氏名の入力
        page.fill("#username", "テスト太郎")

        # 連絡の有無の「希望しない」を選択
        page.select_option("#contact", label="希望しない")

        # 「予約内容を確認する」ボタンをクリック
        page.click("#submit-button")
        # 待機
        page.wait_for_load_state()

        # スクリーンショット
        page.screenshot(path="./output/test_before_today.png")
        # 宿泊日を前日に設定した場合のエラーメッセージの確認
        assert page.text_content("#date ~ div") == "翌日以降の日付を入力してください。", "当日以前の宿泊日では予約できません"

    # 氏名欄が空欄だと予約ができないこと
    def test_name_space_blank(self):
        page = self.page

        # 翌日を宿泊日として入力
        one_day_after = datetime.today() + timedelta(days=1)
        one_day_after = datetime.strftime(one_day_after, '%Y/%m/%d')
        page.fill("#date", one_day_after)
        page.press("#date", "Tab")

        # 宿泊日数入力
        page.fill("#term", "3")

        # 宿泊人数入力
        page.fill("#head-count", "4")

        # 昼からチェックインプランの選択
        checked = page.is_checked("#early-check-in")
        if checked is False:
            page.check("#early-check-in")

        # 氏名を空欄にする
        page.fill("#username", "")

        # 連絡の有無の「希望しない」を選択
        page.select_option("#contact", label="希望しない")

        # 「予約内容を確認する」ボタンをクリック
        page.click("#submit-button")
        # 待機
        page.wait_for_load_state()

        # スクリーンショット
        page.screenshot(path="./output/test_name_space_blank.png")
        # 氏名欄を空欄にした場合のエラーメッセージの確認
        assert page.text_content("#username ~ div") == "このフィールドを入力してください。", "氏名欄が空欄だと予約できません"

    # 当日から三か月以上先の日付は予約できないこと
    def test_three_month_after(self):
        page = self.page

        # 三か月（91日）後を宿泊日として入力
        three_month_after = datetime.today() + timedelta(days=91)
        three_month_after = datetime.strftime(three_month_after, '%Y/%m/%d')
        page.fill("#date", three_month_after)
        page.press("#date", "Tab")

        # 宿泊日数入力
        page.fill("#term", "2")

        # 宿泊人数入力
        page.fill("#head-count", "3")

        # 朝食バイキングの選択
        checked = page.is_checked("#breakfast")
        if checked is False:
            page.check("#breakfast")

        # 氏名の入力
        page.fill("#username", "テスト二郎")

        # 連絡の有無の「希望しない」を選択
        page.select_option("#contact", label="希望しない")

        # 「予約内容を確認する」ボタンをクリック
        page.click("#submit-button")
        # 待機
        page.wait_for_load_state()

        # スクリーンショット
        page.screenshot(path="./output/test_three_month_after.png")
        # 宿泊日を三か月以上先に設定した場合のエラーメッセージの確認
        assert page.text_content("#date ~ div") == "3ヶ月以内の日付を入力してください。", "三か月（91日）以上先の宿泊日では予約できません"