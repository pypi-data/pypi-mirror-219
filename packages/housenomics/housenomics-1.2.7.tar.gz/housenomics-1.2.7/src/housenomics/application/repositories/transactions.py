from sqlalchemy import text

from housenomics.transaction import Transaction


class Transactions:
    def __init__(self, session):
        self.session = session

    def append(self, t: Transaction):
        """
        Append a transaction to the repository.
        """

        sql_statement = """
            INSERT INTO 'transaction' (date_of_movement, description, value, origin)
                               VALUES (:date_of_movement, :description, :value, :origin)
        """
        prepared_statement = text(sql_statement).bindparams(
            date_of_movement=str(t.date_of_movement),
            description=t.description,
            value=t.value,
            origin=t.origin,
        )
        self.session.execute(prepared_statement)
