from playwright.sync_api import Page, expect
import re

# ================= LOGIN INFO =================
URL = "https://admin.odakyu.bravesoft.vn/account-management"
EMAIL_OK = "kimtran@bravesoft.com.vn"
PASSWORD_OK = "brave0404"


# ================= HELPER =================

def setup_register_dialog(page: Page): 
    # 1. Open login page
    page.goto(URL)
    # 2. Fill email
    page.locator('input[name="email"]').fill(EMAIL_OK)
    # 3. Fill password
    page.locator("#password").fill(PASSWORD_OK)
    # 4. Click login
    page.get_by_role("button", name="ログイン").click()
    page.wait_for_load_state("networkidle")
    # 6. Click 新規追加
    page.get_by_role("button", name="新規追加").click()
    
    # Thêm chờ cho dialog hiển thị để tránh timeout ở các test case sau
    page.get_by_text("新規アカウント追加").wait_for(state="visible") 


# ================= TEST CASES =================

# TC1: Verify title
def test_register_01_title(page: Page):
    setup_register_dialog(page)
    expect(page.get_by_text("新規アカウント追加")).to_be_visible()


# TC2: Verify URL
def test_register_02_url(page: Page):
    setup_register_dialog(page)
    expect(page).to_have_url(re.compile(r".*/account-management$"))
    

# TC3: Verify account name label
def test_register_03_account_name_label(page: Page):
    setup_register_dialog(page)
    expect(page.get_by_text(re.compile(r"アカウント名\s*\*\s*（255文字以内）"))).to_be_visible()
    

# TC4: Check nhập và hiển thị text ở ô アカウント名
def test_register_04_account_name_input(page: Page):
    setup_register_dialog(page)
    page.locator("input[name='userName']").fill("きむがん")
    expect(page.locator("input[name='userName']")).to_have_value("きむがん")


# TC5: Verify mail label
def test_register_05_email_label(page: Page):
    setup_register_dialog(page)
    expect(page.get_by_text(re.compile(r"メールアドレス\s*\*\s*"))).to_be_visible()
    

# TC6: Nhập email đúng định dạng vào 「メールアドレス」 và xác nhận hiển thị
def test_register_06_email_input_valid(page: Page):
    setup_register_dialog(page)
    page.locator("input[name='email']").fill("ngannguyen@bravesoft.com.vn")
    expect(page.locator("input[name='email']")).to_have_value("ngannguyen@bravesoft.com.vn")


# TC7: Check label パスワード
def test_register_07_password_label(page: Page):
    setup_register_dialog(page)
    expect(page.get_by_text(re.compile(r"パスワード\s*\*\s*（半角英数字 8文字以上32文字以内）"))).to_be_visible()


# TC8: Check placeholder của パスワード
def test_register_08_password_placeholder(page: Page):
    setup_register_dialog(page)
    expect(page.locator("input[name='password']")).to_have_attribute("placeholder", "**********")


# TC9: Nhập mật khẩu vào 「パスワード」sẽ hiện dạng mask
def test_register_09_password_mask(page: Page):
    setup_register_dialog(page)
    page.locator("input[name='password']").fill("bravesoft123")
    expect(page.locator("input[name='password']")).to_have_attribute("type", "password")
    expect(page.locator("input[name='password']")).to_have_value("bravesoft123")
    

# TC10: Check select box 権限
def test_register_10_role_select_default(page: Page):
    setup_register_dialog(page)
    expect(page.locator(".label-title:has-text('権限')")).to_be_visible()
    page.get_by_role("combobox").nth(1).click()
    expect(page.get_by_role("combobox").nth(1)).to_be_visible()
    
    
# TC11: Check select マスター管理者
def test_register_11_select_master_admin(page: Page):
    setup_register_dialog(page)
    page.get_by_role("combobox").nth(1).click() # Sử dụng nth(1)
    page.get_by_text("マスター管理者").click()
    expect(page.get_by_role("combobox").nth(1)).to_contain_text("マスター管理者")


# TC12: Check select テナント管理者
def test_register_12_select_tenant_admin(page: Page):
    setup_register_dialog(page)
    page.get_by_role("combobox").nth(1).click() # Sử dụng nth(1)
    page.get_by_text("テナント管理者").click()
    expect(page.get_by_role("combobox").nth(1)).to_contain_text("テナント管理者")
    

# TC13: Check không thể chọn đồng thời 「マスター管理者」và「テナント管理者」
def test_register_13_role_single_selection_only(page: Page):
    setup_register_dialog(page)
    page.get_by_role("combobox").nth(1).click() # Sử dụng nth(1)
    page.get_by_text("マスター管理者").click()
    expect(page.get_by_role("combobox").nth(1)).to_contain_text("マスター管理者")
    
    page.get_by_role("combobox").nth(1).click() # Sử dụng nth(1)
    page.get_by_text("テナント管理者").click()
    expect(page.get_by_role("combobox").nth(1)).to_contain_text("テナント管理者")
    expect(page.get_by_role("combobox").nth(1)).not_to_contain_text("マスター管理者")


# TC14: Check チケット組成時のポイント付与パラメータの変更権限
def test_register_14_point_param_permission_visible_only_for_tenant_admin(page: Page):
    setup_register_dialog(page)
    label_text = "チケット組成時のポイント付与パラメータの変更権限"
    
    page.get_by_role("combobox").nth(1).click() # Sử dụng nth(1)
    page.get_by_text("マスター管理者").click()
    expect(page.get_by_text(label_text)).not_to_be_visible()
    
    page.get_by_role("combobox").nth(1).click() # Sử dụng nth(1)
    page.get_by_text("テナント管理者").click()
    expect(page.get_by_text(label_text)).to_be_visible()
    expect(page.get_by_text("有")).to_be_visible()
    expect(page.get_by_text("無")).to_be_visible()


# TC15: Nếu chọn 「有」 thì 「有」 ở trạng thái checked
def test_register_15_radio_yes_checked(page: Page):
    setup_register_dialog(page)
    page.get_by_role("combobox").nth(1).click() # Sử dụng nth(1)
    page.get_by_text("テナント管理者").click()
    page.get_by_role("radio", name="有").click()
    expect(page.get_by_role("radio", name="有")).to_be_checked()


# TC16: Nếu chọn 「無」 thì 「無」 ở trạng thái checked
def test_register_16_radio_no_checked(page: Page):
    setup_register_dialog(page)
    page.get_by_role("combobox").nth(1).click() # Sử dụng nth(1)
    page.get_by_text("テナント管理者").click()
    page.get_by_role("radio", name="無").click()
    expect(page.get_by_role("radio", name="無")).to_be_checked()


# TC17: Check không thể chọn đồng thời 「有」 và 「無」
def test_register_17_radio_mutually_exclusive(page: Page):
    setup_register_dialog(page)
    page.get_by_role("combobox").nth(1).click() # Sử dụng nth(1)
    page.get_by_text("テナント管理者").click()
    page.get_by_role("radio", name="有").click()
    expect(page.get_by_role("radio", name="有")).to_be_checked()
    expect(page.get_by_role("radio", name="無")).not_to_be_checked()
    page.get_by_role("radio", name="無").click()
    expect(page.get_by_role("radio", name="無")).to_be_checked()
    expect(page.get_by_role("radio", name="有")).not_to_be_checked()