import requests


def test_regions_list():  # Получение списка регионов
    response = requests.get("https://regions-test.2gis.com/1.0/regions")
    data = response.json()

    assert data["total"] != 0
    assert response.status_code == 200, f"Статус код отличается от 200: {response.status_code}"


test_regions_list()


def test_regions_search():  # Поиск названия региона
    response = requests.get("https://regions-test.2gis.com/1.0/regions?q=Моск")
    data = response.json()

    for item in data["items"]:
        assert item["name"] == "Москва", "Отсутствует Москва в респонсе"
    assert response.status_code == 200, f"Статус код отличается от 200: {response.status_code}"


test_regions_search()


def test_validation_value_search():  # Поиск названия региона менее 3 символов

    response = requests.get("https://regions-test.2gis.com/1.0/regions?q=Мо")
    data = response.json()

    assert response.status_code == 200, f"Статус код отличается от 200: {response.status_code}"
    assert data["error"]["message"] == "Параметр 'q' должен быть не менее 3 символов", \
        f"Фактическая ошибка: {data['error']['message']}"


test_validation_value_search()


def test_combination_with_search():  # Проверка игнорирования прочих параметров при нечетком поиске
    response = requests.get("https://regions-test.2gis.com/1.0/regions?q=Москва&country_code=cz")
    data = response.json()

    assert response.status_code == 200, f"Статус код отличается от 200: {response.status_code}"
    for item in data["items"]:
        assert item["name"] == "Москва", "Москва отсутствует в респонсе"


test_combination_with_search()


def test_country_code_filter():  # Проверка фильтрации по коду страны
    response = requests.get("https://regions-test.2gis.com/1.0/regions?country_code=cz")
    data = response.json()

    for item in data['items']:
        assert item['country']['code'] == 'cz', 'Чехия отсутствует в респонсе'
    assert response.status_code == 200, f"Статус код отличается от 200: {response.status_code}"


test_country_code_filter()


def test_country_code_error_validation():  # Проверка ошибки по коду страны вне перечня допустимых значений
    response = requests.get("https://regions-test.2gis.com/1.0/regions?country_code=test")
    assert response.status_code == 200

    data = response.json()
    assert data["error"]["message"] == "Параметр 'country_code' может быть одним из следующих значений: ru, kg, kz, cz", \
        f"Фактическая ошибка: {data['error']['message']}"


test_country_code_error_validation()


def test_country_code_values_list():  # Проверка фильтрации элементов всех стран по умолчанию по коду страны
    response1 = requests.get("https://regions-test.2gis.com/1.0/regions?page=1&page_size=15")
    assert response1.status_code == 200, f"Статус код отличается от 200: {response1.status_code}"
    data1 = response1.json()
    response2 = requests.get("https://regions-test.2gis.com/1.0/regions?page=2&page_size=15")
    assert response2.status_code == 200, f"Статус код отличается от 200: {response2.status_code}"
    data2 = response2.json()

    codes = set()
    for item in data1['items'] + data2['items']:
        codes.add(item['country']['code'])

    assert codes == {'ru', 'kg', 'kz', 'cz', 'ua'}


test_country_code_values_list()


def test_set_page_size_5():  # Установка размера страницы в 5 значений
    response = requests.get("https://regions-test.2gis.com/1.0/regions?page_size=5")
    data = response.json()

    assert response.status_code == 200, f"Статус код отличается от 200: {response.status_code}"
    assert len(data['items']) == 5, "Размер страницы не равен 5"


test_set_page_size_5()


def test_set_page_size_10():  # Установка размера страницы в 5 значений
    response = requests.get("https://regions-test.2gis.com/1.0/regions?page_size=10")
    data = response.json()

    assert response.status_code == 200, f"Статус код отличается от 200: {response.status_code}"
    assert len(data['items']) == 10, "Размер страницы не равен 10"


test_set_page_size_10()


def test_set_page_size_15():  # Установка размера страницы в 15 значений
    response = requests.get("https://regions-test.2gis.com/1.0/regions?page_size=15")
    assert response.status_code == 200, f"Статус код отличается от 200: {response.status_code}"
    data = response.json()

    assert len(data['items']) == 15, "Размер страницы не равен 15"


test_set_page_size_15()


def test_page_size_by_default():  # Проверка значения размера страницы по умолчанию
    response = requests.get("https://regions-test.2gis.com/1.0/regions")
    assert response.status_code == 200, f"Статус код отличается от 200: {response.status_code}"
    data = response.json()

    assert len(data['items']) == 15, "Размер страницы по умолчанию не равен 15"


test_page_size_by_default()


def test_page_less_than_1():  # Проверка сообщения об ошибке при порядковом номере страницы < 1
    response = requests.get("https://regions-test.2gis.com/1.0/regions?page=0")
    assert response.status_code == 200, f"Статус код отличается от 200: {response.status_code}"
    data = response.json()

    assert data["error"]["message"] == "Минимальное значение для порядкового номера страницы = 1"


test_page_less_than_1()


def test_combination_region_parameters():  # Проверка комбинации параметров country_code, page, page_size
    response = requests.get("https://regions-test.2gis.com/1.0/regions?page=1&page_size=5&country_code=ru")
    data = response.json()

    assert response.status_code == 200, f"Статус код отличается от 200: {response.status_code}"
    assert len(data['items']) == 5, "Размер страницы не равен 5"
    for item in data['items']:
        assert item['country']['code'] == 'ru', 'Россия отсутствует в респонсе'


test_combination_region_parameters()
