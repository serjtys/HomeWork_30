from rest_framework.pagination import PageNumberPagination


class MaterialsPagination(PageNumberPagination):
    page_size = 5  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Параметр для изменения размера страницы
    max_page_size = 50  # Максимальный размер страницы