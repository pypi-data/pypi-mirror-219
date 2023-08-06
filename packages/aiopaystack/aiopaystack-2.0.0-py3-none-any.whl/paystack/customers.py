from typing import Literal
from datetime import datetime

from .base import Base, Response


class Customers(Base):
    """
    The Customers API allows you create and manage customers on your integration.
    """

    def __init__(self):
        super().__init__()
        url = "/customer/{}"
        self.url = url.format

    async def create(self, *, email: str, last_name: str, first_name: str, **kwargs) -> Response:
        """
        Create a customer on your integration
        :param email: Customer's email address
        :param last_name: Customer's last name
        :param first_name: Customer's first name
        :param kwargs: Optional params as kwargs
        :return: Response Dict
        """
        data = {'email': email, 'last_name': last_name, 'first_name': first_name, **kwargs}
        return await self.post(url=self.url(""), json=data)

    async def list(self, perPage: int = 50, page: int = 1, from_: datetime | None | str = None,
                   to: datetime | None | str = None) -> Response:
        """
        List customers available on your integration
        :param perPage: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
        :param page: Specify exactly what page you want to retrieve. If not specify we use a default value of 1.
        :param from_: A timestamp from which to start listing customers e.g.
        :param to: A timestamp at which to stop listing product e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
        :return: Response Dict
        """
        params = {key: value for key, value in (('perPage', perPage), ('page', page), ('from', from_),
                                                ('to', to)) if value}
        return await self.get(url=self.url(""), params=params)

    async def fetch(self, *, email_or_code: str) -> Response:
        """
        Get details of a customer on your integration.
        :param email_or_code: An email or customer code for the customer you want to fetch
        :return: Response Dict
        """
        return await self.get(url=self.url(f"{email_or_code}"))

    async def update(self, *, code, **kwargs) -> Response:
        """
        Update a customer's details on your integration
        :param code: Customer's code
        :param kwargs: Data to be updated as keyword args
        :return: Response Dict
        """
        data = kwargs
        return await self.put(url=self.url(f"{code}"), json=data)

    async def validate(self, *, code: str, last_name: str, first_name: str,
                       bvn: str, bank_code: str, account_number: str, type: str = "bank_account", country: str = "NG",
                       **kwargs) -> Response:
        """
        Validate a customer's identity
        :param code: customer_identity code
        :param last_name: Customer's last name
        :param first_name: Customer's first name
        :param type: redefined types of identification. Only bank_account is supported at the moment
        :param value: Customer's identification number
        :param country: 2 letter country code of identification issuer
        :param bvn: Customer's Bank Verification Number
        :param bank_code: You can get the list of Bank Codes by calling the List Banks endpoint. (
        required if type is bank_account)
        :param account_number: Customer's bank account number. (required if type is bank_account)
        :param kwargs: Optional params as keyword args
        :return: Response Dict
        """
        data = {'last_name': last_name, 'first_name': first_name, 'type': type,
                'country': country, 'bvn': bvn, 'bank_code': bank_code, "account_number": account_number, **kwargs}
        return await self.post(url=self.url(f"{code}/identification"), json=data)

    async def set_risk_action(self, *, customer: str, email: str,
                              risk_action: Literal['default', 'deny', 'allow'] = 'default') -> Response:
        """
        Whitelist or blacklist a customer on your integration
        :param email: Customer email
        :param customer: Customer's code
        :param risk_action: One of the possible risk actions [ default, allow, deny ]. allow to whitelist.
        deny to blacklist. Customers start with a default risk action.
        :return: Response Dict
        """
        data = {'customer': customer, 'risk_action': risk_action, 'email': email}
        return await self.post(url=self.url(""), json=data)

    async def deactivate_authorization(self, authorization_code: str) -> Response:
        """
        Deactivate an authorization when the card needs to be forgotten
        :param authorization_code: Authorization code to be deactivated
        :return: Response
        """
        data = {'authorization_code': authorization_code}
        return await self.post(url=self.url("deactivate_authorization"), json=data)
