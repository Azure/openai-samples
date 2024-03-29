# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from insights_generator.models.base_model_ import Model
from insights_generator.models.data_metadata import DataMetadata
from insights_generator import util


class DataSample(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self,
                 review_text: str = None,
                 location: str = None,
                 rating: str = None,
                 profile_id: str = None,
                 metadata: List[DataMetadata] = None):
        """DataSample - a model defined in OpenAPI

        :param review_text: The review_text of this DataSample.
        :param location: The location of this DataSample.
        :param rating: The rating of this DataSample.
        :param profile_id: The profile_id of this DataSample.
        :param metadata: The metadata of this DataSample.
        """
        self.openapi_types = {
            'review_text': str,
            'location': str,
            'rating': str,
            'profile_id': str,
            'metadata': List[DataMetadata]
        }

        self.attribute_map = {
            'review_text': 'reviewText',
            'location': 'location',
            'rating': 'rating',
            'profile_id': 'profileId',
            'metadata': 'metadata'
        }

        self._review_text = review_text
        self._location = location
        self._rating = rating
        self._profile_id = profile_id
        self._metadata = metadata

    @classmethod
    def from_dict(cls, dikt: dict) -> 'DataSample':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The DataSample of this DataSample.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def review_text(self):
        """Gets the review_text of this DataSample.


        :return: The review_text of this DataSample.
        :rtype: str
        """
        return self._review_text

    @review_text.setter
    def review_text(self, review_text):
        """Sets the review_text of this DataSample.


        :param review_text: The review_text of this DataSample.
        :type review_text: str
        """
        if review_text is None:
            raise ValueError(
                "Invalid value for `review_text`, must not be `None`")

        self._review_text = review_text

    @property
    def location(self):
        """Gets the location of this DataSample.


        :return: The location of this DataSample.
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this DataSample.


        :param location: The location of this DataSample.
        :type location: str
        """

        self._location = location

    @property
    def rating(self):
        """Gets the rating of this DataSample.


        :return: The rating of this DataSample.
        :rtype: str
        """
        return self._rating

    @rating.setter
    def rating(self, rating):
        """Sets the rating of this DataSample.


        :param rating: The rating of this DataSample.
        :type rating: str
        """

        self._rating = rating

    @property
    def profile_id(self):
        """Gets the profile_id of this DataSample.


        :return: The profile_id of this DataSample.
        :rtype: str
        """
        return self._profile_id

    @profile_id.setter
    def profile_id(self, profile_id):
        """Sets the profile_id of this DataSample.


        :param profile_id: The profile_id of this DataSample.
        :type profile_id: str
        """

        self._profile_id = profile_id

    @property
    def metadata(self):
        """Gets the metadata of this DataSample.


        :return: The metadata of this DataSample.
        :rtype: List[DataMetadata]
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this DataSample.


        :param metadata: The metadata of this DataSample.
        :type metadata: List[DataMetadata]
        """

        self._metadata = metadata
