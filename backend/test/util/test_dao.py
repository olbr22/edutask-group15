import pytest
from unittest.mock import patch, MagicMock
from pymongo import MongoClient

from src.util.dao import DAO

class TestCreate:
    """
    A test suite for the create() method of the DAO class.
    """

    # @pytest.fixture
    # @patch('src.util.dao.getValidator', autospec=True)
    # def sut(self, mockedgetValidator):
    #     test_json = {
    #         "$jsonSchema": {
    #             "bsonType": "object",
    #             "required": ["url"],
    #             "properties": {
    #                 "url": {
    #                     "bsonType": "string",
    #                     "description": "the url of a YouTube video must be determined"
    #                 }
    #             }
    #         }
    #     }
    #     mockedgetValidator.return_value = test_json

    #     sut = DAO("test")

    #     yield sut
    
    #     client = MongoClient('localhost', 27017)
    #     db = client['edutask']
    #     db['test'].drop()

    @pytest.fixture
    def sut(self):
        """
        System Under Test (SUT).

        Returns: DAO: An instance of the DAO class with mocked getValidation.
        """

        test_json = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["url"],
                "properties": {
                    "url": {
                        "bsonType": "string",
                        "description": "the url of a YouTube video must be determined"
                    }
                }
            }
        }

        with patch('src.util.dao.getValidator', autospec=True) as mockedgetValidator:
            mockedgetValidator.return_value = test_json

            sut = DAO("test")
            
            yield sut

        client = MongoClient('localhost', 27017)
        db = client['edutask']
        db['test'].drop()
    

    @pytest.mark.dao
    def test_create(self, sut):
        """
        Test case for the create method of the DAO class.

        Parameters: sut (DAO): The System Under Test (SUT) instance.

        Assertion: Asserts that the result from the create() method is true
        """

        myData = {
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        }

        result = sut.create(myData)

        print(result)

        assert result





