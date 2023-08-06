from housenomics.application.import_transactions import ServiceImportTransactions


def test_append_zero_transactions_when_no_transactions_to_append():
    source_transactions = []
    transactions = []
    ServiceImportTransactions(source_transactions, transactions).execute()

    assert len(transactions) == 0  # nosec


def test_append_one_transaction_when_one_transaction_available_in_source():
    source_transactions = [{}]
    transactions = []
    ServiceImportTransactions(source_transactions, transactions).execute()

    assert len(transactions) == 1  # nosec
