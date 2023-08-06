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


class ReadState(object):
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
        "initialized": "bool",
        "overflowed": "bool",
        "unsplittable": "bool",
        "subarray_partitioner": "SubarrayPartitioner",
    }

    attribute_map = {
        "initialized": "initialized",
        "overflowed": "overflowed",
        "unsplittable": "unsplittable",
        "subarray_partitioner": "subarrayPartitioner",
    }

    def __init__(
        self,
        initialized=None,
        overflowed=None,
        unsplittable=None,
        subarray_partitioner=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """ReadState - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._initialized = None
        self._overflowed = None
        self._unsplittable = None
        self._subarray_partitioner = None
        self.discriminator = None

        if initialized is not None:
            self.initialized = initialized
        if overflowed is not None:
            self.overflowed = overflowed
        if unsplittable is not None:
            self.unsplittable = unsplittable
        if subarray_partitioner is not None:
            self.subarray_partitioner = subarray_partitioner

    @property
    def initialized(self):
        """Gets the initialized of this ReadState.  # noqa: E501

        True if the reader has been initialized.  # noqa: E501

        :return: The initialized of this ReadState.  # noqa: E501
        :rtype: bool
        """
        return self._initialized

    @initialized.setter
    def initialized(self, initialized):
        """Sets the initialized of this ReadState.

        True if the reader has been initialized.  # noqa: E501

        :param initialized: The initialized of this ReadState.  # noqa: E501
        :type: bool
        """

        self._initialized = initialized

    @property
    def overflowed(self):
        """Gets the overflowed of this ReadState.  # noqa: E501

        True if the query produced results that could not fit in some buffer.  # noqa: E501

        :return: The overflowed of this ReadState.  # noqa: E501
        :rtype: bool
        """
        return self._overflowed

    @overflowed.setter
    def overflowed(self, overflowed):
        """Sets the overflowed of this ReadState.

        True if the query produced results that could not fit in some buffer.  # noqa: E501

        :param overflowed: The overflowed of this ReadState.  # noqa: E501
        :type: bool
        """

        self._overflowed = overflowed

    @property
    def unsplittable(self):
        """Gets the unsplittable of this ReadState.  # noqa: E501

        True if the current subarray partition is unsplittable.  # noqa: E501

        :return: The unsplittable of this ReadState.  # noqa: E501
        :rtype: bool
        """
        return self._unsplittable

    @unsplittable.setter
    def unsplittable(self, unsplittable):
        """Sets the unsplittable of this ReadState.

        True if the current subarray partition is unsplittable.  # noqa: E501

        :param unsplittable: The unsplittable of this ReadState.  # noqa: E501
        :type: bool
        """

        self._unsplittable = unsplittable

    @property
    def subarray_partitioner(self):
        """Gets the subarray_partitioner of this ReadState.  # noqa: E501


        :return: The subarray_partitioner of this ReadState.  # noqa: E501
        :rtype: SubarrayPartitioner
        """
        return self._subarray_partitioner

    @subarray_partitioner.setter
    def subarray_partitioner(self, subarray_partitioner):
        """Sets the subarray_partitioner of this ReadState.


        :param subarray_partitioner: The subarray_partitioner of this ReadState.  # noqa: E501
        :type: SubarrayPartitioner
        """

        self._subarray_partitioner = subarray_partitioner

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
        if not isinstance(other, ReadState):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ReadState):
            return True

        return self.to_dict() != other.to_dict()
