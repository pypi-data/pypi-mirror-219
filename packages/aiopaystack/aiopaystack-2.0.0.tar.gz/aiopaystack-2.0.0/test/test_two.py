import pytest
from fix import start, BaseTest


@pytest.mark.order(2)
class TestTwo(BaseTest):
    # @pytest.mark.order(4)
    def test5(self, start):
        # print(start)
        assert start['gender'] == 'male'
