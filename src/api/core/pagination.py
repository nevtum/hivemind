from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class HighLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 500