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


class Reconciliation(object):
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
        'id': 'ReconciliationId',
        'href': 'str',
        'name': 'str',
        'description': 'str',
        'is_portfolio_group': 'bool',
        'left': 'ResourceId',
        'right': 'ResourceId',
        'transactions': 'ReconciliationTransactions',
        'positions': 'ReconciliationConfiguration',
        'valuations': 'ReconciliationConfiguration',
        'properties': 'dict(str, ModelProperty)',
        'version': 'Version',
        'links': 'list[Link]'
    }

    attribute_map = {
        'id': 'id',
        'href': 'href',
        'name': 'name',
        'description': 'description',
        'is_portfolio_group': 'isPortfolioGroup',
        'left': 'left',
        'right': 'right',
        'transactions': 'transactions',
        'positions': 'positions',
        'valuations': 'valuations',
        'properties': 'properties',
        'version': 'version',
        'links': 'links'
    }

    required_map = {
        'id': 'optional',
        'href': 'optional',
        'name': 'optional',
        'description': 'optional',
        'is_portfolio_group': 'optional',
        'left': 'optional',
        'right': 'optional',
        'transactions': 'optional',
        'positions': 'optional',
        'valuations': 'optional',
        'properties': 'optional',
        'version': 'optional',
        'links': 'optional'
    }

    def __init__(self, id=None, href=None, name=None, description=None, is_portfolio_group=None, left=None, right=None, transactions=None, positions=None, valuations=None, properties=None, version=None, links=None, local_vars_configuration=None):  # noqa: E501
        """Reconciliation - a model defined in OpenAPI"
        
        :param id: 
        :type id: lusid.ReconciliationId
        :param href:  The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.
        :type href: str
        :param name:  The name of the scheduled reconciliation
        :type name: str
        :param description:  A description of the scheduled reconciliation
        :type description: str
        :param is_portfolio_group:  Specifies whether reconciliation is between portfolios or portfolio groups
        :type is_portfolio_group: bool
        :param left: 
        :type left: lusid.ResourceId
        :param right: 
        :type right: lusid.ResourceId
        :param transactions: 
        :type transactions: lusid.ReconciliationTransactions
        :param positions: 
        :type positions: lusid.ReconciliationConfiguration
        :param valuations: 
        :type valuations: lusid.ReconciliationConfiguration
        :param properties:  Reconciliation properties
        :type properties: dict[str, lusid.ModelProperty]
        :param version: 
        :type version: lusid.Version
        :param links: 
        :type links: list[lusid.Link]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._href = None
        self._name = None
        self._description = None
        self._is_portfolio_group = None
        self._left = None
        self._right = None
        self._transactions = None
        self._positions = None
        self._valuations = None
        self._properties = None
        self._version = None
        self._links = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.href = href
        self.name = name
        self.description = description
        if is_portfolio_group is not None:
            self.is_portfolio_group = is_portfolio_group
        if left is not None:
            self.left = left
        if right is not None:
            self.right = right
        if transactions is not None:
            self.transactions = transactions
        if positions is not None:
            self.positions = positions
        if valuations is not None:
            self.valuations = valuations
        self.properties = properties
        if version is not None:
            self.version = version
        self.links = links

    @property
    def id(self):
        """Gets the id of this Reconciliation.  # noqa: E501


        :return: The id of this Reconciliation.  # noqa: E501
        :rtype: lusid.ReconciliationId
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Reconciliation.


        :param id: The id of this Reconciliation.  # noqa: E501
        :type id: lusid.ReconciliationId
        """

        self._id = id

    @property
    def href(self):
        """Gets the href of this Reconciliation.  # noqa: E501

        The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.  # noqa: E501

        :return: The href of this Reconciliation.  # noqa: E501
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this Reconciliation.

        The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.  # noqa: E501

        :param href: The href of this Reconciliation.  # noqa: E501
        :type href: str
        """

        self._href = href

    @property
    def name(self):
        """Gets the name of this Reconciliation.  # noqa: E501

        The name of the scheduled reconciliation  # noqa: E501

        :return: The name of this Reconciliation.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Reconciliation.

        The name of the scheduled reconciliation  # noqa: E501

        :param name: The name of this Reconciliation.  # noqa: E501
        :type name: str
        """

        self._name = name

    @property
    def description(self):
        """Gets the description of this Reconciliation.  # noqa: E501

        A description of the scheduled reconciliation  # noqa: E501

        :return: The description of this Reconciliation.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Reconciliation.

        A description of the scheduled reconciliation  # noqa: E501

        :param description: The description of this Reconciliation.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def is_portfolio_group(self):
        """Gets the is_portfolio_group of this Reconciliation.  # noqa: E501

        Specifies whether reconciliation is between portfolios or portfolio groups  # noqa: E501

        :return: The is_portfolio_group of this Reconciliation.  # noqa: E501
        :rtype: bool
        """
        return self._is_portfolio_group

    @is_portfolio_group.setter
    def is_portfolio_group(self, is_portfolio_group):
        """Sets the is_portfolio_group of this Reconciliation.

        Specifies whether reconciliation is between portfolios or portfolio groups  # noqa: E501

        :param is_portfolio_group: The is_portfolio_group of this Reconciliation.  # noqa: E501
        :type is_portfolio_group: bool
        """

        self._is_portfolio_group = is_portfolio_group

    @property
    def left(self):
        """Gets the left of this Reconciliation.  # noqa: E501


        :return: The left of this Reconciliation.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._left

    @left.setter
    def left(self, left):
        """Sets the left of this Reconciliation.


        :param left: The left of this Reconciliation.  # noqa: E501
        :type left: lusid.ResourceId
        """

        self._left = left

    @property
    def right(self):
        """Gets the right of this Reconciliation.  # noqa: E501


        :return: The right of this Reconciliation.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._right

    @right.setter
    def right(self, right):
        """Sets the right of this Reconciliation.


        :param right: The right of this Reconciliation.  # noqa: E501
        :type right: lusid.ResourceId
        """

        self._right = right

    @property
    def transactions(self):
        """Gets the transactions of this Reconciliation.  # noqa: E501


        :return: The transactions of this Reconciliation.  # noqa: E501
        :rtype: lusid.ReconciliationTransactions
        """
        return self._transactions

    @transactions.setter
    def transactions(self, transactions):
        """Sets the transactions of this Reconciliation.


        :param transactions: The transactions of this Reconciliation.  # noqa: E501
        :type transactions: lusid.ReconciliationTransactions
        """

        self._transactions = transactions

    @property
    def positions(self):
        """Gets the positions of this Reconciliation.  # noqa: E501


        :return: The positions of this Reconciliation.  # noqa: E501
        :rtype: lusid.ReconciliationConfiguration
        """
        return self._positions

    @positions.setter
    def positions(self, positions):
        """Sets the positions of this Reconciliation.


        :param positions: The positions of this Reconciliation.  # noqa: E501
        :type positions: lusid.ReconciliationConfiguration
        """

        self._positions = positions

    @property
    def valuations(self):
        """Gets the valuations of this Reconciliation.  # noqa: E501


        :return: The valuations of this Reconciliation.  # noqa: E501
        :rtype: lusid.ReconciliationConfiguration
        """
        return self._valuations

    @valuations.setter
    def valuations(self, valuations):
        """Sets the valuations of this Reconciliation.


        :param valuations: The valuations of this Reconciliation.  # noqa: E501
        :type valuations: lusid.ReconciliationConfiguration
        """

        self._valuations = valuations

    @property
    def properties(self):
        """Gets the properties of this Reconciliation.  # noqa: E501

        Reconciliation properties  # noqa: E501

        :return: The properties of this Reconciliation.  # noqa: E501
        :rtype: dict[str, lusid.ModelProperty]
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this Reconciliation.

        Reconciliation properties  # noqa: E501

        :param properties: The properties of this Reconciliation.  # noqa: E501
        :type properties: dict[str, lusid.ModelProperty]
        """

        self._properties = properties

    @property
    def version(self):
        """Gets the version of this Reconciliation.  # noqa: E501


        :return: The version of this Reconciliation.  # noqa: E501
        :rtype: lusid.Version
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Reconciliation.


        :param version: The version of this Reconciliation.  # noqa: E501
        :type version: lusid.Version
        """

        self._version = version

    @property
    def links(self):
        """Gets the links of this Reconciliation.  # noqa: E501


        :return: The links of this Reconciliation.  # noqa: E501
        :rtype: list[lusid.Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this Reconciliation.


        :param links: The links of this Reconciliation.  # noqa: E501
        :type links: list[lusid.Link]
        """

        self._links = links

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
        if not isinstance(other, Reconciliation):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Reconciliation):
            return True

        return self.to_dict() != other.to_dict()
