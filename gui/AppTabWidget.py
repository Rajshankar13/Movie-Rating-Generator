import subprocess
import shlex
from functools import partial
import os
import re
import pickle

from PySide2.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QTabWidget, QVBoxLayout, QWidget)


class AppTabWidget(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        # self.tabs.resize(300, 200)

        # Create tabs in the main application window
        self.scrapeTab = QWidget()
        self.ratingTab = QWidget()

        # Add the tabs to the widget
        self.tabs.addTab(self.scrapeTab, 'Scrape Data')
        self.tabs.addTab(self.ratingTab, 'Generate Rating')

        # Functions to layout the tabs
        self._layoutscrapeTab()
        self._layoutratingTab()

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    # Layout functions
    def _layoutscrapeTab(self) -> None:
        layout = QGridLayout(self)

        nameLabel = QLabel('Movie Name')
        nameLineEdit = QLineEdit()
        nameLineEdit.setPlaceholderText('Enter name of the movie')

        # Adding rows to the form layout
        layout.addWidget(nameLabel, 0, 0)
        layout.addWidget(nameLineEdit, 0, 1)

        nameLabel2 = QLabel('Movie Link')
        nameLineEdit2 = QLineEdit()
        nameLineEdit2.setPlaceholderText('Enter the link of the movie reviews')

        # Adding rows to the form layout
        layout.addWidget(nameLabel2, 1, 0)
        layout.addWidget(nameLineEdit2, 1, 1)

        # Create a button to that will take the name and pass it on to
        # another program to create dataset
        scrapeButton = QPushButton('Scrape Reviews')
        # Set a target method for `scrapeButton` when clicked
        scrapeButton.clicked.connect(
            partial(self._transferToScraping, scrapeButton, nameLineEdit, nameLineEdit2)
        )
        # Add `scrapeButton` to the layout
        layout.addWidget(scrapeButton, 2, 0, 2, 2)

        # Reset button to clear the name field
        resetButton = QPushButton('Reset')
        # Set a target to clear the field when clicked
        resetButton.clicked.connect(
            partial(self._clearField, resetButton, nameLineEdit, nameLineEdit2)
        )
        # Add `resetButton` to the layout
        layout.addWidget(resetButton, 4, 0, 2, 2)

        # Set this as the layout of the 'Training' tab
        self.scrapeTab.setLayout(layout)


    def _layoutratingTab(self) -> None:
        layout = QGridLayout(self)

        nameLabel = QLabel('Movie Name')
        nameLineEdit = QLineEdit()
        nameLineEdit.setPlaceholderText('Enter name of the movie')
        layout.addWidget(nameLabel, 0, 0)
        layout.addWidget(nameLineEdit, 0, 1)

        ratingLabel = QLabel('Rating')
        actualRating = QLabel()
        layout.addWidget(ratingLabel, 1, 0)
        layout.addWidget(actualRating, 1, 1)

        positive_review = QLabel('Most Positive Review')
        most_positive_review = QLabel()
        layout.addWidget(positive_review, 2, 0)
        layout.addWidget(most_positive_review, 2, 1)

        negative_review = QLabel('Most Negative Review')
        most_negative_review = QLabel()
        layout.addWidget(negative_review, 3, 0)
        layout.addWidget(most_negative_review, 3, 1)

        # Button to open the camera and transfer control to another
        # program that will recognise the face
        ratingButton = QPushButton('Generate Rating')
        # Set a target method for `ratingButton` when clicked
        ratingButton.clicked.connect(
            partial(self._transferToGenerateRating, ratingButton, nameLineEdit, actualRating,
                        most_positive_review, most_negative_review)
        )
        # Add `ratingButton` to the layout
        layout.addWidget(ratingButton, 5, 0, 2, 2)

        # Set this as the layout of the 'Recognition' tab
        self.ratingTab.setLayout(layout)


    # Button target functions
    def _transferToScraping(self,
                                 sender: QPushButton,
                                 name: QLineEdit,
                                 link: QLineEdit) -> None:
        spider_name = 'metacritic_reviews'
        if (name.text() and link.text()):
            movie = str(name.text())            #This is the entered movie name
            movie_name = re.sub(' ', '-', movie.lower())            #Converting it to a valid filename for storing the data
            movie_link = str(link.text())          #This is the movie link
            command = 'scrapy crawl metacritic_reviews -a link=' + movie_link + ' -o ' + movie_name + '.json'           #Generating the command to be run on the cmd for scraping
            #The shlex class makes it easy to write lexical analyzers for simple syntaxes resembling that of the Unix shell.
            args = shlex.split(command)
            os.chdir("movie_reviews/")          #Since the spider is in movie_reviews directory
            # print(os.getcwd())
            subprocess.call(args)               #Executing the crawl command for Spider
            os.chdir("..")
        else:
            # Do something to display error
            print('Field/s is/are empty')
            pass


    def _transferToGenerateRating(self, sender: QPushButton,
                                    name: QLineEdit,
                                    rating: QLabel,
                                    positive: QLabel,
                                    negative: QLabel
                                ) -> None:
        if(name.text()):
            movie_name = re.sub(' ', '-', name.text().lower())            #Converting it to a valid filename for storing the data
            subprocess.call(
                    ['python', 'review_generator.py',
                        '{0}'.format(movie_name)
                    ]
                )

            details_data = []
            with open('details.pickle', 'rb') as fr:
                try:
                    while True:
                        details_data.append(pickle.load(fr))
                except EOFError:
                    pass

            for ele in details_data:
                rating.setText(str(round(ele['rating'], 1)))
                positive.setText(ele['most_positive'])
                positive.setWordWrap(1)
                negative.setText(ele['most_negative'])
                negative.setWordWrap(1)

            os.remove('details.pickle')
        else:
            print('Please enter movie name')
            pass


    def _clearField(self, sender: QPushButton, name: QLineEdit, link: QLineEdit) -> None:
        if (name.text() and link.text()):
            name.setText('')
            link.setText('')
            name.clear()
            link.clear()
