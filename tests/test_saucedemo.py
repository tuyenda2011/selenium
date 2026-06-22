from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"


def login(driver):
    """Hàm dùng chung để đăng nhập vào SauceDemo."""
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    username_input = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    username_input.clear()
    username_input.send_keys(USERNAME)

    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys(PASSWORD)

    driver.find_element(By.ID, "login-button").click()
    wait.until(EC.url_contains("inventory.html"))


def test_login_success(driver):
    """TC01: Kiểm thử đăng nhập thành công."""
    login(driver)

    page_title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )

    assert "inventory.html" in driver.current_url
    assert page_title.text == "Products"


def test_add_product_to_cart(driver):
    """TC02: Kiểm thử thêm sản phẩm vào giỏ hàng."""
    login(driver)
    wait = WebDriverWait(driver, 10)

    product_name = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()='Sauce Labs Backpack']"))
    ).text

    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

    cart_badge = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert cart_badge.text == "1"

    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    cart_product = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name"))
    )

    assert cart_product.text == product_name


def test_logout_success(driver):
    """TC03: Kiểm thử đăng xuất thành công."""
    login(driver)
    wait = WebDriverWait(driver, 10)

    menu_button = wait.until(
        EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
    )
    menu_button.click()

    logout_link = wait.until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    )
    logout_link.click()

    username_input = wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )

    assert username_input.is_displayed()
    assert driver.current_url == BASE_URL


def test_login_failure(driver):
    """TC04: Kiểm thử đăng nhập thất bại với sai mật khẩu."""
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    username_input = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    username_input.clear()
    username_input.send_keys(USERNAME)

    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys("wrong_password")

    driver.find_element(By.ID, "login-button").click()

    error_message = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )
    assert "Username and password do not match any user in this service" in error_message.text


def test_remove_product_from_cart(driver):
    """TC05: Kiểm thử xóa sản phẩm khỏi giỏ hàng."""
    login(driver)
    wait = WebDriverWait(driver, 10)

    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

    cart_badge = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert cart_badge.text == "1"

    driver.find_element(By.ID, "remove-sauce-labs-backpack").click()

    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    badges = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(badges) == 0


def test_checkout_workflow(driver):
    """TC06: Kiểm thử quy trình thanh toán (Checkout)."""
    login(driver)
    wait = WebDriverWait(driver, 10)

    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Test")
    driver.find_element(By.ID, "last-name").send_keys("User")
    driver.find_element(By.ID, "postal-code").send_keys("12345")

    driver.find_element(By.ID, "continue").click()

    wait.until(EC.url_contains("checkout-step-two.html"))
    summary_total_label = driver.find_element(By.CLASS_NAME, "summary_total_label")
    assert "Total" in summary_total_label.text
