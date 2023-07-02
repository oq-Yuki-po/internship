from factory import Factory
from factory.faker import Faker

from app.schemas.requests.user import User


class UserFactory(Factory):
    class Meta:

        model = User

    machine_name = "sample machine name"
    name = Faker('name')
    ip_address = Faker('ipv4')


if __name__ == '__main__':
    print(UserFactory().dict())
