import pytest
from unittest.mock import patch, MagicMock
from pymongo import MongoClient

from src.util.dao import DAO

class TestCreate:

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

        with patch('src.util.dao.getValidator', autospec=True) as mocked_getValidator:
            mocked_getValidator.return_value = test_json

            sut = DAO("test")
            
            yield sut

        client = MongoClient('localhost', 27017)
        db = client['edutask']
        db['test'].drop()
    

    @pytest.mark.dao
    def test_create(self, sut):

        myData = {
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        }

        result = sut.create(myData)

        print(result)

        assert result





