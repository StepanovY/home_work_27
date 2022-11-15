from pytest_factoryboy import register

from tests.factories import CategoryFactory, UserFactory, AdFactory

pytest_plugins = "tests.fixtures"

register(AdFactory)
register(CategoryFactory)
register(UserFactory)


