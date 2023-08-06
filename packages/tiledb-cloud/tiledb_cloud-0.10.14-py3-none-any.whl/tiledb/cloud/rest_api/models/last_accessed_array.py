# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class LastAccessedArray(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        "array_id": "str",
        "array_name": "str",
        "namespace": "str",
        "accessed_time": "float",
        "access_type": "ActivityEventType",
    }

    attribute_map = {
        "array_id": "array_id",
        "array_name": "array_name",
        "namespace": "namespace",
        "accessed_time": "accessed_time",
        "access_type": "access_type",
    }

    def __init__(
        self,
        array_id=None,
        array_name=None,
        namespace=None,
        accessed_time=None,
        access_type=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """LastAccessedArray - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._array_id = None
        self._array_name = None
        self._namespace = None
        self._accessed_time = None
        self._access_type = None
        self.discriminator = None

        if array_id is not None:
            self.array_id = array_id
        if array_name is not None:
            self.array_name = array_name
        if namespace is not None:
            self.namespace = namespace
        if accessed_time is not None:
            self.accessed_time = accessed_time
        if access_type is not None:
            self.access_type = access_type

    @property
    def array_id(self):
        """Gets the array_id of this LastAccessedArray.  # noqa: E501

        unique ID of array  # noqa: E501

        :return: The array_id of this LastAccessedArray.  # noqa: E501
        :rtype: str
        """
        return self._array_id

    @array_id.setter
    def array_id(self, array_id):
        """Sets the array_id of this LastAccessedArray.

        unique ID of array  # noqa: E501

        :param array_id: The array_id of this LastAccessedArray.  # noqa: E501
        :type: str
        """

        self._array_id = array_id

    @property
    def array_name(self):
        """Gets the array_name of this LastAccessedArray.  # noqa: E501

        name of the array  # noqa: E501

        :return: The array_name of this LastAccessedArray.  # noqa: E501
        :rtype: str
        """
        return self._array_name

    @array_name.setter
    def array_name(self, array_name):
        """Sets the array_name of this LastAccessedArray.

        name of the array  # noqa: E501

        :param array_name: The array_name of this LastAccessedArray.  # noqa: E501
        :type: str
        """

        self._array_name = array_name

    @property
    def namespace(self):
        """Gets the namespace of this LastAccessedArray.  # noqa: E501

        namespace of a user or organization  # noqa: E501

        :return: The namespace of this LastAccessedArray.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this LastAccessedArray.

        namespace of a user or organization  # noqa: E501

        :param namespace: The namespace of this LastAccessedArray.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def accessed_time(self):
        """Gets the accessed_time of this LastAccessedArray.  # noqa: E501

        timestamp (epoch milliseconds) array is last accessed  # noqa: E501

        :return: The accessed_time of this LastAccessedArray.  # noqa: E501
        :rtype: float
        """
        return self._accessed_time

    @accessed_time.setter
    def accessed_time(self, accessed_time):
        """Sets the accessed_time of this LastAccessedArray.

        timestamp (epoch milliseconds) array is last accessed  # noqa: E501

        :param accessed_time: The accessed_time of this LastAccessedArray.  # noqa: E501
        :type: float
        """

        self._accessed_time = accessed_time

    @property
    def access_type(self):
        """Gets the access_type of this LastAccessedArray.  # noqa: E501


        :return: The access_type of this LastAccessedArray.  # noqa: E501
        :rtype: ActivityEventType
        """
        return self._access_type

    @access_type.setter
    def access_type(self, access_type):
        """Sets the access_type of this LastAccessedArray.


        :param access_type: The access_type of this LastAccessedArray.  # noqa: E501
        :type: ActivityEventType
        """

        self._access_type = access_type

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, LastAccessedArray):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LastAccessedArray):
            return True

        return self.to_dict() != other.to_dict()
