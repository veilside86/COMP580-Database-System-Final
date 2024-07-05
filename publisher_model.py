from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel


class PublisherModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        """Create and set up the model."""
        tableModel = QSqlTableModel()
        tableModel.setTable("publishers")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("Name", "Market Cap", "Country", "Employees")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
        return tableModel

    def addPublisher(self, data):
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()
        self.model.select()

    def deletePublisher(self, row):
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()


    def searchGame(self, text, column):
        if column == 'All':
            self.model.setFilter(
                "Name LIKE '%{}%' OR Country LIKE '%{}%'".format(text, text)
                )
        else:
            self.model.setFilter(
                "{} LIKE '%{}%'".format(column, text)
            )
        self.model.select()