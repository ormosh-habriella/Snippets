import pytest
from MainApp.factories import TagFactory
import pytest
from MainApp.factories import UserFactory, SnippetFactory
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def user():
    """Фикстура для создания пользователя"""
    return UserFactory()

@pytest.fixture
def tag_factory():
    def _create_tags(names):
        tags = []
        for name in names:
            tags.append(TagFactory(name=name))
        return tags

    return _create_tags

@pytest.fixture
def snippets_factory():
    def _create_snippets(n, **kwargs):
        snippets = SnippetFactory.create_batch(n=n, **kwargs)
        return snippets

    return _create_snippets


# Фикстура для настройки и очистки драйвера браузера
@pytest.fixture(scope="session")
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()