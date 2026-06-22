import pytest
from selenium import webdriver
from selenium.webdriver.edge.options import Options


@pytest.fixture
def driver():
    """Khởi tạo và đóng trình duyệt Microsoft Edge cho mỗi test case."""
    options = Options()
    options.add_argument("--start-maximized")
    # Nếu chạy trên máy không có giao diện, bỏ dấu # dòng dưới:
    # options.add_argument("--headless=new")

    browser = webdriver.Edge(options=options)
    browser.implicitly_wait(5)
    yield browser
    browser.quit()
