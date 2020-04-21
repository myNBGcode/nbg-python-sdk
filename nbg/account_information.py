from datetime import datetime

from .base import client, decorators


class AccountInformationPSD2Client(client.BaseClient):
    _production_base_url = "https://services.nbg.gr/apis/account.info/v2.1"
    _sandbox_base_url = "https://apis.nbg.gr/sandbox/account.info/oauth2/v2.1"

    _production_scopes = [
        "openid",
        "profile",
        "ibank_profile",
        "role",
        "account-info-api-v2-1",
    ]
    _sandbox_scopes = ["openid", "profile", "role", "sandbox-account-info-api-v2-1"]

    def accounts(self, user_id: str) -> dict:
        data = {"userId": user_id}
        return self._api_request("POST", "account/list", data)

    def account_beneficiaries(self, user_id: str, iban: str) -> dict:
        data = {"userId": user_id, "iban": iban}
        return self._api_request("POST", "account/beneficiaries", data)

    def account_details(self, user_id: str, account: str) -> dict:
        data = {"userId": user_id, "account": account}
        return self._api_request("POST", "account/details", data)

    def account_transactions(
        self, user_id: str, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        data = {
            "userId": user_id,
            "account": account,
            "dateFrom": date_from,
            "dateTo": date_to,
        }
        return self._api_request("POST", "account/transactions", data)

    def cards(self, user_id: str) -> dict:
        data = {"userId": user_id}
        return self._api_request("POST", "card/list", data)

    def card_details(self, user_id: str, card_number: str) -> dict:
        data = {"userId": user_id, "cardNumber": card_number}
        return self._api_request("POST", "card/details", data)

    def card_transactions(
        self, user_id: str, card_number: str, date_from: datetime, date_to: datetime
    ) -> dict:
        data = {
            "userId": user_id,
            "cardNumber": card_number,
            "dateFrom": date_from,
            "dateTo": date_to,
        }
        return self._api_request("POST", "card/transactions", data)

    def foreign_currency_accounts(self, user_id: str) -> dict:
        data = {"userId": user_id}
        return self._api_request("POST", "foreign-currency-account/list", data)

    def foreign_currency_account_beneficiaries(
        self, user_id: str, account: str
    ) -> dict:
        data = {"userId": user_id, "account": account}
        return self._api_request("POST", "foreign-currency-account/beneficiaries", data)

    def foreign_currency_account_details(self, user_id: str, account: str) -> dict:
        data = {"userId": user_id, "account": account}
        return self._api_request("POST", "foreign-currency-account/details", data)

    def foreign_currency_account_transactions(
        self, user_id: str, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        data = {
            "userId": user_id,
            "account": account,
            "dateFrom": date_from,
            "dateTo": date_to,
        }
        return self._api_request("POST", "foreign-currency-account/transactions", data)

    def scheduled_payments(
        self, user_id: str, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        data = {
            "userId": user_id,
            "account": account,
            "dateFrom": date_from,
            "dateTo": date_to,
        }
        return self._api_request("POST", "scheduled-payments/list", data)

    def standing_orders(
        self, user_id: str, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        data = {
            "userId": user_id,
            "account": account,
            "dateFrom": date_from,
            "dateTo": date_to,
        }
        return self._api_request("POST", "standing-orders/list", data)
