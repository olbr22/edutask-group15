import pytest
from unittest.mock import patch, MagicMock
from pymongo import MongoClient
from pymongo.errors import WriteError
import json

from src.util.dao import DAO

class TestCreate:
    """
    A test suite for the create() method of the DAO class.
    """

    #######################################################################
    # COMMENTED SECTION BELOW USES YIELD WITH FIRST SYNTAX, DOES NOT WORK #
    #######################################################################

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

    #######################################################
    # COMMENTED SECTION BELOW USES VIDEO AS JSON TEMPLATE #
    #######################################################

    # @pytest.fixture
    # def sut(self):
    #     """
    #     System Under Test (SUT).

    #     Returns: DAO: An instance of the DAO class with mocked getValidation.
    #     """

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

    #     with patch('src.util.dao.getValidator', autospec=True) as mockedgetValidator:
    #         mockedgetValidator.return_value = test_json

    #         sut = DAO("test")
            
    #         yield sut

    #     client = MongoClient('localhost', 27017)
    #     db = client['edutask']
    #     db['test'].drop()

    
    @pytest.fixture
    def sut(self):
        """
        System Under Test (SUT).

        Returns: DAO: An instance of the DAO class with mocked getValidation.
        """

        # Changed to string as test 2 fails: python wants capitalised True but bson prefers true. Still does not work though!
        test_json = """{
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["firstName", "lastName", "email"],
                "properties": {
                    "firstName": {
                        "bsonType": "string",
                        "description": "the first name of a user must be determined"
                    }, 
                    "lastName": {
                        "bsonType": "string",
                        "description": "the last name of a user must be determined"
                    },
                    "email": {
                        "bsonType": "string",
                        "description": "the email address of a user must be determined",
                        "uniqueItems": true
                    },
                    "tasks": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "objectId"
                        }
                    }
                }
            }
        }"""

        with patch('src.util.dao.getValidator', autospec=True) as mockedgetValidator:
            mockedgetValidator.return_value = json.loads(test_json)

            sut = DAO("test")
            
            yield sut
            # return sut

        client = MongoClient('localhost', 27017)
        db = client['edutask']
        db['test'].drop()
    

    @pytest.mark.dao
    def test_create(self, sut):
        """
        Test case for the create method of the DAO class.
        This is a TEST test case to ensure that it works.

        Parameters: sut (DAO): The System Under Test (SUT) instance.

        Assertion: Asserts that the result from the create() method is true
        """

        # myData = {
        #     "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        # }

        myData = {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": "joe.bloggs@test.com"
        }

        result = sut.create(myData)

        print(result)

        assert result

    @pytest.mark.dao
    def test_create_1(self, sut):
        """
        Test case 1: Required properties, BSON compliance, and flagged with uniqueItems.
        Required Properties: TRUE
        Comply with BSON: TRUE
        Flagged with uniqueItems: TRUE
        Outcome: JSON Object returned with data: dict and _id.
        """
        myData = {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": "joe.bloggs@test.com"
        }

        result = sut.create(myData)

        assert isinstance(result, dict)
        assert "_id" in result

    @pytest.mark.dao
    def test_create_2(self, sut):
        """
        Test case 2: Required properties, BSON compliance, but not flagged with uniqueItems.
        Required Properties: TRUE
        Comply with BSON: TRUE
        Flagged with uniqueItems: FALSE
        Outcome: WriteError.
        """

        myData = {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": "j.bloggs@test.com"
        }

        sut.create(myData)

        newData = {
            "firstName": "Jonathan",
            "lastName": "Blogs",
            "email": "j.bloggs@test.com"
        }

        with pytest.raises(WriteError):
            sut.create(newData)

    @pytest.mark.dao
    def test_create_3(self, sut):
        """
        Test case 3: Required properties, not BSON compliant, and not flagged with uniqueItems.
        Required Properties: TRUE
        Comply with BSON: FALSE
        Flagged with uniqueItems: FALSE
        Outcome: WriteError.
        """

        myData = {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": "j.bloggs@test.com"
        }

        sut.create(myData)

        newData = {
            "firstName": "Jonathan",
            "lastName": "Blogs",
            "email": (1, 2, 3)
        }

        with pytest.raises(WriteError):
            sut.create(newData)

    @pytest.mark.dao
    def test_create_4(self, sut):
        """
        Test case 4: Required properties, not BSON compliant, but flagged with uniqueItems.
        Required Properties: TRUE
        Comply with BSON: FALSE
        Flagged with uniqueItems: TRUE
        Outcome: WriteError.
        """

        myData = {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": (1, 2, 3)
        }

        with pytest.raises(WriteError):
            sut.create(myData)

    @pytest.mark.dao
    def test_create_5(self, sut):
        """
        Test case 5: No required properties, BSON compliant, and flagged with uniqueItems.
        Required Properties: FALSE
        Comply with BSON: TRUE
        Flagged with uniqueItems: TRUE
        Outcome: WriteError.
        """

        data = {
            "firstName": "Joe",
            "email": "joe.bloggs@test.com"
        }

        with pytest.raises(WriteError):
            sut.create(data)

    @pytest.mark.dao
    def test_create_6(self, sut):
        """
        Test case 6: No required properties, BSON compliant, but not flagged with uniqueItems.
        Required Properties: FALSE
        Comply with BSON: TRUE
        Flagged with uniqueItems: FALSE
        Outcome: WriteError.
        """

        data = {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": "joe.bloggs@test.com"
        }

        sut.create(data)

        newData = {
            "firstName": "Jonathan",
            "email": "joe.bloggs@test.com"
        }

        with pytest.raises(WriteError):
            sut.create(newData)

    @pytest.mark.dao
    def test_create_7(self, sut):
        """
        Test case 7: No required properties, not BSON compliant, but flagged with uniqueItems.
        Required Properties: FALSE
        Comply with BSON: FALSE
        Flagged with uniqueItems: TRUE
        Outcome: WriteError.
        """

        myData = {
            "firstName": "Joe",
            "email": (1, 2, 3)
        }

        with pytest.raises(WriteError):
            sut.create(myData)

    @pytest.mark.dao
    def test_create_8(self, sut):
        """
        Test case 8: No required properties, not BSON compliant, and not flagged with uniqueItems.
        Required Properties: FALSE
        Comply with BSON: FALSE
        Flagged with uniqueItems: FALSE
        Outcome: WriteError.
        """

        myData = {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": "j.bloggs@test.com"
        }

        sut.create(myData)

        newData = {
            "lastName": (1,2,3),
            "email": "j.bloggs@test.com"
        }

        with pytest.raises(WriteError):
            sut.create(newData)

    ########################################################
    # COMMENTED SECTION BELOW EXPERIMENTS WITH PARAMETRISE #
    ########################################################
    
    # @pytest.mark.dao
    # @pytest.mark.parametrize('data, expected', [
    #     ({
    #         "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    #     }, {
    #         "_id": "<generated_object_id>",
    #         "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    #     }),
    #     ({
    #         "ul": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    #     }, WriteError),
        
    #     ])
    # def test_create(self, sut, data, expected):
    #     """
    #     Test case for the create method of the DAO class.

    #     Parameters: sut (DAO): The System Under Test (SUT) instance.

    #     Assertion: Asserts that the result from the create() method is true
    #     """

    #     result = sut.create(data = data)

    #     print(result)

    #     assert result == expected



