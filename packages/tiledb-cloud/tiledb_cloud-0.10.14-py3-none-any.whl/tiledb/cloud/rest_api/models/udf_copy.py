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


class UDFCopy(object):
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
    openapi_types = {"output_uri": "str", "namespace": "str", "name": "str"}

    attribute_map = {
        "output_uri": "output_uri",
        "namespace": "namespace",
        "name": "name",
    }

    def __init__(
        self, output_uri=None, namespace=None, name=None, local_vars_configuration=None
    ):  # noqa: E501
        """UDFCopy - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._output_uri = None
        self._namespace = None
        self._name = None
        self.discriminator = None

        if output_uri is not None:
            self.output_uri = output_uri
        if namespace is not None:
            self.namespace = namespace
        if name is not None:
            self.name = name

    @property
    def output_uri(self):
        """Gets the output_uri of this UDFCopy.  # noqa: E501

        output location of the TileDB File  # noqa: E501

        :return: The output_uri of this UDFCopy.  # noqa: E501
        :rtype: str
        """
        return self._output_uri

    @output_uri.setter
    def output_uri(self, output_uri):
        """Sets the output_uri of this UDFCopy.

        output location of the TileDB File  # noqa: E501

        :param output_uri: The output_uri of this UDFCopy.  # noqa: E501
        :type: str
        """

        self._output_uri = output_uri

    @property
    def namespace(self):
        """Gets the namespace of this UDFCopy.  # noqa: E501

        namespace to register the copy. If empty use the namespace of the request user  # noqa: E501

        :return: The namespace of this UDFCopy.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this UDFCopy.

        namespace to register the copy. If empty use the namespace of the request user  # noqa: E501

        :param namespace: The namespace of this UDFCopy.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def name(self):
        """Gets the name of this UDFCopy.  # noqa: E501

        name to set for the copy. If empty use the name as the original udf, if it not already used in the namespace  # noqa: E501

        :return: The name of this UDFCopy.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UDFCopy.

        name to set for the copy. If empty use the name as the original udf, if it not already used in the namespace  # noqa: E501

        :param name: The name of this UDFCopy.  # noqa: E501
        :type: str
        """

        self._name = name

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
        if not isinstance(other, UDFCopy):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UDFCopy):
            return True

        return self.to_dict() != other.to_dict()
