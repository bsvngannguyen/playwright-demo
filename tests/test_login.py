from playwright.sync_api import Page, expect
import re

# ================= CONSTANTS =================

EMAIL = "#mail_address"
PASSWORD = "#password"
LOGIN_BTN = "#login_button"

FORGOT_PASSWORD_LINK = ".smart__forget__link"
REGISTER_LINK = "text=新規登録"

ERROR_TEXT_1 = "text=メールアドレスが正しくありません"
ERROR_TEXT_2 = "text=パスワードは8文字以上32文字以下で指定してください"

REQUIRED_TEXT_1 = "text=メールアドレスを入力してください"
REQUIRED_TEXT_2 = "text=パスワードを入力してください"

ERROR_MESSAGE = "text=ログインできませんでした"

EMAIL_OK = "ngantest112233@gmail.com"
PW_OK = "ngantest123"

PW_SHORT = "1234567"
PW_LONG = "a" * 33
PW_INVALID = "wrongpass"

LOGIN_URL = "https://playwright-demo.eventos.work/web/portal/529/event/3988/users/login"
RESET_PASSWORD_URL_PART = "password"
REGISTER_URL_PART = "register"


# ================= COMMON =================

def open_login(page: Page):
    page.goto(LOGIN_URL)


# ================= A. UI DISPLAY =================

def test_login_01_url(page: Page):
    open_login(page)
    expect(page).to_have_url(LOGIN_URL)


def test_login_02_login_button(page: Page):
    open_login(page)
    expect(page.locator(LOGIN_BTN)).to_be_visible()


def test_login_03_email_field(page: Page):
    open_login(page)
    expect(page.locator(EMAIL)).to_be_visible()


def test_login_04_password_field(page: Page):
    open_login(page)
    expect(page.locator(PASSWORD)).to_be_visible()


# ================= B. EMAIL VALIDATION =================

def test_login_05_email_invalid(page: Page):
    open_login(page)

    invalid_emails = [
        "abc@gmail",
        "abc!@gmail.com",
        "test.abc",
        "@gmail.com",
        "ａｂｃ＠gmail.com"
    ]

    for mail in invalid_emails:
        page.fill(EMAIL, mail)
        page.fill(PASSWORD, PW_OK)
        page.click(LOGIN_BTN)

        expect(page.locator(ERROR_TEXT_1)).to_be_visible()


def test_login_06_email_required(page: Page):
    open_login(page)

    page.fill(PASSWORD, PW_OK)
    page.click(LOGIN_BTN)

    expect(page.locator(REQUIRED_TEXT_1)).to_be_visible()


# ================= C. PASSWORD VALIDATION =================

def test_login_07_password_short(page: Page):
    open_login(page)

    page.fill(EMAIL, EMAIL_OK)
    page.fill(PASSWORD, PW_SHORT)
    page.click(LOGIN_BTN)

    expect(page.locator(ERROR_TEXT_2)).to_be_visible()


def test_login_08_password_required(page: Page):
    open_login(page)

    page.fill(EMAIL, EMAIL_OK)
    page.click(LOGIN_BTN)

    expect(page.locator(REQUIRED_TEXT_2)).to_be_visible()


def test_login_09_password_long(page: Page):
    open_login(page)

    page.fill(EMAIL, EMAIL_OK)
    page.fill(PASSWORD, PW_LONG)
    page.click(LOGIN_BTN)

    expect(page.locator(ERROR_TEXT_2)).to_be_visible()


# ================= D. LOGIN RESULT =================

def test_login_10_wrong_password(page: Page):
    open_login(page)

    page.fill(EMAIL, EMAIL_OK)
    page.fill(PASSWORD, PW_INVALID)
    page.click(LOGIN_BTN)

    expect(page.locator(ERROR_MESSAGE)).to_be_visible()


def test_login_11_success(page: Page):
    open_login(page)

    page.fill(EMAIL, EMAIL_OK)
    page.fill(PASSWORD, PW_OK)
    page.click(LOGIN_BTN)

    # redirect away from login page
    expect(page).not_to_have_url(LOGIN_URL)


# ================= E. LINKS =================

# ---------- Forgot Password (UI) ----------
def test_login_12_forgot_password_ui(page: Page):
    open_login(page)

    link = page.locator(FORGOT_PASSWORD_LINK)

    expect(link).to_be_visible()
    expect(link).to_have_css("text-decoration-line", "underline")


# ---------- Forgot Password (Click) ----------
def test_login_13_forgot_password_click(page: Page):
    open_login(page)

    page.locator(FORGOT_PASSWORD_LINK).click()

    expect(page).not_to_have_url(LOGIN_URL)


# ---------- Register (UI) ----------
def test_login_14_register_ui(page: Page):
    open_login(page)

    link = page.get_by_text("新規登録")

    expect(link).to_be_visible()


# ---------- Register (Click) ----------
def test_login_15_register_click(page: Page):
    open_login(page)

    page.get_by_text("新規登録").click()

    expect(page).not_to_have_url(LOGIN_URL)