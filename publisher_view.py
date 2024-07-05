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


from publisher_model import PublisherModel

# Main Window class for a PyQt5 application
class PublisherWindow(QMainWindow):
    """Main Window.
    This class represents the main window of the application. It sets up the main window and its layout,
    and creates and arranges the widgets for the window, including a QTableView and three QPushButtons.
    """

    def __init__(self, parent=None):
        # This method sets up the main window, creates an instance of the Model and Publisher
        # classes, and calls the setUpUI method.
        super().__init__(parent)
        self.setWindowTitle("Video Game Publisher Information")
        self.resize(900, 400)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.Model = PublisherModel()
        self.setUpUI()

    def setUpUI(self):
        # Create the table view widget
        self.table = QTableView()
        self.table.setModel(self.Model.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()

        # Create buttons
        self.addButton = QPushButton("ADD")
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton("DELETE")
        self.deleteButton.clicked.connect(self.deletePublisher)
        self.switchTableButton = QPushButton("VIEW GAMES")
        self.switchTableButton.clicked.connect(self.window2)

        # Create the search bar
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search...")
        self.search.textChanged.connect(self.updateSearchResults)

        # Create the combobox to select column for searching
        self.columnComboBox = QComboBox(self)
        self.columnComboBox.addItems(['All', 'Name', 'Country'])

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
        # Open the Add Publisher information dialog
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.Model.addPublisher(dialog.data)
            self.table.resizeColumnsToContents()

    def deletePublisher(self):
        row = self.table.currentIndex().row()
        if row < 0:
            return

        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Make sure all the games for this publisher have been deleted first!",
            QMessageBox.Ok | QMessageBox.Cancel
        )

        if messageBox == QMessageBox.Ok:
            self.Model.deletePublisher(row)

    def updateSearchResults(self, search_string):
        selectColumn = self.columnComboBox.currentText()
        self.Model.searchGame(search_string, selectColumn)

    def window2(self):  # This will open up the publisher window when triggered.
        from views import Window
        self.w = Window()
        self.w.show()
        self.hide()


class AddDialog(QDialog):
    # Add Publisher info dialog
    def __init__(self, parent: None):
        super().__init__(parent=parent)
        self.setWindowTitle("Add Publisher")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setupUI()

    def setupUI(self):
        # Create line edits for data fields
        self.nameField = QLineEdit()
        self.nameField.setObjectName("Name")
        self.marketCapField = QLineEdit()
        self.marketCapField.setObjectName("Market Cap")
        self.countryField = QLineEdit()
        self.countryField.setObjectName("Country")
        self.employeesField = QLineEdit()
        self.employeesField.setObjectName("Employees")

        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("Name:", self.nameField)
        layout.addRow("Market Cap:", self.marketCapField)
        layout.addRow("Country:", self.countryField)
        layout.addRow("Employees:", self.employeesField)
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

    def accept(self):
        self.data = []
        for field in (self.nameField, self.marketCapField, self.countryField, self.employeesField):
            # If given data is not valid
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide valid info {field.objectName()}",
                )
                # Reset .data
                self.data = None
                return

            self.data.append(field.text())

        if not self.data:
            return

        super().accept()