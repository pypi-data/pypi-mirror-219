import pytest
from anon.client import AnonClient


@pytest.fixture(scope="session")
def client():
    token = "04OhpR7fOXa51vQvB4D7k5-0UU00FHqoePeS5RFOn74tq-12MqTkoEuQSIWjnCZViBab-6rOv6FHsrmCA4vnyGpR8RY"
    client = AnonClient(token=token, restriction=False)
    return client

@pytest.fixture(scope="session")
def owner_id():
    owner_id = "646dfe317efd86d845bc71bb"
    return owner_id

