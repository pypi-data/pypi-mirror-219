import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session
from toolcat.database import Database

from housenomics.application.import_transactions import ServiceImportTransactions
from housenomics.application.repositories.transactions import Transactions
from housenomics.infrastructure.gateway_cgd_file import GatewayCGDFile
from housenomics.ui.cli.report import report
from housenomics.ui.cli.version import CommandVersion
from toolbox import cli
from toolbox.cli import CLIApplication

logging_format: dict = {
    "level": logging.CRITICAL,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}

logging.basicConfig(**logging_format)
logger = logging.getLogger(__name__)

database_path = Path.home() / Path("Library/Application Support/Housenomics")


class HousenomicsCLI(CLIApplication):
    help = "Housenomics helps you manage your personal finances."


housenomics_cli = HousenomicsCLI()
app = housenomics_cli.app
housenomics_cli.register_command(CommandVersion)


def migrate_database():
    Database(database_path, Path("migrations/0001 - Initial.sql"))


def import_file(file_path: Path):
    with Session(Database(database_path).engine) as session:
        gateway_cgd = GatewayCGDFile(file_path)
        transactions = Transactions(session)
        ServiceImportTransactions(gateway_cgd, transactions).execute()
        session.commit()


@app.command(name="import", help="Imports the transactions to feed the application")
def import_(file_path: Path):
    reset()
    migrate_database()
    import_file(file_path)


@app.command(name="report", help="Builds reports according to filters")
def report_(
    seller: Optional[str] = cli.Option(default="", help="Filters report by Seller"),
    since: Optional[datetime] = cli.Option(
        default=None, help="Show report since specified date"
    ),
    on: Optional[datetime] = cli.Option(
        default=None, help="Show report on specified date"
    ),
):
    migrate_database()
    report(database_path, seller, since, on)


def reset():
    db = Database(database_path)
    db.remove()


@app.command(
    name="reset",
    help="Deletes all financial information from the application",
)
def reset_():
    delete_information = cli.confirm(
        "Are you sure you want to delete all financial information ?"
    )
    if not delete_information:
        raise cli.Abort()

    reset()
