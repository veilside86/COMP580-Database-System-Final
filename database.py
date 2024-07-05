from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase


def createConnection(databaseName):
    # Create and open a database connection
    # QSQLITE: SQLite version 3 or above
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    # Open the connection and handle possible errors
    if not connection.open():
        QMessageBox.warning(
            None,
            "Game Info",
            f"Database Error: {connection.lastError().text()}",
        )
        return False
    return True