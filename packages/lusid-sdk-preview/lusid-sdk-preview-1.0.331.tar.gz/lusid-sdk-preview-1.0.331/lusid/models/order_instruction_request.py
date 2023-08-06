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


class OrderInstructionRequest(object):
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
        'id': 'ResourceId',
        'created_date': 'datetime',
        'portfolio_id': 'ResourceId',
        'instrument_identifiers': 'dict(str, str)',
        'quantity': 'float',
        'weight': 'float',
        'price': 'CurrencyAndAmount',
        'properties': 'dict(str, PerpetualProperty)'
    }

    attribute_map = {
        'id': 'id',
        'created_date': 'createdDate',
        'portfolio_id': 'portfolioId',
        'instrument_identifiers': 'instrumentIdentifiers',
        'quantity': 'quantity',
        'weight': 'weight',
        'price': 'price',
        'properties': 'properties'
    }

    required_map = {
        'id': 'required',
        'created_date': 'required',
        'portfolio_id': 'optional',
        'instrument_identifiers': 'optional',
        'quantity': 'optional',
        'weight': 'optional',
        'price': 'optional',
        'properties': 'optional'
    }

    def __init__(self, id=None, created_date=None, portfolio_id=None, instrument_identifiers=None, quantity=None, weight=None, price=None, properties=None, local_vars_configuration=None):  # noqa: E501
        """OrderInstructionRequest - a model defined in OpenAPI"
        
        :param id:  (required)
        :type id: lusid.ResourceId
        :param created_date:  The active date of this order instruction. (required)
        :type created_date: datetime
        :param portfolio_id: 
        :type portfolio_id: lusid.ResourceId
        :param instrument_identifiers:  The instrument ordered.
        :type instrument_identifiers: dict(str, str)
        :param quantity:  The quantity of given instrument ordered.
        :type quantity: float
        :param weight:  The weight of given instrument ordered.
        :type weight: float
        :param price: 
        :type price: lusid.CurrencyAndAmount
        :param properties:  Client-defined properties associated with this execution.
        :type properties: dict[str, lusid.PerpetualProperty]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._created_date = None
        self._portfolio_id = None
        self._instrument_identifiers = None
        self._quantity = None
        self._weight = None
        self._price = None
        self._properties = None
        self.discriminator = None

        self.id = id
        self.created_date = created_date
        if portfolio_id is not None:
            self.portfolio_id = portfolio_id
        self.instrument_identifiers = instrument_identifiers
        self.quantity = quantity
        self.weight = weight
        if price is not None:
            self.price = price
        self.properties = properties

    @property
    def id(self):
        """Gets the id of this OrderInstructionRequest.  # noqa: E501


        :return: The id of this OrderInstructionRequest.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OrderInstructionRequest.


        :param id: The id of this OrderInstructionRequest.  # noqa: E501
        :type id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def created_date(self):
        """Gets the created_date of this OrderInstructionRequest.  # noqa: E501

        The active date of this order instruction.  # noqa: E501

        :return: The created_date of this OrderInstructionRequest.  # noqa: E501
        :rtype: datetime
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        """Sets the created_date of this OrderInstructionRequest.

        The active date of this order instruction.  # noqa: E501

        :param created_date: The created_date of this OrderInstructionRequest.  # noqa: E501
        :type created_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_date is None:  # noqa: E501
            raise ValueError("Invalid value for `created_date`, must not be `None`")  # noqa: E501

        self._created_date = created_date

    @property
    def portfolio_id(self):
        """Gets the portfolio_id of this OrderInstructionRequest.  # noqa: E501


        :return: The portfolio_id of this OrderInstructionRequest.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, portfolio_id):
        """Sets the portfolio_id of this OrderInstructionRequest.


        :param portfolio_id: The portfolio_id of this OrderInstructionRequest.  # noqa: E501
        :type portfolio_id: lusid.ResourceId
        """

        self._portfolio_id = portfolio_id

    @property
    def instrument_identifiers(self):
        """Gets the instrument_identifiers of this OrderInstructionRequest.  # noqa: E501

        The instrument ordered.  # noqa: E501

        :return: The instrument_identifiers of this OrderInstructionRequest.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._instrument_identifiers

    @instrument_identifiers.setter
    def instrument_identifiers(self, instrument_identifiers):
        """Sets the instrument_identifiers of this OrderInstructionRequest.

        The instrument ordered.  # noqa: E501

        :param instrument_identifiers: The instrument_identifiers of this OrderInstructionRequest.  # noqa: E501
        :type instrument_identifiers: dict(str, str)
        """

        self._instrument_identifiers = instrument_identifiers

    @property
    def quantity(self):
        """Gets the quantity of this OrderInstructionRequest.  # noqa: E501

        The quantity of given instrument ordered.  # noqa: E501

        :return: The quantity of this OrderInstructionRequest.  # noqa: E501
        :rtype: float
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this OrderInstructionRequest.

        The quantity of given instrument ordered.  # noqa: E501

        :param quantity: The quantity of this OrderInstructionRequest.  # noqa: E501
        :type quantity: float
        """

        self._quantity = quantity

    @property
    def weight(self):
        """Gets the weight of this OrderInstructionRequest.  # noqa: E501

        The weight of given instrument ordered.  # noqa: E501

        :return: The weight of this OrderInstructionRequest.  # noqa: E501
        :rtype: float
        """
        return self._weight

    @weight.setter
    def weight(self, weight):
        """Sets the weight of this OrderInstructionRequest.

        The weight of given instrument ordered.  # noqa: E501

        :param weight: The weight of this OrderInstructionRequest.  # noqa: E501
        :type weight: float
        """

        self._weight = weight

    @property
    def price(self):
        """Gets the price of this OrderInstructionRequest.  # noqa: E501


        :return: The price of this OrderInstructionRequest.  # noqa: E501
        :rtype: lusid.CurrencyAndAmount
        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of this OrderInstructionRequest.


        :param price: The price of this OrderInstructionRequest.  # noqa: E501
        :type price: lusid.CurrencyAndAmount
        """

        self._price = price

    @property
    def properties(self):
        """Gets the properties of this OrderInstructionRequest.  # noqa: E501

        Client-defined properties associated with this execution.  # noqa: E501

        :return: The properties of this OrderInstructionRequest.  # noqa: E501
        :rtype: dict[str, lusid.PerpetualProperty]
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this OrderInstructionRequest.

        Client-defined properties associated with this execution.  # noqa: E501

        :param properties: The properties of this OrderInstructionRequest.  # noqa: E501
        :type properties: dict[str, lusid.PerpetualProperty]
        """

        self._properties = properties

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
        if not isinstance(other, OrderInstructionRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrderInstructionRequest):
            return True

        return self.to_dict() != other.to_dict()
