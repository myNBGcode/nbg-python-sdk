from datetime import datetime

from . import base


class AccountInformationPSD2Client(base.BaseClient):
    _production_base_url = "https://services.nbg.gr/apis/account.info/v2"
    _sandbox_base_url = "https://apis.nbg.gr/sandbox/account.info/oauth2/v2"

    _production_scopes = ["openid", "profile", "ibank_profile", "role", "sandbox-account-info-api-v2"]
    _sandbox_scopes = ["openid", "profile", "role", "sandbox-account-info-api-v2"]

    def accounts(self) -> dict:
        """
        [Extensive documentation]
        """
        return self._api_request("POST", "account/list")

    def account_beneficiaries(self, iban: str) -> dict:
        """
        [Extensive documentation]
        """
        data = {"iban": iban}
        return self._api_request("POST", "account/beneficiaries", data)

    def account_details(self, account: str) -> dict:
        """
        [Extensive documentation]
        """
        data = {"account": account}
        return self._api_request("POST", "account/details", data)

    def account_transactions(
        self, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """
        [Extensive documentation]
        """
        data = {"account": account, "dateFrom": date_from, "dateTo": date_to}
        return self._api_request("POST", "account/transactions", data)

    def foreign_currency_accounts(self) -> dict:
        """
        [Extensive documentation]
        """
        return self._api_request("POST", "foreign-currency-account/list")

    def foreign_currency_account_beneficiaries(self, account: str) -> dict:
        """
        [Extensive documentation]
        """
        data = {"account": account}
        return self._api_request("POST", "foreign-currency-account/beneficiaries", data)

    def foreign_currency_account_details(self, account: str) -> dict:
        """
        [Extensive documentation]
        """
        data = {"account": account}
        return self._api_request("POST", "foreign-currency-account/details", data)

    def foreign_currency_account_transactions(
        self, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """
        [Extensive documentation]
        """
        data = {"account": account, "dateFrom": date_from, "dateTo": date_to}
        return self._api_request("POST", "foreign-currency-account/transactions", data)

    def scheduled_payments(
        self, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """
        Get scheduled payments. [Extensive documentation]
        """
        data = {"account": account, "dateFrom": date_from, "dateTo": date_to}
        return self._api_request("POST", "scheduled-payments/list", data)

    def standing_orders(
        self, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """
        Retrieves standing orders list for a specified account. [Extensive documentation]
        """
        data = {"account": account, "dateFrom": date_from, "dateTo": date_to}
        return self._api_request("POST", "standing-orders/list", data)

    def create_sandbox(self, sandbox_id: str) -> dict:
        data = {"sandboxId": sandbox_id}
        return self._api_request("POST", "sandbox", data)

    def export_sandbox(self, sandbox_id: str) -> dict:
        return self._api_request("GET", "sandbox/{sandbox_id}")

    def import_sandbox(self, sandbox_id: str, data: dict) -> dict:
        return self._api_request("PUT", "sandbox/{sandbox_id}", data)

    def delete_sandbox(self, sandbox_id: str) -> dict:
        return self._api_request("DELETE", f"sandbox/{sandbox_id}")
