from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
    QComboBox,
)

from model import Model
from publisher_view import PublisherWindow

# Main Window class for a PyQt5 application
class Window(QMainWindow):
    def __init__(self, parent=None):
        # This method sets up the main window, creates an instance of the Model class, and calls the setUpUI method.
        super().__init__(parent)
        self.setWindowTitle("Game Informations")
        self.resize(900, 300)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.gameModel = Model()
        self.setUpUI()


    def setUpUI(self):
        # Create the table view widget
        self.table = QTableView()
        self.table.setModel(self.gameModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)    
        self.table.resizeColumnsToContents()

        # Create buttons
        self.addButton = QPushButton("ADD")
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton("DELETE")
        self.deleteButton.clicked.connect(self.deleteGame)
        self.switchTableButton = QPushButton("VIEW PUBLISHERS")
        self.switchTableButton.clicked.connect(self.window2)
        
        # Create the search bar
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search...")
        self.search.textChanged.connect(self.updateSearchResults)

        # Create the combobox to select column for searching
        self.columnComboBox = QComboBox(self)
        self.columnComboBox.addItems(['All', 'Name', 'Publisher', 'Tag'])
        
        # Lay out the GUI
        layout = QHBoxLayout()
        self.layout.addWidget(self.columnComboBox)
        self.layout.addLayout(layout)
        layout.addWidget(self.search)
        # layout.addStretch()
        self.layout.addWidget(self.table)
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addWidget(self.switchTableButton)


    def openAddDialog(self):
        # Open the Add game information dialog
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.gameModel.addGame(dialog.data)
            self.table.resizeColumnsToContents()


    def deleteGame(self):
        row = self.table.currentIndex().row()
        if row < 0:
            return

        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected game?",
            QMessageBox.Ok | QMessageBox.Cancel
        )

        if messageBox == QMessageBox.Ok:
            self.gameModel.deleteGame(row)


    def updateSearchResults(self, search_string):
        selectColumn = self.columnComboBox.currentText()
        self.gameModel.searchGame(search_string, selectColumn)
            

    def window2(self):  # This will open up the publisher window when triggered.
        self.w = PublisherWindow()
        self.w.show()
        self.hide()


class AddDialog(QDialog):
    # Add Games info dialog
    def __init__(self, parent: None):
        super().__init__(parent=parent)
        self.setWindowTitle("Add Games")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setupUI()


    def setupUI(self):
        # Create line edits for data fields
        self.nameField = QLineEdit()
        self.nameField.setObjectName("Name")
        self.monthField = QLineEdit()
        self.monthField.setObjectName("Month")
        self.dayField = QLineEdit()
        self.dayField.setObjectName("Day")
        self.yearField = QLineEdit()
        self.yearField.setObjectName("Year")
        self.publisherField = QLineEdit()
        self.publisherField.setObjectName("Publisher")
        self.tagField = QLineEdit()
        self.tagField.setObjectName("Tag")

        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("Name:", self.nameField)
        layout.addRow("Month:", self.monthField)
        layout.addRow("Day:", self.dayField)
        layout.addRow("Year:", self.yearField)
        layout.addRow("Publisher:", self.publisherField)
        layout.addRow("Tag:", self.tagField)
        self.layout.addLayout(layout)

        # Add standard buttons to the dialog and connect them
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    # Check if the text entered in each field is empty or not
    def accept(self):
        self.data = []
        for field in (self.nameField, self.monthField, self.dayField, self.yearField, self.publisherField, self.tagField):
            # If given data is not valid
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a information for '{field.objectName()}'\nIf you are not sure what to enter, leave the field with 'N/A'",
                )
                # Reset .data
                self.data = None
                return

            self.data.append(field.text())

        if not self.data:
            return

        super().accept()
