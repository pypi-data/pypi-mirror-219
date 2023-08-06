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


class ComplianceRule(object):
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
        'scope': 'str',
        'code': 'str',
        'display_name': 'str',
        'type': 'str',
        'property_key': 'str',
        'value': 'str',
        'address_key': 'str',
        'lower_bound': 'float',
        'upper_bound': 'float',
        'schedule': 'str',
        'hard_requirement': 'bool',
        'target_portfolio_ids': 'list[ResourceId]',
        'description': 'str',
        'version': 'Version'
    }

    attribute_map = {
        'scope': 'scope',
        'code': 'code',
        'display_name': 'displayName',
        'type': 'type',
        'property_key': 'propertyKey',
        'value': 'value',
        'address_key': 'addressKey',
        'lower_bound': 'lowerBound',
        'upper_bound': 'upperBound',
        'schedule': 'schedule',
        'hard_requirement': 'hardRequirement',
        'target_portfolio_ids': 'targetPortfolioIds',
        'description': 'description',
        'version': 'version'
    }

    required_map = {
        'scope': 'required',
        'code': 'required',
        'display_name': 'required',
        'type': 'required',
        'property_key': 'optional',
        'value': 'optional',
        'address_key': 'optional',
        'lower_bound': 'required',
        'upper_bound': 'required',
        'schedule': 'required',
        'hard_requirement': 'required',
        'target_portfolio_ids': 'required',
        'description': 'optional',
        'version': 'optional'
    }

    def __init__(self, scope=None, code=None, display_name=None, type=None, property_key=None, value=None, address_key=None, lower_bound=None, upper_bound=None, schedule=None, hard_requirement=None, target_portfolio_ids=None, description=None, version=None, local_vars_configuration=None):  # noqa: E501
        """ComplianceRule - a model defined in OpenAPI"
        
        :param scope:  (required)
        :type scope: str
        :param code:  (required)
        :type code: str
        :param display_name:  (required)
        :type display_name: str
        :param type:  (required)
        :type type: str
        :param property_key: 
        :type property_key: str
        :param value: 
        :type value: str
        :param address_key: 
        :type address_key: str
        :param lower_bound:  (required)
        :type lower_bound: float
        :param upper_bound:  (required)
        :type upper_bound: float
        :param schedule:  (required)
        :type schedule: str
        :param hard_requirement:  (required)
        :type hard_requirement: bool
        :param target_portfolio_ids:  (required)
        :type target_portfolio_ids: list[lusid.ResourceId]
        :param description: 
        :type description: str
        :param version: 
        :type version: lusid.Version

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._scope = None
        self._code = None
        self._display_name = None
        self._type = None
        self._property_key = None
        self._value = None
        self._address_key = None
        self._lower_bound = None
        self._upper_bound = None
        self._schedule = None
        self._hard_requirement = None
        self._target_portfolio_ids = None
        self._description = None
        self._version = None
        self.discriminator = None

        self.scope = scope
        self.code = code
        self.display_name = display_name
        self.type = type
        self.property_key = property_key
        self.value = value
        self.address_key = address_key
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.schedule = schedule
        self.hard_requirement = hard_requirement
        self.target_portfolio_ids = target_portfolio_ids
        self.description = description
        if version is not None:
            self.version = version

    @property
    def scope(self):
        """Gets the scope of this ComplianceRule.  # noqa: E501


        :return: The scope of this ComplianceRule.  # noqa: E501
        :rtype: str
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this ComplianceRule.


        :param scope: The scope of this ComplianceRule.  # noqa: E501
        :type scope: str
        """
        if self.local_vars_configuration.client_side_validation and scope is None:  # noqa: E501
            raise ValueError("Invalid value for `scope`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                scope is not None and len(scope) < 1):
            raise ValueError("Invalid value for `scope`, length must be greater than or equal to `1`")  # noqa: E501

        self._scope = scope

    @property
    def code(self):
        """Gets the code of this ComplianceRule.  # noqa: E501


        :return: The code of this ComplianceRule.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this ComplianceRule.


        :param code: The code of this ComplianceRule.  # noqa: E501
        :type code: str
        """
        if self.local_vars_configuration.client_side_validation and code is None:  # noqa: E501
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and len(code) < 1):
            raise ValueError("Invalid value for `code`, length must be greater than or equal to `1`")  # noqa: E501

        self._code = code

    @property
    def display_name(self):
        """Gets the display_name of this ComplianceRule.  # noqa: E501


        :return: The display_name of this ComplianceRule.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this ComplianceRule.


        :param display_name: The display_name of this ComplianceRule.  # noqa: E501
        :type display_name: str
        """
        if self.local_vars_configuration.client_side_validation and display_name is None:  # noqa: E501
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                display_name is not None and len(display_name) < 1):
            raise ValueError("Invalid value for `display_name`, length must be greater than or equal to `1`")  # noqa: E501

        self._display_name = display_name

    @property
    def type(self):
        """Gets the type of this ComplianceRule.  # noqa: E501


        :return: The type of this ComplianceRule.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ComplianceRule.


        :param type: The type of this ComplianceRule.  # noqa: E501
        :type type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                type is not None and len(type) < 1):
            raise ValueError("Invalid value for `type`, length must be greater than or equal to `1`")  # noqa: E501

        self._type = type

    @property
    def property_key(self):
        """Gets the property_key of this ComplianceRule.  # noqa: E501


        :return: The property_key of this ComplianceRule.  # noqa: E501
        :rtype: str
        """
        return self._property_key

    @property_key.setter
    def property_key(self, property_key):
        """Sets the property_key of this ComplianceRule.


        :param property_key: The property_key of this ComplianceRule.  # noqa: E501
        :type property_key: str
        """

        self._property_key = property_key

    @property
    def value(self):
        """Gets the value of this ComplianceRule.  # noqa: E501


        :return: The value of this ComplianceRule.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this ComplianceRule.


        :param value: The value of this ComplianceRule.  # noqa: E501
        :type value: str
        """
        if (self.local_vars_configuration.client_side_validation and
                value is not None and len(value) > 512):
            raise ValueError("Invalid value for `value`, length must be less than or equal to `512`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                value is not None and len(value) < 1):
            raise ValueError("Invalid value for `value`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                value is not None and not re.search(r'^[\s\S]*$', value)):  # noqa: E501
            raise ValueError(r"Invalid value for `value`, must be a follow pattern or equal to `/^[\s\S]*$/`")  # noqa: E501

        self._value = value

    @property
    def address_key(self):
        """Gets the address_key of this ComplianceRule.  # noqa: E501


        :return: The address_key of this ComplianceRule.  # noqa: E501
        :rtype: str
        """
        return self._address_key

    @address_key.setter
    def address_key(self, address_key):
        """Sets the address_key of this ComplianceRule.


        :param address_key: The address_key of this ComplianceRule.  # noqa: E501
        :type address_key: str
        """

        self._address_key = address_key

    @property
    def lower_bound(self):
        """Gets the lower_bound of this ComplianceRule.  # noqa: E501


        :return: The lower_bound of this ComplianceRule.  # noqa: E501
        :rtype: float
        """
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, lower_bound):
        """Sets the lower_bound of this ComplianceRule.


        :param lower_bound: The lower_bound of this ComplianceRule.  # noqa: E501
        :type lower_bound: float
        """
        if self.local_vars_configuration.client_side_validation and lower_bound is None:  # noqa: E501
            raise ValueError("Invalid value for `lower_bound`, must not be `None`")  # noqa: E501

        self._lower_bound = lower_bound

    @property
    def upper_bound(self):
        """Gets the upper_bound of this ComplianceRule.  # noqa: E501


        :return: The upper_bound of this ComplianceRule.  # noqa: E501
        :rtype: float
        """
        return self._upper_bound

    @upper_bound.setter
    def upper_bound(self, upper_bound):
        """Sets the upper_bound of this ComplianceRule.


        :param upper_bound: The upper_bound of this ComplianceRule.  # noqa: E501
        :type upper_bound: float
        """
        if self.local_vars_configuration.client_side_validation and upper_bound is None:  # noqa: E501
            raise ValueError("Invalid value for `upper_bound`, must not be `None`")  # noqa: E501

        self._upper_bound = upper_bound

    @property
    def schedule(self):
        """Gets the schedule of this ComplianceRule.  # noqa: E501


        :return: The schedule of this ComplianceRule.  # noqa: E501
        :rtype: str
        """
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        """Sets the schedule of this ComplianceRule.


        :param schedule: The schedule of this ComplianceRule.  # noqa: E501
        :type schedule: str
        """
        if self.local_vars_configuration.client_side_validation and schedule is None:  # noqa: E501
            raise ValueError("Invalid value for `schedule`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                schedule is not None and len(schedule) < 1):
            raise ValueError("Invalid value for `schedule`, length must be greater than or equal to `1`")  # noqa: E501

        self._schedule = schedule

    @property
    def hard_requirement(self):
        """Gets the hard_requirement of this ComplianceRule.  # noqa: E501


        :return: The hard_requirement of this ComplianceRule.  # noqa: E501
        :rtype: bool
        """
        return self._hard_requirement

    @hard_requirement.setter
    def hard_requirement(self, hard_requirement):
        """Sets the hard_requirement of this ComplianceRule.


        :param hard_requirement: The hard_requirement of this ComplianceRule.  # noqa: E501
        :type hard_requirement: bool
        """
        if self.local_vars_configuration.client_side_validation and hard_requirement is None:  # noqa: E501
            raise ValueError("Invalid value for `hard_requirement`, must not be `None`")  # noqa: E501

        self._hard_requirement = hard_requirement

    @property
    def target_portfolio_ids(self):
        """Gets the target_portfolio_ids of this ComplianceRule.  # noqa: E501


        :return: The target_portfolio_ids of this ComplianceRule.  # noqa: E501
        :rtype: list[lusid.ResourceId]
        """
        return self._target_portfolio_ids

    @target_portfolio_ids.setter
    def target_portfolio_ids(self, target_portfolio_ids):
        """Sets the target_portfolio_ids of this ComplianceRule.


        :param target_portfolio_ids: The target_portfolio_ids of this ComplianceRule.  # noqa: E501
        :type target_portfolio_ids: list[lusid.ResourceId]
        """
        if self.local_vars_configuration.client_side_validation and target_portfolio_ids is None:  # noqa: E501
            raise ValueError("Invalid value for `target_portfolio_ids`, must not be `None`")  # noqa: E501

        self._target_portfolio_ids = target_portfolio_ids

    @property
    def description(self):
        """Gets the description of this ComplianceRule.  # noqa: E501


        :return: The description of this ComplianceRule.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ComplianceRule.


        :param description: The description of this ComplianceRule.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def version(self):
        """Gets the version of this ComplianceRule.  # noqa: E501


        :return: The version of this ComplianceRule.  # noqa: E501
        :rtype: lusid.Version
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ComplianceRule.


        :param version: The version of this ComplianceRule.  # noqa: E501
        :type version: lusid.Version
        """

        self._version = version

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
        if not isinstance(other, ComplianceRule):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ComplianceRule):
            return True

        return self.to_dict() != other.to_dict()
