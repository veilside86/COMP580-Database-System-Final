from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel
#, QSqlRelationalTableModel, QSqlRelation

class Model:
    def __init__(self):
        self.model = self._createGameModel()

    # defines a static method in the class in Pyton
    @staticmethod
    def _createGameModel():
        # Create and set up the model using QSqlTableModel
        tableModel = QSqlTableModel()
        tableModel.setTable("games")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("ID", "Name", "Month", "Day", "Year", "Publisher", "Tag")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header) 
        return tableModel


    # When add button clicked add row with given datas
    def addGame(self, data):
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()
        self.model.select()

    # When delete button clicked delete the row
    def deleteGame(self, row):
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()

    # Compare the input text and datas in realtime and display the result by Combobox value
    def searchGame(self, text, column):
        if column == 'All':
            self.model.setFilter(
                "Name LIKE '%{}%' OR Publisher LIKE '%{}%' OR Tag LIKE '%{}%'".format(text, text, text)
                )
        else:
            self.model.setFilter(
                "{} LIKE '%{}%'".format(column, text)
            )
        self.model.select()