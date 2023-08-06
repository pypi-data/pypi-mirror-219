# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 1.0.331
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class QuoteId(object):
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
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'quote_series_id': 'QuoteSeriesId',
        'effective_at': 'str'
    }

    attribute_map = {
        'quote_series_id': 'quoteSeriesId',
        'effective_at': 'effectiveAt'
    }

    required_map = {
        'quote_series_id': 'required',
        'effective_at': 'required'
    }

    def __init__(self, quote_series_id=None, effective_at=None, local_vars_configuration=None):  # noqa: E501
        """QuoteId - a model defined in OpenAPI"
        
        :param quote_series_id:  (required)
        :type quote_series_id: lusid.QuoteSeriesId
        :param effective_at:  The effective datetime or cut label at which the quote is valid from. (required)
        :type effective_at: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._quote_series_id = None
        self._effective_at = None
        self.discriminator = None

        self.quote_series_id = quote_series_id
        self.effective_at = effective_at

    @property
    def quote_series_id(self):
        """Gets the quote_series_id of this QuoteId.  # noqa: E501


        :return: The quote_series_id of this QuoteId.  # noqa: E501
        :rtype: lusid.QuoteSeriesId
        """
        return self._quote_series_id

    @quote_series_id.setter
    def quote_series_id(self, quote_series_id):
        """Sets the quote_series_id of this QuoteId.


        :param quote_series_id: The quote_series_id of this QuoteId.  # noqa: E501
        :type quote_series_id: lusid.QuoteSeriesId
        """
        if self.local_vars_configuration.client_side_validation and quote_series_id is None:  # noqa: E501
            raise ValueError("Invalid value for `quote_series_id`, must not be `None`")  # noqa: E501

        self._quote_series_id = quote_series_id

    @property
    def effective_at(self):
        """Gets the effective_at of this QuoteId.  # noqa: E501

        The effective datetime or cut label at which the quote is valid from.  # noqa: E501

        :return: The effective_at of this QuoteId.  # noqa: E501
        :rtype: str
        """
        return self._effective_at

    @effective_at.setter
    def effective_at(self, effective_at):
        """Sets the effective_at of this QuoteId.

        The effective datetime or cut label at which the quote is valid from.  # noqa: E501

        :param effective_at: The effective_at of this QuoteId.  # noqa: E501
        :type effective_at: str
        """
        if self.local_vars_configuration.client_side_validation and effective_at is None:  # noqa: E501
            raise ValueError("Invalid value for `effective_at`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                effective_at is not None and len(effective_at) < 1):
            raise ValueError("Invalid value for `effective_at`, length must be greater than or equal to `1`")  # noqa: E501

        self._effective_at = effective_at

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, QuoteId):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, QuoteId):
            return True

        return self.to_dict() != other.to_dict()
