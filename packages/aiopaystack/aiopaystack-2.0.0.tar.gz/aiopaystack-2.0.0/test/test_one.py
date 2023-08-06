import pytest
from fix import start, BaseTest


@pytest.mark.order(1)
class TestOne(BaseTest):
    # @pytest.mark.order(2)
    def test(self, start):
        # print(self.start)
        assert start['email'] == 'e@r'
        assert start['name'] == 'sam'
        start['age'] = 10

    # @pytest.mark.order(1)
    def test2(self, start):
        # print(start2)
        assert start['age'] == 10
        start['gender'] = 'male'

    # @pytest.mark.order(3)
    def test3(self, start):
        assert start['gender'] == 'male'
