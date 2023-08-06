import typing


class GatewayTransactions(typing.Protocol):
    """
    Gateway to transactions.
    """

    def __iter__(self):
        pass  # pragma: no cover


class RepositoryTransactions(typing.Protocol):
    """
    Repository to transactions.
    """

    def append(self, transaction):
        pass  # pragma: no cover


class ServiceImportTransactions:
    """
    Imports transactions from a source.
    """

    def __init__(
        self,
        transactions_gateway: GatewayTransactions,
        transactions: RepositoryTransactions,
    ):
        self._transactions_gateway = transactions_gateway
        self._transactions = transactions

    def execute(self):
        for transaction in self._transactions_gateway:
            self._transactions.append(transaction)
