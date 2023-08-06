'''
# aws-vpclattice-prealpha

# vpcLattice L2 Construct

* [Project Information](#project-information)
* [Example Impleentation](#example-implementation)
* [API Design](#proposed-api-design-for-vpclattice)
* [FAQ](#faq)
* [Acceptance](#acceptance)

---


## Project Information

**Status** (DRAFT)

**Original Author(s):** @mrpackethead, , @taylaand,  @nbaillie

**Tracking Issue:** #502

**API Bar Raiser:** @TheRealAmazonKendra

**Public Issues ( aws-cdk)**

* (vpclattice): L2 for Amazon VPC Lattice #25452

**Prototype Code**

* https://github.com/raindancers/aws-cdk/tree/mrpackethead/aws-vpclattice-alpha/packages/%40aws-cdk/aws-vpclattice-alpha

**Example implementation**

* https://github.com/raindancers/vpclattice-prealpha-demo

**Blog**

**VpcLattice**

Amazon VPC Lattice is an application networking service that consistently connects, monitors, and secures communications between your services, helping to improve productivity so that your developers can focus on building features that matter to your business. You can define policies for network traffic management, access, and monitoring to connect compute services in a simplified and consistent way across instances, containers, and serverless applications.

The L2 Construct seeks to assist the consumer to create a lattice service easily by abstracting some of the detail.  The major part of this is in creating the underlying auth policy and listener rules together, as their is significant intersection in the properties require for both.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_certificatemanager as _aws_cdk_aws_certificatemanager_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kinesis as _aws_cdk_aws_kinesis_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_vpclattice as _aws_cdk_aws_vpclattice_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.AddServiceProps",
    jsii_struct_bases=[],
    name_mapping={"service": "service", "service_network_id": "serviceNetworkId"},
)
class AddServiceProps:
    def __init__(
        self,
        *,
        service: "IService",
        service_network_id: builtins.str,
    ) -> None:
        '''(experimental) Properties to add a Service to a Service Network.

        :param service: (experimental) The Service to add to the Service Network.
        :param service_network_id: (experimental) The Service Network to add the Service to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b4015f66cc1e6e4d2908b5f92fc0e0fc30e4335031b75bdf77f8d32a45f21c)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument service_network_id", value=service_network_id, expected_type=type_hints["service_network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
            "service_network_id": service_network_id,
        }

    @builtins.property
    def service(self) -> "IService":
        '''(experimental) The Service to add to the Service Network.

        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast("IService", result)

    @builtins.property
    def service_network_id(self) -> builtins.str:
        '''(experimental) The Service Network to add the Service to.

        :stability: experimental
        '''
        result = self._values.get("service_network_id")
        assert result is not None, "Required property 'service_network_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.AddloggingDestinationProps",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class AddloggingDestinationProps:
    def __init__(self, *, destination: "LoggingDestination") -> None:
        '''(experimental) Properties to add a logging Destination.

        :param destination: (experimental) The logging destination.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb99c82f399463ba79b71714c4f2c6a7b042bbd802770d02abaa8442a99c657b)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> "LoggingDestination":
        '''(experimental) The logging destination.

        :stability: experimental
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast("LoggingDestination", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddloggingDestinationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.AssociateVPCProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc", "security_groups": "securityGroups"},
)
class AssociateVPCProps:
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]] = None,
    ) -> None:
        '''(experimental) Properties to associate a VPC with a Service Network.

        :param vpc: (experimental) The VPC to associate with the Service Network.
        :param security_groups: (experimental) The security groups to associate with the Service Network. Default: a security group that allows inbound 443 will be permitted.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faaf88da9f034b12708826cb10f821f26e98818781b4c562804d0c0c19b50c9c)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) The VPC to associate with the Service Network.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]]:
        '''(experimental) The security groups to associate with the Service Network.

        :default: a security group that allows inbound 443 will be permitted.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssociateVPCProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AssociateVpc(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-vpclattice-prealpha.AssociateVpc",
):
    '''(experimental) Associate a VPO with Lattice Service Network.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        service_network_id: builtins.str,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param service_network_id: (experimental) Service Network Identifier.
        :param vpc: (experimental) The VPC to associate with.
        :param security_groups: (experimental) security groups for the lattice endpoint. Default: a security group that will permit inbound 443

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7671d0d9b6ef8d7b1dc2a0f4ccd98692dae7426b69523eafb3a014fa224f95d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AssociateVpcProps(
            service_network_id=service_network_id,
            vpc=vpc,
            security_groups=security_groups,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.AssociateVpcProps",
    jsii_struct_bases=[],
    name_mapping={
        "service_network_id": "serviceNetworkId",
        "vpc": "vpc",
        "security_groups": "securityGroups",
    },
)
class AssociateVpcProps:
    def __init__(
        self,
        *,
        service_network_id: builtins.str,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    ) -> None:
        '''(experimental) Props to Associate a VPC with a Service Network.

        :param service_network_id: (experimental) Service Network Identifier.
        :param vpc: (experimental) The VPC to associate with.
        :param security_groups: (experimental) security groups for the lattice endpoint. Default: a security group that will permit inbound 443

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b24b97a18efc24b7b85203f1578630c8bd0654097deb6dd8cc8e13f19603b7d2)
            check_type(argname="argument service_network_id", value=service_network_id, expected_type=type_hints["service_network_id"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_network_id": service_network_id,
            "vpc": vpc,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups

    @builtins.property
    def service_network_id(self) -> builtins.str:
        '''(experimental) Service Network Identifier.

        :stability: experimental
        '''
        result = self._values.get("service_network_id")
        assert result is not None, "Required property 'service_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) The VPC to associate with.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) security groups for the lattice endpoint.

        :default: a security group that will permit inbound 443

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssociateVpcProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-vpclattice-prealpha.AuthType")
class AuthType(enum.Enum):
    '''(experimental) AuthTypes.

    :stability: experimental
    '''

    NONE = "NONE"
    '''(experimental) No Authorization.

    :stability: experimental
    '''
    AWS_IAM = "AWS_IAM"
    '''(experimental) Use IAM Policy as.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.DefaultListenerAction",
    jsii_struct_bases=[],
    name_mapping={"fixed_response": "fixedResponse", "forward": "forward"},
)
class DefaultListenerAction:
    def __init__(
        self,
        *,
        fixed_response: typing.Optional["FixedResponse"] = None,
        forward: typing.Optional[typing.Union["WeightedTargetGroup", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) A default listener action.

        one of fixed response or forward needs to be provided.

        :param fixed_response: (experimental) Provide a fixed Response. Default: none
        :param forward: (experimental) Forward to a target group. Default: none

        :stability: experimental
        '''
        if isinstance(forward, dict):
            forward = WeightedTargetGroup(**forward)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44af5882c9ea40e745089d97a10308472b69df8c9603ac29739a7b00f9434a63)
            check_type(argname="argument fixed_response", value=fixed_response, expected_type=type_hints["fixed_response"])
            check_type(argname="argument forward", value=forward, expected_type=type_hints["forward"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fixed_response is not None:
            self._values["fixed_response"] = fixed_response
        if forward is not None:
            self._values["forward"] = forward

    @builtins.property
    def fixed_response(self) -> typing.Optional["FixedResponse"]:
        '''(experimental) Provide a fixed Response.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("fixed_response")
        return typing.cast(typing.Optional["FixedResponse"], result)

    @builtins.property
    def forward(self) -> typing.Optional["WeightedTargetGroup"]:
        '''(experimental) Forward to a target group.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("forward")
        return typing.cast(typing.Optional["WeightedTargetGroup"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DefaultListenerAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-vpclattice-prealpha.FixedResponse")
class FixedResponse(enum.Enum):
    '''(experimental) Fixed response codes.

    :stability: experimental
    '''

    NOT_FOUND = "NOT_FOUND"
    '''(experimental) Not Found 404.

    :stability: experimental
    '''
    OK = "OK"
    '''(experimental) OK 200.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.HTTPMatch",
    jsii_struct_bases=[],
    name_mapping={
        "header_matches": "headerMatches",
        "method": "method",
        "path_matches": "pathMatches",
    },
)
class HTTPMatch:
    def __init__(
        self,
        *,
        header_matches: typing.Optional[typing.Sequence[typing.Union["HeaderMatch", typing.Dict[builtins.str, typing.Any]]]] = None,
        method: typing.Optional["HTTPMethods"] = None,
        path_matches: typing.Optional[typing.Union["PathMatch", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) An HTTPMatch for creating rules At least one of headermatch, method or patchmatches must be created.

        :param header_matches: (experimental) Properties to Create A HeaderMatch. Default: no header match
        :param method: (experimental) Method to match against. Default: no header match
        :param path_matches: (experimental) Properties to Create A PathMatch. Default: no path match

        :stability: experimental
        '''
        if isinstance(path_matches, dict):
            path_matches = PathMatch(**path_matches)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5aba9d5436c7bf0a13346c8c563cdde4ffa85f0f4dd100dfcbce7af3416d93f)
            check_type(argname="argument header_matches", value=header_matches, expected_type=type_hints["header_matches"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument path_matches", value=path_matches, expected_type=type_hints["path_matches"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_matches is not None:
            self._values["header_matches"] = header_matches
        if method is not None:
            self._values["method"] = method
        if path_matches is not None:
            self._values["path_matches"] = path_matches

    @builtins.property
    def header_matches(self) -> typing.Optional[typing.List["HeaderMatch"]]:
        '''(experimental) Properties to Create A HeaderMatch.

        :default: no header match

        :stability: experimental
        '''
        result = self._values.get("header_matches")
        return typing.cast(typing.Optional[typing.List["HeaderMatch"]], result)

    @builtins.property
    def method(self) -> typing.Optional["HTTPMethods"]:
        '''(experimental) Method to match against.

        :default: no header match

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional["HTTPMethods"], result)

    @builtins.property
    def path_matches(self) -> typing.Optional["PathMatch"]:
        '''(experimental) Properties to Create A PathMatch.

        :default: no path match

        :stability: experimental
        '''
        result = self._values.get("path_matches")
        return typing.cast(typing.Optional["PathMatch"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HTTPMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-vpclattice-prealpha.HTTPMethods")
class HTTPMethods(enum.Enum):
    '''(experimental) HTTP Methods.

    :stability: experimental
    '''

    GET = "GET"
    '''(experimental) GET Method.

    :stability: experimental
    '''
    POST = "POST"
    '''(experimental) POST Method.

    :stability: experimental
    '''
    PUT = "PUT"
    '''(experimental) PUT Method.

    :stability: experimental
    '''
    DELETE = "DELETE"
    '''(experimental) Delete Method.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.HeaderMatch",
    jsii_struct_bases=[],
    name_mapping={
        "headername": "headername",
        "match_operator": "matchOperator",
        "match_value": "matchValue",
        "case_sensitive": "caseSensitive",
    },
)
class HeaderMatch:
    def __init__(
        self,
        *,
        headername: builtins.str,
        match_operator: "MatchOperator",
        match_value: builtins.str,
        case_sensitive: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Header Matches for creating rules.

        :param headername: (experimental) the name of the header to match.
        :param match_operator: (experimental) Type of match to make.
        :param match_value: (experimental) Value to match against.
        :param case_sensitive: (experimental) Should the match be case sensitive? Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630e305fb29c08a9d5d7c4d0ce4c846132292e1ad11b996b501d021ab122b09e)
            check_type(argname="argument headername", value=headername, expected_type=type_hints["headername"])
            check_type(argname="argument match_operator", value=match_operator, expected_type=type_hints["match_operator"])
            check_type(argname="argument match_value", value=match_value, expected_type=type_hints["match_value"])
            check_type(argname="argument case_sensitive", value=case_sensitive, expected_type=type_hints["case_sensitive"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "headername": headername,
            "match_operator": match_operator,
            "match_value": match_value,
        }
        if case_sensitive is not None:
            self._values["case_sensitive"] = case_sensitive

    @builtins.property
    def headername(self) -> builtins.str:
        '''(experimental) the name of the header to match.

        :stability: experimental
        '''
        result = self._values.get("headername")
        assert result is not None, "Required property 'headername' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_operator(self) -> "MatchOperator":
        '''(experimental) Type of match to make.

        :stability: experimental
        '''
        result = self._values.get("match_operator")
        assert result is not None, "Required property 'match_operator' is missing"
        return typing.cast("MatchOperator", result)

    @builtins.property
    def match_value(self) -> builtins.str:
        '''(experimental) Value to match against.

        :stability: experimental
        '''
        result = self._values.get("match_value")
        assert result is not None, "Required property 'match_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def case_sensitive(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Should the match be case sensitive?

        :default: true

        :stability: experimental
        '''
        result = self._values.get("case_sensitive")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HeaderMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-vpclattice-prealpha.IListener")
class IListener(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Create a vpcLattice Listener.

    Implemented by ``Listener``.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the service.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="listenerId")
    def listener_id(self) -> builtins.str:
        '''(experimental) The Id of the Service Network.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addListenerRule")
    def add_listener_rule(
        self,
        *,
        action: typing.Union[FixedResponse, typing.Sequence[typing.Union["WeightedTargetGroup", typing.Dict[builtins.str, typing.Any]]]],
        http_match: typing.Union[HTTPMatch, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        access_mode: typing.Optional["RuleAccessMode"] = None,
        allowed_principal_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_principals: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IPrincipal]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Add A Listener Rule to the Listener.

        :param action: (experimental) the action for the rule, is either a fixed Reponse, or a being sent to Weighted TargetGroup.
        :param http_match: (experimental) the Matching criteria for the rule. This must contain at least one of header, method or patchMatches
        :param name: (experimental) A name for the the Rule.
        :param access_mode: (experimental) Set an access mode. Default: false
        :param allowed_principal_arn: (experimental) List of principalArns that are allowed to access the resource. Default: none
        :param allowed_principals: (experimental) List of principals that are allowed to access the resource. Default: none
        :param priority: (experimental) the priority of this rule, a lower priority will be processed first. Default: 50

        :stability: experimental
        '''
        ...


class _IListenerProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Create a vpcLattice Listener.

    Implemented by ``Listener``.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-vpclattice-prealpha.IListener"

    @builtins.property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the service.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerArn"))

    @builtins.property
    @jsii.member(jsii_name="listenerId")
    def listener_id(self) -> builtins.str:
        '''(experimental) The Id of the Service Network.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerId"))

    @jsii.member(jsii_name="addListenerRule")
    def add_listener_rule(
        self,
        *,
        action: typing.Union[FixedResponse, typing.Sequence[typing.Union["WeightedTargetGroup", typing.Dict[builtins.str, typing.Any]]]],
        http_match: typing.Union[HTTPMatch, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        access_mode: typing.Optional["RuleAccessMode"] = None,
        allowed_principal_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_principals: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IPrincipal]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Add A Listener Rule to the Listener.

        :param action: (experimental) the action for the rule, is either a fixed Reponse, or a being sent to Weighted TargetGroup.
        :param http_match: (experimental) the Matching criteria for the rule. This must contain at least one of header, method or patchMatches
        :param name: (experimental) A name for the the Rule.
        :param access_mode: (experimental) Set an access mode. Default: false
        :param allowed_principal_arn: (experimental) List of principalArns that are allowed to access the resource. Default: none
        :param allowed_principals: (experimental) List of principals that are allowed to access the resource. Default: none
        :param priority: (experimental) the priority of this rule, a lower priority will be processed first. Default: 50

        :stability: experimental
        '''
        props = RuleProp(
            action=action,
            http_match=http_match,
            name=name,
            access_mode=access_mode,
            allowed_principal_arn=allowed_principal_arn,
            allowed_principals=allowed_principals,
            priority=priority,
        )

        return typing.cast(None, jsii.invoke(self, "addListenerRule", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IListener).__jsii_proxy_class__ = lambda : _IListenerProxy


@jsii.interface(jsii_type="aws-vpclattice-prealpha.IService")
class IService(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Create a vpcLattice service network.

    Implemented by ``Service``.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="imported")
    def imported(self) -> builtins.bool:
        '''(experimental) Imported.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> builtins.str:
        '''(experimental) The Arn of the Service.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> builtins.str:
        '''(experimental) The Id of the Service.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) the discovered OrgId.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="authPolicy")
    def auth_policy(self) -> _aws_cdk_aws_iam_ceddda9d.PolicyDocument:
        '''(experimental) The auth Policy for the service.

        :stability: experimental
        '''
        ...

    @auth_policy.setter
    def auth_policy(self, value: _aws_cdk_aws_iam_ceddda9d.PolicyDocument) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The authType of the service.

        :stability: experimental
        '''
        ...

    @auth_type.setter
    def auth_type(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate]:
        '''(experimental) A certificate that may be used by the service.

        :stability: experimental
        '''
        ...

    @certificate.setter
    def certificate(
        self,
        value: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="customDomain")
    def custom_domain(self) -> typing.Optional[builtins.str]:
        '''(experimental) A custom Domain used by the service.

        :stability: experimental
        '''
        ...

    @custom_domain.setter
    def custom_domain(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the service.

        :stability: experimental
        '''
        ...

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @jsii.member(jsii_name="applyAuthPolicy")
    def apply_auth_policy(self) -> _aws_cdk_aws_iam_ceddda9d.PolicyDocument:
        '''(experimental) apply an authpolicy to the servicenetwork.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="associateWithServiceNetwork")
    def associate_with_service_network(
        self,
        service_network: "IServiceNetwork",
    ) -> None:
        '''(experimental) associate the service with a servicenetwork.

        :param service_network: -

        :stability: experimental
        '''
        ...


class _IServiceProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Create a vpcLattice service network.

    Implemented by ``Service``.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-vpclattice-prealpha.IService"

    @builtins.property
    @jsii.member(jsii_name="imported")
    def imported(self) -> builtins.bool:
        '''(experimental) Imported.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "imported"))

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> builtins.str:
        '''(experimental) The Arn of the Service.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceArn"))

    @builtins.property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> builtins.str:
        '''(experimental) The Id of the Service.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceId"))

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) the discovered OrgId.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgId"))

    @builtins.property
    @jsii.member(jsii_name="authPolicy")
    def auth_policy(self) -> _aws_cdk_aws_iam_ceddda9d.PolicyDocument:
        '''(experimental) The auth Policy for the service.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.PolicyDocument, jsii.get(self, "authPolicy"))

    @auth_policy.setter
    def auth_policy(self, value: _aws_cdk_aws_iam_ceddda9d.PolicyDocument) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3552df34a58f59ebe96fa8e8e9e946506c316b05c8490a91a9da9cbbed02720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The authType of the service.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3d733e9e1b87f3780e70fc8a1fadb074e593edf1e7819442d23b72bbb3aa6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate]:
        '''(experimental) A certificate that may be used by the service.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(
        self,
        value: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf546ba69e00ab089cb3faab5297e3c1d9f7654a6e07e60153aeede16ed2374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="customDomain")
    def custom_domain(self) -> typing.Optional[builtins.str]:
        '''(experimental) A custom Domain used by the service.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDomain"))

    @custom_domain.setter
    def custom_domain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d440d965bd15e56d27443d1bd9693d943d9e84dd228cdd9b5d20178b4d81a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDomain", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the service.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9154e180f7868fa32c6e112ffba8f5229db13a067a022373656550b77bb9fba2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.member(jsii_name="applyAuthPolicy")
    def apply_auth_policy(self) -> _aws_cdk_aws_iam_ceddda9d.PolicyDocument:
        '''(experimental) apply an authpolicy to the servicenetwork.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.PolicyDocument, jsii.invoke(self, "applyAuthPolicy", []))

    @jsii.member(jsii_name="associateWithServiceNetwork")
    def associate_with_service_network(
        self,
        service_network: "IServiceNetwork",
    ) -> None:
        '''(experimental) associate the service with a servicenetwork.

        :param service_network: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__649ee528054b2fde60cb4a4bb489a362d64612813194a7c4edafe1ed296890a2)
            check_type(argname="argument service_network", value=service_network, expected_type=type_hints["service_network"])
        return typing.cast(None, jsii.invoke(self, "associateWithServiceNetwork", [service_network]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IService).__jsii_proxy_class__ = lambda : _IServiceProxy


@jsii.interface(jsii_type="aws-vpclattice-prealpha.IServiceNetwork")
class IServiceNetwork(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Create a vpc lattice service network.

    Implemented by ``ServiceNetwork``.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="imported")
    def imported(self) -> builtins.bool:
        '''(experimental) Is this an imported serviceNetwork.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkArn")
    def service_network_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the service network.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkId")
    def service_network_id(self) -> builtins.str:
        '''(experimental) The Id of the Service Network.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addService")
    def add_service(
        self,
        *,
        service: IService,
        service_network_id: builtins.str,
    ) -> None:
        '''(experimental) Add Lattice Service.

        :param service: (experimental) The Service to add to the Service Network.
        :param service_network_id: (experimental) The Service Network to add the Service to.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="associateVPC")
    def associate_vpc(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]] = None,
    ) -> None:
        '''(experimental) Associate a VPC with the Service Network.

        :param vpc: (experimental) The VPC to associate with the Service Network.
        :param security_groups: (experimental) The security groups to associate with the Service Network. Default: a security group that allows inbound 443 will be permitted.

        :stability: experimental
        '''
        ...


class _IServiceNetworkProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Create a vpc lattice service network.

    Implemented by ``ServiceNetwork``.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-vpclattice-prealpha.IServiceNetwork"

    @builtins.property
    @jsii.member(jsii_name="imported")
    def imported(self) -> builtins.bool:
        '''(experimental) Is this an imported serviceNetwork.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "imported"))

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkArn")
    def service_network_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the service network.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceNetworkArn"))

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkId")
    def service_network_id(self) -> builtins.str:
        '''(experimental) The Id of the Service Network.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceNetworkId"))

    @jsii.member(jsii_name="addService")
    def add_service(
        self,
        *,
        service: IService,
        service_network_id: builtins.str,
    ) -> None:
        '''(experimental) Add Lattice Service.

        :param service: (experimental) The Service to add to the Service Network.
        :param service_network_id: (experimental) The Service Network to add the Service to.

        :stability: experimental
        '''
        props = AddServiceProps(service=service, service_network_id=service_network_id)

        return typing.cast(None, jsii.invoke(self, "addService", [props]))

    @jsii.member(jsii_name="associateVPC")
    def associate_vpc(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]] = None,
    ) -> None:
        '''(experimental) Associate a VPC with the Service Network.

        :param vpc: (experimental) The VPC to associate with the Service Network.
        :param security_groups: (experimental) The security groups to associate with the Service Network. Default: a security group that allows inbound 443 will be permitted.

        :stability: experimental
        '''
        props = AssociateVPCProps(vpc=vpc, security_groups=security_groups)

        return typing.cast(None, jsii.invoke(self, "associateVPC", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IServiceNetwork).__jsii_proxy_class__ = lambda : _IServiceNetworkProxy


@jsii.interface(jsii_type="aws-vpclattice-prealpha.ITarget")
class ITarget(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> typing.List[_aws_cdk_aws_vpclattice_ceddda9d.CfnTargetGroup.TargetProperty]:
        '''(experimental) References to the targets, ids or Arns.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''(experimental) Target Type.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_vpclattice_ceddda9d.CfnTargetGroup.TargetGroupConfigProperty]:
        '''(experimental) Configuration for the TargetGroup, if it is not a lambda.

        :stability: experimental
        '''
        ...


class _ITargetProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-vpclattice-prealpha.ITarget"

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> typing.List[_aws_cdk_aws_vpclattice_ceddda9d.CfnTargetGroup.TargetProperty]:
        '''(experimental) References to the targets, ids or Arns.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_vpclattice_ceddda9d.CfnTargetGroup.TargetProperty], jsii.get(self, "targets"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''(experimental) Target Type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_vpclattice_ceddda9d.CfnTargetGroup.TargetGroupConfigProperty]:
        '''(experimental) Configuration for the TargetGroup, if it is not a lambda.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_vpclattice_ceddda9d.CfnTargetGroup.TargetGroupConfigProperty], jsii.get(self, "config"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITarget).__jsii_proxy_class__ = lambda : _ITargetProxy


@jsii.interface(jsii_type="aws-vpclattice-prealpha.ITargetGroup")
class ITargetGroup(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Create a vpc lattice TargetGroup.

    Implemented by ``TargetGroup``.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> builtins.str:
        '''(experimental) The Arn of the target group.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="targetGroupId")
    def target_group_id(self) -> builtins.str:
        '''(experimental) The id of the target group.

        :stability: experimental
        '''
        ...


class _ITargetGroupProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Create a vpc lattice TargetGroup.

    Implemented by ``TargetGroup``.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-vpclattice-prealpha.ITargetGroup"

    @builtins.property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> builtins.str:
        '''(experimental) The Arn of the target group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupId")
    def target_group_id(self) -> builtins.str:
        '''(experimental) The id of the target group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetGroupId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITargetGroup).__jsii_proxy_class__ = lambda : _ITargetGroupProxy


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.ImportedServiceNetworkProps",
    jsii_struct_bases=[],
    name_mapping={
        "service_network_id": "serviceNetworkId",
        "service_network_name": "serviceNetworkName",
    },
)
class ImportedServiceNetworkProps:
    def __init__(
        self,
        *,
        service_network_id: typing.Optional[builtins.str] = None,
        service_network_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Props for ImportedSearch.

        :param service_network_id: (experimental) Import by Id. Default: - No Search by Id
        :param service_network_name: (experimental) Import by Name. Default: - No search By Name

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7ec4aa4b499c4d5c90362046200cac1b690729c2ad2e0b7758945fb4eb4212)
            check_type(argname="argument service_network_id", value=service_network_id, expected_type=type_hints["service_network_id"])
            check_type(argname="argument service_network_name", value=service_network_name, expected_type=type_hints["service_network_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if service_network_id is not None:
            self._values["service_network_id"] = service_network_id
        if service_network_name is not None:
            self._values["service_network_name"] = service_network_name

    @builtins.property
    def service_network_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Import by Id.

        :default: - No Search by Id

        :stability: experimental
        '''
        result = self._values.get("service_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_network_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Import by Name.

        :default: - No search By Name

        :stability: experimental
        '''
        result = self._values.get("service_network_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImportedServiceNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IListener)
class Listener(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-vpclattice-prealpha.Listener",
):
    '''(experimental) This class should not be called directly.

    Use the .addListener() Method on an instance of LatticeService
    Creates a vpcLattice Listener

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        service: IService,
        default_action: typing.Optional[typing.Union[DefaultListenerAction, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional["Protocol"] = None,
        rules: typing.Optional[typing.Sequence[typing.Union["RuleProp", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Service auth Policy.

        :param scope: -
        :param id: -
        :param service: (experimental) The Id of the service that this listener is associated with.
        :param default_action: (experimental) * A default action that will be taken if no rules match. Default: 404 NOT Found
        :param name: (experimental) The Name of the service. Default: CloudFormation provided name.
        :param port: (experimental) Optional port number for the listener. If not supplied, will default to 80 or 443, depending on the Protocol Default: 80 or 443 depending on the Protocol
        :param protocol: (experimental) protocol that the listener will listen on. Default: HTTPS
        :param rules: (experimental) rules for the listener.

        :default: none.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb71f2f6428ab04fb943120047ec2c8af2d396af0ee76e1dafa108ef1373641)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ListenerProps(
            service=service,
            default_action=default_action,
            name=name,
            port=port,
            protocol=protocol,
            rules=rules,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addListenerRule")
    def add_listener_rule(
        self,
        *,
        action: typing.Union[FixedResponse, typing.Sequence[typing.Union["WeightedTargetGroup", typing.Dict[builtins.str, typing.Any]]]],
        http_match: typing.Union[HTTPMatch, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        access_mode: typing.Optional["RuleAccessMode"] = None,
        allowed_principal_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_principals: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IPrincipal]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) add a rule to the listener.

        :param action: (experimental) the action for the rule, is either a fixed Reponse, or a being sent to Weighted TargetGroup.
        :param http_match: (experimental) the Matching criteria for the rule. This must contain at least one of header, method or patchMatches
        :param name: (experimental) A name for the the Rule.
        :param access_mode: (experimental) Set an access mode. Default: false
        :param allowed_principal_arn: (experimental) List of principalArns that are allowed to access the resource. Default: none
        :param allowed_principals: (experimental) List of principals that are allowed to access the resource. Default: none
        :param priority: (experimental) the priority of this rule, a lower priority will be processed first. Default: 50

        :stability: experimental
        '''
        props = RuleProp(
            action=action,
            http_match=http_match,
            name=name,
            access_mode=access_mode,
            allowed_principal_arn=allowed_principal_arn,
            allowed_principals=allowed_principals,
            priority=priority,
        )

        return typing.cast(None, jsii.invoke(self, "addListenerRule", [props]))

    @builtins.property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''(experimental) THe Arn of the Listener.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerArn"))

    @builtins.property
    @jsii.member(jsii_name="listenerId")
    def listener_id(self) -> builtins.str:
        '''(experimental) The Id of the Listener.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerId"))

    @builtins.property
    @jsii.member(jsii_name="listenerPrioritys")
    def listener_prioritys(self) -> typing.List[jsii.Number]:
        '''(experimental) A list of prioritys, to check for duplicates.

        :stability: experimental
        '''
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "listenerPrioritys"))

    @listener_prioritys.setter
    def listener_prioritys(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1ace053d59e3cbdcee35db1e63d58cc647015852487fa802da3eacbdb559e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listenerPrioritys", value)

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> IService:
        '''(experimental) The service this listener is attached to.

        :stability: experimental
        '''
        return typing.cast(IService, jsii.get(self, "service"))

    @service.setter
    def service(self, value: IService) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68f71fa25236c863d0edf9b99555f53d628bab19f530cf943f220f94fce91ea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value)


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.ListenerProps",
    jsii_struct_bases=[],
    name_mapping={
        "service": "service",
        "default_action": "defaultAction",
        "name": "name",
        "port": "port",
        "protocol": "protocol",
        "rules": "rules",
    },
)
class ListenerProps:
    def __init__(
        self,
        *,
        service: IService,
        default_action: typing.Optional[typing.Union[DefaultListenerAction, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional["Protocol"] = None,
        rules: typing.Optional[typing.Sequence[typing.Union["RuleProp", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Propertys to Create a Lattice Listener.

        :param service: (experimental) The Id of the service that this listener is associated with.
        :param default_action: (experimental) * A default action that will be taken if no rules match. Default: 404 NOT Found
        :param name: (experimental) The Name of the service. Default: CloudFormation provided name.
        :param port: (experimental) Optional port number for the listener. If not supplied, will default to 80 or 443, depending on the Protocol Default: 80 or 443 depending on the Protocol
        :param protocol: (experimental) protocol that the listener will listen on. Default: HTTPS
        :param rules: (experimental) rules for the listener.

        :stability: experimental
        '''
        if isinstance(default_action, dict):
            default_action = DefaultListenerAction(**default_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f43a6d10644426ab80eab11e6e7983c88a302ece410564a74eedba73d29a7ee)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }
        if default_action is not None:
            self._values["default_action"] = default_action
        if name is not None:
            self._values["name"] = name
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def service(self) -> IService:
        '''(experimental) The Id of the service that this listener is associated with.

        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(IService, result)

    @builtins.property
    def default_action(self) -> typing.Optional[DefaultListenerAction]:
        '''(experimental) * A default action that will be taken if no rules match.

        :default: 404 NOT Found

        :stability: experimental
        '''
        result = self._values.get("default_action")
        return typing.cast(typing.Optional[DefaultListenerAction], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Name of the service.

        :default: CloudFormation provided name.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Optional port number for the listener.

        If not supplied, will default to 80 or 443, depending on the Protocol

        :default: 80 or 443 depending on the Protocol

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        '''(experimental) protocol that the listener will listen on.

        :default: HTTPS

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional["Protocol"], result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List["RuleProp"]]:
        '''(experimental) rules for the listener.

        :stability: experimental
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List["RuleProp"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoggingDestination(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="aws-vpclattice-prealpha.LoggingDestination",
):
    '''(experimental) Logging options.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="cloudwatch")
    @builtins.classmethod
    def cloudwatch(
        cls,
        log_group: _aws_cdk_aws_logs_ceddda9d.ILogGroup,
    ) -> "LoggingDestination":
        '''(experimental) Send to CLoudwatch.

        :param log_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65fbe8af34569ae5b49f723939433775f2758f47c325f0b2023c22d9c7838fa8)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("LoggingDestination", jsii.sinvoke(cls, "cloudwatch", [log_group]))

    @jsii.member(jsii_name="kinesis")
    @builtins.classmethod
    def kinesis(
        cls,
        stream: _aws_cdk_aws_kinesis_ceddda9d.IStream,
    ) -> "LoggingDestination":
        '''(experimental) Stream to Kinesis.

        :param stream: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a734623fe81363d29a1c3070244ecfa8e49152584668c9f7754e5a6e5a153748)
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
        return typing.cast("LoggingDestination", jsii.sinvoke(cls, "kinesis", [stream]))

    @jsii.member(jsii_name="s3")
    @builtins.classmethod
    def s3(cls, bucket: _aws_cdk_aws_s3_ceddda9d.IBucket) -> "LoggingDestination":
        '''(experimental) Construct a logging destination for a S3 Bucket.

        :param bucket: an s3 bucket.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b5df1dc69409b6b0939b62d8b509bf75454dae7b761dee61b9fdc3aaab12b1)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("LoggingDestination", jsii.sinvoke(cls, "s3", [bucket]))

    @builtins.property
    @jsii.member(jsii_name="addr")
    @abc.abstractmethod
    def addr(self) -> builtins.str:
        '''(experimental) unique addr of the destination.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="arn")
    @abc.abstractmethod
    def arn(self) -> builtins.str:
        '''(experimental) An Arn of the destination.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    @abc.abstractmethod
    def name(self) -> builtins.str:
        '''(experimental) A name of the destination.

        :stability: experimental
        '''
        ...


class _LoggingDestinationProxy(LoggingDestination):
    @builtins.property
    @jsii.member(jsii_name="addr")
    def addr(self) -> builtins.str:
        '''(experimental) unique addr of the destination.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "addr"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) An Arn of the destination.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) A name of the destination.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, LoggingDestination).__jsii_proxy_class__ = lambda : _LoggingDestinationProxy


@jsii.enum(jsii_type="aws-vpclattice-prealpha.MatchOperator")
class MatchOperator(enum.Enum):
    '''(experimental) Operators for Matches.

    :stability: experimental
    '''

    CONTAINS = "CONTAINS"
    '''(experimental) Contains Match.

    :stability: experimental
    '''
    EXACT = "EXACT"
    '''(experimental) Exact Match.

    :stability: experimental
    '''
    PREFIX = "PREFIX"
    '''(experimental) Prefix Match.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.PathMatch",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "case_sensitive": "caseSensitive",
        "path_match_type": "pathMatchType",
    },
)
class PathMatch:
    def __init__(
        self,
        *,
        path: builtins.str,
        case_sensitive: typing.Optional[builtins.bool] = None,
        path_match_type: typing.Optional["PathMatchType"] = None,
    ) -> None:
        '''(experimental) Properties to create a PathMatch.

        :param path: (experimental) Value to match against.
        :param case_sensitive: (experimental) Should the match be case sensitive? Default: true
        :param path_match_type: (experimental) Type of match to make. Default: PathMatchType.EXACT

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702732e343b1a7a05bed7ce0fdc2ad13ca491ad2a880b7f97f1fbd850e11b32e)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument case_sensitive", value=case_sensitive, expected_type=type_hints["case_sensitive"])
            check_type(argname="argument path_match_type", value=path_match_type, expected_type=type_hints["path_match_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if case_sensitive is not None:
            self._values["case_sensitive"] = case_sensitive
        if path_match_type is not None:
            self._values["path_match_type"] = path_match_type

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) Value to match against.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def case_sensitive(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Should the match be case sensitive?

        :default: true

        :stability: experimental
        '''
        result = self._values.get("case_sensitive")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def path_match_type(self) -> typing.Optional["PathMatchType"]:
        '''(experimental) Type of match to make.

        :default: PathMatchType.EXACT

        :stability: experimental
        '''
        result = self._values.get("path_match_type")
        return typing.cast(typing.Optional["PathMatchType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PathMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-vpclattice-prealpha.PathMatchType")
class PathMatchType(enum.Enum):
    '''(experimental) Operators for Path Matches.

    :stability: experimental
    '''

    EXACT = "EXACT"
    '''(experimental) Exact Match.

    :stability: experimental
    '''
    PREFIX = "PREFIX"
    '''(experimental) Prefix Match.

    :stability: experimental
    '''


@jsii.enum(jsii_type="aws-vpclattice-prealpha.Protocol")
class Protocol(enum.Enum):
    '''(experimental) HTTP/HTTPS methods.

    :stability: experimental
    '''

    HTTP = "HTTP"
    '''(experimental) HTTP Protocol.

    :stability: experimental
    '''
    HTTPS = "HTTPS"
    '''(experimental) HTTPS Protocol.

    :stability: experimental
    '''


@jsii.enum(jsii_type="aws-vpclattice-prealpha.RuleAccessMode")
class RuleAccessMode(enum.Enum):
    '''(experimental) Access mode for the rule.

    :stability: experimental
    '''

    UNAUTHENTICATED = "UNAUTHENTICATED"
    '''(experimental) Unauthenticated Access.

    :stability: experimental
    '''
    AUTHENTICATED_ONLY = "AUTHENTICATED_ONLY"
    '''(experimental) Unauthenticated Access.

    :stability: experimental
    '''
    ORG_ONLY = "ORG_ONLY"
    '''(experimental) THIS Org only.

    :stability: experimental
    '''
    NO_STATEMENT = "NO_STATEMENT"
    '''(experimental) Do not create a s.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.RuleProp",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "http_match": "httpMatch",
        "name": "name",
        "access_mode": "accessMode",
        "allowed_principal_arn": "allowedPrincipalArn",
        "allowed_principals": "allowedPrincipals",
        "priority": "priority",
    },
)
class RuleProp:
    def __init__(
        self,
        *,
        action: typing.Union[FixedResponse, typing.Sequence[typing.Union["WeightedTargetGroup", typing.Dict[builtins.str, typing.Any]]]],
        http_match: typing.Union[HTTPMatch, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        access_mode: typing.Optional[RuleAccessMode] = None,
        allowed_principal_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_principals: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IPrincipal]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties to add rules to to a listener One of headerMatch, PathMatch, or methodMatch can be supplied, the Rule can not match multiple Types.

        :param action: (experimental) the action for the rule, is either a fixed Reponse, or a being sent to Weighted TargetGroup.
        :param http_match: (experimental) the Matching criteria for the rule. This must contain at least one of header, method or patchMatches
        :param name: (experimental) A name for the the Rule.
        :param access_mode: (experimental) Set an access mode. Default: false
        :param allowed_principal_arn: (experimental) List of principalArns that are allowed to access the resource. Default: none
        :param allowed_principals: (experimental) List of principals that are allowed to access the resource. Default: none
        :param priority: (experimental) the priority of this rule, a lower priority will be processed first. Default: 50

        :stability: experimental
        '''
        if isinstance(http_match, dict):
            http_match = HTTPMatch(**http_match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef52623acd059fdd95b01760a388f3671e3961d089c325fe8bede2fb84ad61c)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument http_match", value=http_match, expected_type=type_hints["http_match"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument access_mode", value=access_mode, expected_type=type_hints["access_mode"])
            check_type(argname="argument allowed_principal_arn", value=allowed_principal_arn, expected_type=type_hints["allowed_principal_arn"])
            check_type(argname="argument allowed_principals", value=allowed_principals, expected_type=type_hints["allowed_principals"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "http_match": http_match,
            "name": name,
        }
        if access_mode is not None:
            self._values["access_mode"] = access_mode
        if allowed_principal_arn is not None:
            self._values["allowed_principal_arn"] = allowed_principal_arn
        if allowed_principals is not None:
            self._values["allowed_principals"] = allowed_principals
        if priority is not None:
            self._values["priority"] = priority

    @builtins.property
    def action(self) -> typing.Union[FixedResponse, typing.List["WeightedTargetGroup"]]:
        '''(experimental) the action for the rule, is either a fixed Reponse, or a being sent to  Weighted TargetGroup.

        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(typing.Union[FixedResponse, typing.List["WeightedTargetGroup"]], result)

    @builtins.property
    def http_match(self) -> HTTPMatch:
        '''(experimental) the Matching criteria for the rule.

        This must contain at least one of
        header, method or patchMatches

        :stability: experimental
        '''
        result = self._values.get("http_match")
        assert result is not None, "Required property 'http_match' is missing"
        return typing.cast(HTTPMatch, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) A name for the the Rule.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_mode(self) -> typing.Optional[RuleAccessMode]:
        '''(experimental) Set an access mode.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("access_mode")
        return typing.cast(typing.Optional[RuleAccessMode], result)

    @builtins.property
    def allowed_principal_arn(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of principalArns that are allowed to access the resource.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("allowed_principal_arn")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_principals(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IPrincipal]]:
        '''(experimental) List of principals that are allowed to access the resource.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("allowed_principals")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IPrincipal]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) the priority of this rule, a lower priority will be processed first.

        :default: 50

        :stability: experimental
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleProp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IService)
class Service(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-vpclattice-prealpha.Service",
):
    '''(experimental) Create a vpcLattice Service.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        auth_type: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate] = None,
        custom_domain: typing.Optional[builtins.str] = None,
        hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
        listeners: typing.Optional[typing.Sequence[IListener]] = None,
        name: typing.Optional[builtins.str] = None,
        service_network: typing.Optional[IServiceNetwork] = None,
        shares: typing.Optional[typing.Sequence[typing.Union["ShareServiceProps", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param auth_type: (experimental) The authType of the Service. Default: 'AWS_IAM'
        :param certificate: (experimental) A certificate that may be used by the service. Default: no custom certificate is used
        :param custom_domain: (experimental) A customDomain used by the service. Default: no customdomain is used
        :param hosted_zone: (experimental) A custom hosname. Default: no hostname is used
        :param listeners: (experimental) Listeners that will be attached to the service. Default: no listeners
        :param name: (experimental) Name for the service. Default: cloudformation will provide a name
        :param service_network: (experimental) ServiceNetwork to associate with. Default: will not assocaite with any serviceNetwork.
        :param shares: (experimental) Share Service. Default: no sharing of the service

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a33850b7c5e8418f477213ab06d5800d7a1845d919e83a51f66eeba45ca78d20)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ServiceProps(
            auth_type=auth_type,
            certificate=certificate,
            custom_domain=custom_domain,
            hosted_zone=hosted_zone,
            listeners=listeners,
            name=name,
            service_network=service_network,
            shares=shares,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromServiceId")
    @builtins.classmethod
    def from_service_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        service_id: builtins.str,
    ) -> IService:
        '''(experimental) import a service from Id.

        :param scope: -
        :param id: -
        :param service_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__536d2d64bd917ab406b346c442d8676cef65b1df3cd0ea48290ac1f0320ab3d3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
        return typing.cast(IService, jsii.sinvoke(cls, "fromServiceId", [scope, id, service_id]))

    @jsii.member(jsii_name="addPolicyStatement")
    def add_policy_statement(
        self,
        statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
    ) -> None:
        '''(experimental) Add a PolicyStatement.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa284bcf9140f3788b7e5882133f718a7901612c937e10c2d5139b8caa1ac834)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(None, jsii.invoke(self, "addPolicyStatement", [statement]))

    @jsii.member(jsii_name="applyAuthPolicy")
    def apply_auth_policy(self) -> _aws_cdk_aws_iam_ceddda9d.PolicyDocument:
        '''(experimental) apply an authpolicy.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.PolicyDocument, jsii.invoke(self, "applyAuthPolicy", []))

    @jsii.member(jsii_name="associateWithServiceNetwork")
    def associate_with_service_network(self, service_network: IServiceNetwork) -> None:
        '''(experimental) Associate with a Service Network.

        :param service_network: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37fae3757cb060322eb4b5581dd9f1b58b5450034337dd448faaf5c4a423033)
            check_type(argname="argument service_network", value=service_network, expected_type=type_hints["service_network"])
        return typing.cast(None, jsii.invoke(self, "associateWithServiceNetwork", [service_network]))

    @jsii.member(jsii_name="grantAccess")
    def grant_access(
        self,
        principals: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IPrincipal],
    ) -> None:
        '''(experimental) .grantAccess on a lattice service, will permit the principals to access all of the service. Consider using more granual permissions at the rule level.

        :param principals: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c4cee15734969107c7bc804a65dcb9a92b7a78bbe3690cb36405f531b98bdb)
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
        return typing.cast(None, jsii.invoke(self, "grantAccess", [principals]))

    @jsii.member(jsii_name="shareToAccounts")
    def share_to_accounts(
        self,
        *,
        name: builtins.str,
        accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_external_principals: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Share the service to other accounts via RAM.

        :param name: (experimental) The name of the service.
        :param accounts: (experimental) Principals to share the service with. TO DO, this needs some work Default: none
        :param allow_external_principals: (experimental) Allow External Principals. Default: false

        :stability: experimental
        '''
        props = ShareServiceProps(
            name=name,
            accounts=accounts,
            allow_external_principals=allow_external_principals,
        )

        return typing.cast(None, jsii.invoke(self, "shareToAccounts", [props]))

    @builtins.property
    @jsii.member(jsii_name="imported")
    def imported(self) -> builtins.bool:
        '''(experimental) Imported.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "imported"))

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> builtins.str:
        '''(experimental) The Arn of the Service.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceArn"))

    @builtins.property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> builtins.str:
        '''(experimental) The Id of the Service.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceId"))

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) the discovered OrgId.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgId"))

    @builtins.property
    @jsii.member(jsii_name="authPolicy")
    def auth_policy(self) -> _aws_cdk_aws_iam_ceddda9d.PolicyDocument:
        '''(experimental) The auth Policy for the service.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.PolicyDocument, jsii.get(self, "authPolicy"))

    @auth_policy.setter
    def auth_policy(self, value: _aws_cdk_aws_iam_ceddda9d.PolicyDocument) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04d36f2c70158faece2d30ac5a65d0145e34a90b550b76c3c67827c388fdda0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The authType of the service.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__260aa4ceb0330c49c77c173a149e81fc9e9aeeba877134d2f44164c65e1c271d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate]:
        '''(experimental) A certificate that may be used by the service.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(
        self,
        value: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44371e27a83554ed17ad32d0b903051edec2a60d31e2151e2bac2b2a69e32612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="customDomain")
    def custom_domain(self) -> typing.Optional[builtins.str]:
        '''(experimental) A custom Domain used by the service.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDomain"))

    @custom_domain.setter
    def custom_domain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa902b9cb442b40c6d2858638e478d4eeee07a846a3473c67f1927a5dcc4417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDomain", value)

    @builtins.property
    @jsii.member(jsii_name="hostedZone")
    def hosted_zone(self) -> typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone]:
        '''(experimental) A DNS Entry for the service.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone], jsii.get(self, "hostedZone"))

    @hosted_zone.setter
    def hosted_zone(
        self,
        value: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f84ca3ed6facb06b8860be0bd622971c6437a32302316501d9f2ec0869c4aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostedZone", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the service.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea6ff9c2840e668bc6ba0ae4c2d75662f92448caa9b12b819c73607abd8dd77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


class ServiceAssociation(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-vpclattice-prealpha.ServiceAssociation",
):
    '''(experimental) Creates an Association Between a Lattice Service and a Service Network.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        service: IService,
        service_network_id: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param service: (experimental) lattice Service.
        :param service_network_id: (experimental) Lattice ServiceId.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c92784ccec40fd5bbc425457ea7b2d583f16d81909b714b1db1487c3a33b4a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ServiceAssociationProps(
            service=service, service_network_id=service_network_id
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.ServiceAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"service": "service", "service_network_id": "serviceNetworkId"},
)
class ServiceAssociationProps:
    def __init__(self, *, service: IService, service_network_id: builtins.str) -> None:
        '''(experimental) Props for Service Assocaition.

        :param service: (experimental) lattice Service.
        :param service_network_id: (experimental) Lattice ServiceId.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29e0f0596a05248b29caf1321d3ac1ea461640e88139abb0708fc6fa38216679)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument service_network_id", value=service_network_id, expected_type=type_hints["service_network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
            "service_network_id": service_network_id,
        }

    @builtins.property
    def service(self) -> IService:
        '''(experimental) lattice Service.

        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(IService, result)

    @builtins.property
    def service_network_id(self) -> builtins.str:
        '''(experimental) Lattice ServiceId.

        :stability: experimental
        '''
        result = self._values.get("service_network_id")
        assert result is not None, "Required property 'service_network_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IServiceNetwork)
class ServiceNetwork(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-vpclattice-prealpha.ServiceNetwork",
):
    '''(experimental) Create a vpcLattice Service Network.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        accessmode: typing.Optional["ServiceNetworkAccessMode"] = None,
        auth_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        auth_type: typing.Optional[AuthType] = None,
        logging_destinations: typing.Optional[typing.Sequence[LoggingDestination]] = None,
        name: typing.Optional[builtins.str] = None,
        services: typing.Optional[typing.Sequence[IService]] = None,
        vpcs: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.IVpc]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param accessmode: (experimental) Allow external principals. Default: false
        :param auth_statements: (experimental) Additional AuthStatments:.
        :param auth_type: (experimental) The type of authentication to use with the Service Network. Default: 'AWS_IAM'
        :param logging_destinations: (experimental) Logging destinations. Default: : no logging
        :param name: (experimental) The name of the Service Network. If not provided Cloudformation will provide a name Default: cloudformation generated name
        :param services: (experimental) Lattice Services that are assocaited with this Service Network. Default: no services are associated with the service network
        :param vpcs: (experimental) Vpcs that are associated with this Service Network. Default: no vpcs are associated

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de151a2ad4bc98964269dae761de01f5e454e7dc434e2e1b4a0fb7f43ea5410a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ServiceNetworkProps(
            accessmode=accessmode,
            auth_statements=auth_statements,
            auth_type=auth_type,
            logging_destinations=logging_destinations,
            name=name,
            services=services,
            vpcs=vpcs,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromId")
    @builtins.classmethod
    def from_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        service_network_id: builtins.str,
    ) -> IServiceNetwork:
        '''(experimental) Import a Service Network by Id.

        :param scope: -
        :param id: -
        :param service_network_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9243fcd9f7589f40cf588ea260858b4b3eec8f1368ceadc62e433f7715c522cc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument service_network_id", value=service_network_id, expected_type=type_hints["service_network_id"])
        return typing.cast(IServiceNetwork, jsii.sinvoke(cls, "fromId", [scope, id, service_network_id]))

    @jsii.member(jsii_name="fromName")
    @builtins.classmethod
    def from_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        service_network_name: builtins.str,
    ) -> IServiceNetwork:
        '''
        :param scope: -
        :param id: -
        :param service_network_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ec1a40d648e8ddf40761db7d89c9fc1a1cfe16a9b8c657725d7bcffcd38fd0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument service_network_name", value=service_network_name, expected_type=type_hints["service_network_name"])
        return typing.cast(IServiceNetwork, jsii.sinvoke(cls, "fromName", [scope, id, service_network_name]))

    @jsii.member(jsii_name="addloggingDestination")
    def addlogging_destination(self, *, destination: LoggingDestination) -> None:
        '''(experimental) send logs to a destination.

        :param destination: (experimental) The logging destination.

        :stability: experimental
        '''
        props = AddloggingDestinationProps(destination=destination)

        return typing.cast(None, jsii.invoke(self, "addloggingDestination", [props]))

    @jsii.member(jsii_name="addService")
    def add_service(
        self,
        *,
        service: IService,
        service_network_id: builtins.str,
    ) -> None:
        '''(experimental) Add A lattice service to a lattice network.

        :param service: (experimental) The Service to add to the Service Network.
        :param service_network_id: (experimental) The Service Network to add the Service to.

        :stability: experimental
        '''
        props = AddServiceProps(service=service, service_network_id=service_network_id)

        return typing.cast(None, jsii.invoke(self, "addService", [props]))

    @jsii.member(jsii_name="addStatementToAuthPolicy")
    def add_statement_to_auth_policy(
        self,
        statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
    ) -> None:
        '''(experimental) This will give the principals access to all resources that are on this service network.

        This is a broad permission.
        Consider granting Access at the Service
        addToResourcePolicy()

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e786816186e43e34cc91b53da5c90a18cf73c201e5c0dd2c2d5970a23526f9)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(None, jsii.invoke(self, "addStatementToAuthPolicy", [statement]))

    @jsii.member(jsii_name="applyAuthPolicyToServiceNetwork")
    def apply_auth_policy_to_service_network(self) -> None:
        '''(experimental) Apply the AuthPolicy to a Service Network.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "applyAuthPolicyToServiceNetwork", []))

    @jsii.member(jsii_name="associateVPC")
    def associate_vpc(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]] = None,
    ) -> None:
        '''(experimental) Associate a VPC with the Service Network This provides an opinionated default of adding a security group to allow inbound 443.

        :param vpc: (experimental) The VPC to associate with the Service Network.
        :param security_groups: (experimental) The security groups to associate with the Service Network. Default: a security group that allows inbound 443 will be permitted.

        :stability: experimental
        '''
        props = AssociateVPCProps(vpc=vpc, security_groups=security_groups)

        return typing.cast(None, jsii.invoke(self, "associateVPC", [props]))

    @jsii.member(jsii_name="share")
    def share(
        self,
        *,
        accounts: typing.Sequence[builtins.str],
        name: builtins.str,
        access_mode: typing.Optional["ServiceNetworkAccessMode"] = None,
        allow_external_principals: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        disable_discovery: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Share the The Service network using RAM.

        :param accounts: (experimental) Principals to share the Service Network with. Default: none
        :param name: (experimental) The name of the share.
        :param access_mode: (experimental) The access mode for the Service Network. Default: 'UNAUTHENTICATED'
        :param allow_external_principals: (experimental) Are external Principals allowed. Default: false;
        :param description: (experimental) The description of the Service Network. Default: none
        :param disable_discovery: (experimental) disable discovery. Default: false
        :param tags: (experimental) The tags to apply to the Service Network. Default: none

        :stability: experimental
        '''
        props = ShareServiceNetworkProps(
            accounts=accounts,
            name=name,
            access_mode=access_mode,
            allow_external_principals=allow_external_principals,
            description=description,
            disable_discovery=disable_discovery,
            tags=tags,
        )

        return typing.cast(None, jsii.invoke(self, "share", [props]))

    @builtins.property
    @jsii.member(jsii_name="imported")
    def imported(self) -> builtins.bool:
        '''(experimental) imported.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "imported"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) Name of the ServiceNetwork.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkArn")
    def service_network_arn(self) -> builtins.str:
        '''(experimental) The Arn of the service network.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceNetworkArn"))

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkId")
    def service_network_id(self) -> builtins.str:
        '''(experimental) The Id of the Service Network.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceNetworkId"))

    @builtins.property
    @jsii.member(jsii_name="authPolicy")
    def auth_policy(self) -> _aws_cdk_aws_iam_ceddda9d.PolicyDocument:
        '''(experimental) A managed Policy that is the auth policy.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.PolicyDocument, jsii.get(self, "authPolicy"))

    @auth_policy.setter
    def auth_policy(self, value: _aws_cdk_aws_iam_ceddda9d.PolicyDocument) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e980f16275c01a927459b29042c01b665e25c653f12f3ddb4cb88f9a2d13901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> typing.Optional[AuthType]:
        '''(experimental) the authType of the service network.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[AuthType], jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: typing.Optional[AuthType]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283532f01625f252eaef51db2c0cfa7ae01d90dab5f5f659bc84dcf8aea1eac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value)


@jsii.enum(jsii_type="aws-vpclattice-prealpha.ServiceNetworkAccessMode")
class ServiceNetworkAccessMode(enum.Enum):
    '''(experimental) AccesModes.

    :stability: experimental
    '''

    UNAUTHENTICATED = "UNAUTHENTICATED"
    '''(experimental) Unauthenticated Access.

    :stability: experimental
    '''
    AUTHENTICATED_ONLY = "AUTHENTICATED_ONLY"
    '''(experimental) Unauthenticated Access.

    :stability: experimental
    '''
    ORG_ONLY = "ORG_ONLY"
    '''(experimental) THIS Org only.

    :stability: experimental
    '''


class ServiceNetworkAssociation(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-vpclattice-prealpha.ServiceNetworkAssociation",
):
    '''(experimental) Creates an Association Between a Lattice Service and a Service Network consider using .associateWithServiceNetwork.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        service_id: builtins.str,
        service_network: IServiceNetwork,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param service_id: (experimental) Lattice ServiceId.
        :param service_network: (experimental) lattice Service.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e45e0945bfa3da60848fec97f96879fb705e79c77723361651f24f55d8804e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ServiceNetworkAssociationProps(
            service_id=service_id, service_network=service_network
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.ServiceNetworkAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"service_id": "serviceId", "service_network": "serviceNetwork"},
)
class ServiceNetworkAssociationProps:
    def __init__(
        self,
        *,
        service_id: builtins.str,
        service_network: IServiceNetwork,
    ) -> None:
        '''(experimental) Props for Service Assocaition.

        :param service_id: (experimental) Lattice ServiceId.
        :param service_network: (experimental) lattice Service.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bafe9c29c25ac5fb0f856db1bbf30cab5fac093a313d72c236eded05925d762)
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
            check_type(argname="argument service_network", value=service_network, expected_type=type_hints["service_network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_id": service_id,
            "service_network": service_network,
        }

    @builtins.property
    def service_id(self) -> builtins.str:
        '''(experimental) Lattice ServiceId.

        :stability: experimental
        '''
        result = self._values.get("service_id")
        assert result is not None, "Required property 'service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_network(self) -> IServiceNetwork:
        '''(experimental) lattice Service.

        :stability: experimental
        '''
        result = self._values.get("service_network")
        assert result is not None, "Required property 'service_network' is missing"
        return typing.cast(IServiceNetwork, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceNetworkAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.ServiceNetworkProps",
    jsii_struct_bases=[],
    name_mapping={
        "accessmode": "accessmode",
        "auth_statements": "authStatements",
        "auth_type": "authType",
        "logging_destinations": "loggingDestinations",
        "name": "name",
        "services": "services",
        "vpcs": "vpcs",
    },
)
class ServiceNetworkProps:
    def __init__(
        self,
        *,
        accessmode: typing.Optional[ServiceNetworkAccessMode] = None,
        auth_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        auth_type: typing.Optional[AuthType] = None,
        logging_destinations: typing.Optional[typing.Sequence[LoggingDestination]] = None,
        name: typing.Optional[builtins.str] = None,
        services: typing.Optional[typing.Sequence[IService]] = None,
        vpcs: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.IVpc]] = None,
    ) -> None:
        '''(experimental) The properties for the ServiceNetwork.

        :param accessmode: (experimental) Allow external principals. Default: false
        :param auth_statements: (experimental) Additional AuthStatments:.
        :param auth_type: (experimental) The type of authentication to use with the Service Network. Default: 'AWS_IAM'
        :param logging_destinations: (experimental) Logging destinations. Default: : no logging
        :param name: (experimental) The name of the Service Network. If not provided Cloudformation will provide a name Default: cloudformation generated name
        :param services: (experimental) Lattice Services that are assocaited with this Service Network. Default: no services are associated with the service network
        :param vpcs: (experimental) Vpcs that are associated with this Service Network. Default: no vpcs are associated

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c5b474503b3d82c41ab24892bfd41523b749529c0d3b3060a5058d4a0226d6)
            check_type(argname="argument accessmode", value=accessmode, expected_type=type_hints["accessmode"])
            check_type(argname="argument auth_statements", value=auth_statements, expected_type=type_hints["auth_statements"])
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument logging_destinations", value=logging_destinations, expected_type=type_hints["logging_destinations"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
            check_type(argname="argument vpcs", value=vpcs, expected_type=type_hints["vpcs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accessmode is not None:
            self._values["accessmode"] = accessmode
        if auth_statements is not None:
            self._values["auth_statements"] = auth_statements
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if logging_destinations is not None:
            self._values["logging_destinations"] = logging_destinations
        if name is not None:
            self._values["name"] = name
        if services is not None:
            self._values["services"] = services
        if vpcs is not None:
            self._values["vpcs"] = vpcs

    @builtins.property
    def accessmode(self) -> typing.Optional[ServiceNetworkAccessMode]:
        '''(experimental) Allow external principals.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("accessmode")
        return typing.cast(typing.Optional[ServiceNetworkAccessMode], result)

    @builtins.property
    def auth_statements(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]]:
        '''(experimental) Additional AuthStatments:.

        :stability: experimental
        '''
        result = self._values.get("auth_statements")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]], result)

    @builtins.property
    def auth_type(self) -> typing.Optional[AuthType]:
        '''(experimental) The type of  authentication to use with the Service Network.

        :default: 'AWS_IAM'

        :stability: experimental
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[AuthType], result)

    @builtins.property
    def logging_destinations(self) -> typing.Optional[typing.List[LoggingDestination]]:
        '''(experimental) Logging destinations.

        :default: : no logging

        :stability: experimental
        '''
        result = self._values.get("logging_destinations")
        return typing.cast(typing.Optional[typing.List[LoggingDestination]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the Service Network.

        If not provided Cloudformation will provide
        a name

        :default: cloudformation generated name

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def services(self) -> typing.Optional[typing.List[IService]]:
        '''(experimental) Lattice Services that are assocaited with this Service Network.

        :default: no services are associated with the service network

        :stability: experimental
        '''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.List[IService]], result)

    @builtins.property
    def vpcs(self) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.IVpc]]:
        '''(experimental) Vpcs that are associated with this Service Network.

        :default: no vpcs are associated

        :stability: experimental
        '''
        result = self._values.get("vpcs")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.IVpc]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.ServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "certificate": "certificate",
        "custom_domain": "customDomain",
        "hosted_zone": "hostedZone",
        "listeners": "listeners",
        "name": "name",
        "service_network": "serviceNetwork",
        "shares": "shares",
    },
)
class ServiceProps:
    def __init__(
        self,
        *,
        auth_type: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate] = None,
        custom_domain: typing.Optional[builtins.str] = None,
        hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
        listeners: typing.Optional[typing.Sequence[IListener]] = None,
        name: typing.Optional[builtins.str] = None,
        service_network: typing.Optional[IServiceNetwork] = None,
        shares: typing.Optional[typing.Sequence[typing.Union["ShareServiceProps", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties for a Lattice Service.

        :param auth_type: (experimental) The authType of the Service. Default: 'AWS_IAM'
        :param certificate: (experimental) A certificate that may be used by the service. Default: no custom certificate is used
        :param custom_domain: (experimental) A customDomain used by the service. Default: no customdomain is used
        :param hosted_zone: (experimental) A custom hosname. Default: no hostname is used
        :param listeners: (experimental) Listeners that will be attached to the service. Default: no listeners
        :param name: (experimental) Name for the service. Default: cloudformation will provide a name
        :param service_network: (experimental) ServiceNetwork to associate with. Default: will not assocaite with any serviceNetwork.
        :param shares: (experimental) Share Service. Default: no sharing of the service

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d46d70cae814eabdfefba7001e4d74ae5941b4dfac46989c922623f9c2c6e54c)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument custom_domain", value=custom_domain, expected_type=type_hints["custom_domain"])
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
            check_type(argname="argument listeners", value=listeners, expected_type=type_hints["listeners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_network", value=service_network, expected_type=type_hints["service_network"])
            check_type(argname="argument shares", value=shares, expected_type=type_hints["shares"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if certificate is not None:
            self._values["certificate"] = certificate
        if custom_domain is not None:
            self._values["custom_domain"] = custom_domain
        if hosted_zone is not None:
            self._values["hosted_zone"] = hosted_zone
        if listeners is not None:
            self._values["listeners"] = listeners
        if name is not None:
            self._values["name"] = name
        if service_network is not None:
            self._values["service_network"] = service_network
        if shares is not None:
            self._values["shares"] = shares

    @builtins.property
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The authType of the Service.

        :default: 'AWS_IAM'

        :stability: experimental
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate]:
        '''(experimental) A certificate that may be used by the service.

        :default: no custom certificate is used

        :stability: experimental
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate], result)

    @builtins.property
    def custom_domain(self) -> typing.Optional[builtins.str]:
        '''(experimental) A customDomain used by the service.

        :default: no customdomain is used

        :stability: experimental
        '''
        result = self._values.get("custom_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hosted_zone(self) -> typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone]:
        '''(experimental) A custom hosname.

        :default: no hostname is used

        :stability: experimental
        '''
        result = self._values.get("hosted_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone], result)

    @builtins.property
    def listeners(self) -> typing.Optional[typing.List[IListener]]:
        '''(experimental) Listeners that will be attached to the service.

        :default: no listeners

        :stability: experimental
        '''
        result = self._values.get("listeners")
        return typing.cast(typing.Optional[typing.List[IListener]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name for the service.

        :default: cloudformation will provide a name

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_network(self) -> typing.Optional[IServiceNetwork]:
        '''(experimental) ServiceNetwork to associate with.

        :default: will not assocaite with any serviceNetwork.

        :stability: experimental
        '''
        result = self._values.get("service_network")
        return typing.cast(typing.Optional[IServiceNetwork], result)

    @builtins.property
    def shares(self) -> typing.Optional[typing.List["ShareServiceProps"]]:
        '''(experimental) Share Service.

        :default: no sharing of the service

        :stability: experimental
        '''
        result = self._values.get("shares")
        return typing.cast(typing.Optional[typing.List["ShareServiceProps"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.ShareServiceNetworkProps",
    jsii_struct_bases=[],
    name_mapping={
        "accounts": "accounts",
        "name": "name",
        "access_mode": "accessMode",
        "allow_external_principals": "allowExternalPrincipals",
        "description": "description",
        "disable_discovery": "disableDiscovery",
        "tags": "tags",
    },
)
class ShareServiceNetworkProps:
    def __init__(
        self,
        *,
        accounts: typing.Sequence[builtins.str],
        name: builtins.str,
        access_mode: typing.Optional[ServiceNetworkAccessMode] = None,
        allow_external_principals: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        disable_discovery: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties to share a Service Network.

        :param accounts: (experimental) Principals to share the Service Network with. Default: none
        :param name: (experimental) The name of the share.
        :param access_mode: (experimental) The access mode for the Service Network. Default: 'UNAUTHENTICATED'
        :param allow_external_principals: (experimental) Are external Principals allowed. Default: false;
        :param description: (experimental) The description of the Service Network. Default: none
        :param disable_discovery: (experimental) disable discovery. Default: false
        :param tags: (experimental) The tags to apply to the Service Network. Default: none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fedf0cf4f5d543e3ab39b8f8e7dac5b1f8a6f8c1ed0923cb1d1264ea676fccf)
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument access_mode", value=access_mode, expected_type=type_hints["access_mode"])
            check_type(argname="argument allow_external_principals", value=allow_external_principals, expected_type=type_hints["allow_external_principals"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_discovery", value=disable_discovery, expected_type=type_hints["disable_discovery"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accounts": accounts,
            "name": name,
        }
        if access_mode is not None:
            self._values["access_mode"] = access_mode
        if allow_external_principals is not None:
            self._values["allow_external_principals"] = allow_external_principals
        if description is not None:
            self._values["description"] = description
        if disable_discovery is not None:
            self._values["disable_discovery"] = disable_discovery
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def accounts(self) -> typing.List[builtins.str]:
        '''(experimental) Principals to share the Service Network with.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("accounts")
        assert result is not None, "Required property 'accounts' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the share.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_mode(self) -> typing.Optional[ServiceNetworkAccessMode]:
        '''(experimental) The access mode for the Service Network.

        :default: 'UNAUTHENTICATED'

        :stability: experimental
        '''
        result = self._values.get("access_mode")
        return typing.cast(typing.Optional[ServiceNetworkAccessMode], result)

    @builtins.property
    def allow_external_principals(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Are external Principals allowed.

        :default: false;

        :stability: experimental
        '''
        result = self._values.get("allow_external_principals")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the Service Network.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_discovery(self) -> typing.Optional[builtins.bool]:
        '''(experimental) disable discovery.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("disable_discovery")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The tags to apply to the Service Network.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ShareServiceNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.ShareServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "accounts": "accounts",
        "allow_external_principals": "allowExternalPrincipals",
    },
)
class ShareServiceProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_external_principals: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties to Share the Service.

        :param name: (experimental) The name of the service.
        :param accounts: (experimental) Principals to share the service with. TO DO, this needs some work Default: none
        :param allow_external_principals: (experimental) Allow External Principals. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5e29e3fa88298a4e4928c04749904336e3eacf2b5a4bfee01853dd10bfda192)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
            check_type(argname="argument allow_external_principals", value=allow_external_principals, expected_type=type_hints["allow_external_principals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if accounts is not None:
            self._values["accounts"] = accounts
        if allow_external_principals is not None:
            self._values["allow_external_principals"] = allow_external_principals

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the service.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Principals to share the service with.

        TO DO, this needs some work

        :default: none

        :stability: experimental
        '''
        result = self._values.get("accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_external_principals(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow External Principals.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("allow_external_principals")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ShareServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITargetGroup)
class TargetGroup(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-vpclattice-prealpha.TargetGroup",
):
    '''(experimental) Create a vpc lattice TargetGroup.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        target: ITarget,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: (experimental) The name of the target group.
        :param target: (experimental) Targets.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a176a630861c516852778a8ed1f5049196b91a41c7e45a8e1acd70bf582bcaf8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TargetGroupProps(name=name, target=target)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> builtins.str:
        '''(experimental) The Arn of the targetGroup.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupId")
    def target_group_id(self) -> builtins.str:
        '''(experimental) The id of the target group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetGroupId"))


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.TargetGroupProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "target": "target"},
)
class TargetGroupProps:
    def __init__(self, *, name: builtins.str, target: ITarget) -> None:
        '''(experimental) Properties for a Target Group, Only supply one of instancetargets, lambdaTargets, albTargets, ipTargets.

        :param name: (experimental) The name of the target group.
        :param target: (experimental) Targets.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47f30a4764ceb906bba13a9afa50eab0d3d4c412fc4de8631056c26d8ef3203)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "target": target,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the target group.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> ITarget:
        '''(experimental) Targets.

        :stability: experimental
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(ITarget, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-vpclattice-prealpha.WeightedTargetGroup",
    jsii_struct_bases=[],
    name_mapping={"target_group": "targetGroup", "weight": "weight"},
)
class WeightedTargetGroup:
    def __init__(
        self,
        *,
        target_group: TargetGroup,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target_group: (experimental) A target Group.
        :param weight: (experimental) A weight for the target group. Default: 100

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d09cf15092c702ea025dfe6852c3cb360bbc14e79272beccfa8a13e66a0c48c4)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_group": target_group,
        }
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def target_group(self) -> TargetGroup:
        '''(experimental) A target Group.

        :stability: experimental
        '''
        result = self._values.get("target_group")
        assert result is not None, "Required property 'target_group' is missing"
        return typing.cast(TargetGroup, result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''(experimental) A weight for the target group.

        :default: 100

        :stability: experimental
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WeightedTargetGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddServiceProps",
    "AddloggingDestinationProps",
    "AssociateVPCProps",
    "AssociateVpc",
    "AssociateVpcProps",
    "AuthType",
    "DefaultListenerAction",
    "FixedResponse",
    "HTTPMatch",
    "HTTPMethods",
    "HeaderMatch",
    "IListener",
    "IService",
    "IServiceNetwork",
    "ITarget",
    "ITargetGroup",
    "ImportedServiceNetworkProps",
    "Listener",
    "ListenerProps",
    "LoggingDestination",
    "MatchOperator",
    "PathMatch",
    "PathMatchType",
    "Protocol",
    "RuleAccessMode",
    "RuleProp",
    "Service",
    "ServiceAssociation",
    "ServiceAssociationProps",
    "ServiceNetwork",
    "ServiceNetworkAccessMode",
    "ServiceNetworkAssociation",
    "ServiceNetworkAssociationProps",
    "ServiceNetworkProps",
    "ServiceProps",
    "ShareServiceNetworkProps",
    "ShareServiceProps",
    "TargetGroup",
    "TargetGroupProps",
    "WeightedTargetGroup",
]

publication.publish()

def _typecheckingstub__02b4015f66cc1e6e4d2908b5f92fc0e0fc30e4335031b75bdf77f8d32a45f21c(
    *,
    service: IService,
    service_network_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb99c82f399463ba79b71714c4f2c6a7b042bbd802770d02abaa8442a99c657b(
    *,
    destination: LoggingDestination,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faaf88da9f034b12708826cb10f821f26e98818781b4c562804d0c0c19b50c9c(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7671d0d9b6ef8d7b1dc2a0f4ccd98692dae7426b69523eafb3a014fa224f95d8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    service_network_id: builtins.str,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24b97a18efc24b7b85203f1578630c8bd0654097deb6dd8cc8e13f19603b7d2(
    *,
    service_network_id: builtins.str,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44af5882c9ea40e745089d97a10308472b69df8c9603ac29739a7b00f9434a63(
    *,
    fixed_response: typing.Optional[FixedResponse] = None,
    forward: typing.Optional[typing.Union[WeightedTargetGroup, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5aba9d5436c7bf0a13346c8c563cdde4ffa85f0f4dd100dfcbce7af3416d93f(
    *,
    header_matches: typing.Optional[typing.Sequence[typing.Union[HeaderMatch, typing.Dict[builtins.str, typing.Any]]]] = None,
    method: typing.Optional[HTTPMethods] = None,
    path_matches: typing.Optional[typing.Union[PathMatch, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630e305fb29c08a9d5d7c4d0ce4c846132292e1ad11b996b501d021ab122b09e(
    *,
    headername: builtins.str,
    match_operator: MatchOperator,
    match_value: builtins.str,
    case_sensitive: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3552df34a58f59ebe96fa8e8e9e946506c316b05c8490a91a9da9cbbed02720(
    value: _aws_cdk_aws_iam_ceddda9d.PolicyDocument,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3d733e9e1b87f3780e70fc8a1fadb074e593edf1e7819442d23b72bbb3aa6c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf546ba69e00ab089cb3faab5297e3c1d9f7654a6e07e60153aeede16ed2374(
    value: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d440d965bd15e56d27443d1bd9693d943d9e84dd228cdd9b5d20178b4d81a8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9154e180f7868fa32c6e112ffba8f5229db13a067a022373656550b77bb9fba2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649ee528054b2fde60cb4a4bb489a362d64612813194a7c4edafe1ed296890a2(
    service_network: IServiceNetwork,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7ec4aa4b499c4d5c90362046200cac1b690729c2ad2e0b7758945fb4eb4212(
    *,
    service_network_id: typing.Optional[builtins.str] = None,
    service_network_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb71f2f6428ab04fb943120047ec2c8af2d396af0ee76e1dafa108ef1373641(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    service: IService,
    default_action: typing.Optional[typing.Union[DefaultListenerAction, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[Protocol] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[RuleProp, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1ace053d59e3cbdcee35db1e63d58cc647015852487fa802da3eacbdb559e2(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f71fa25236c863d0edf9b99555f53d628bab19f530cf943f220f94fce91ea1(
    value: IService,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f43a6d10644426ab80eab11e6e7983c88a302ece410564a74eedba73d29a7ee(
    *,
    service: IService,
    default_action: typing.Optional[typing.Union[DefaultListenerAction, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[Protocol] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[RuleProp, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65fbe8af34569ae5b49f723939433775f2758f47c325f0b2023c22d9c7838fa8(
    log_group: _aws_cdk_aws_logs_ceddda9d.ILogGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a734623fe81363d29a1c3070244ecfa8e49152584668c9f7754e5a6e5a153748(
    stream: _aws_cdk_aws_kinesis_ceddda9d.IStream,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b5df1dc69409b6b0939b62d8b509bf75454dae7b761dee61b9fdc3aaab12b1(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702732e343b1a7a05bed7ce0fdc2ad13ca491ad2a880b7f97f1fbd850e11b32e(
    *,
    path: builtins.str,
    case_sensitive: typing.Optional[builtins.bool] = None,
    path_match_type: typing.Optional[PathMatchType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef52623acd059fdd95b01760a388f3671e3961d089c325fe8bede2fb84ad61c(
    *,
    action: typing.Union[FixedResponse, typing.Sequence[typing.Union[WeightedTargetGroup, typing.Dict[builtins.str, typing.Any]]]],
    http_match: typing.Union[HTTPMatch, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    access_mode: typing.Optional[RuleAccessMode] = None,
    allowed_principal_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_principals: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IPrincipal]] = None,
    priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a33850b7c5e8418f477213ab06d5800d7a1845d919e83a51f66eeba45ca78d20(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    auth_type: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate] = None,
    custom_domain: typing.Optional[builtins.str] = None,
    hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
    listeners: typing.Optional[typing.Sequence[IListener]] = None,
    name: typing.Optional[builtins.str] = None,
    service_network: typing.Optional[IServiceNetwork] = None,
    shares: typing.Optional[typing.Sequence[typing.Union[ShareServiceProps, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536d2d64bd917ab406b346c442d8676cef65b1df3cd0ea48290ac1f0320ab3d3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    service_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa284bcf9140f3788b7e5882133f718a7901612c937e10c2d5139b8caa1ac834(
    statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37fae3757cb060322eb4b5581dd9f1b58b5450034337dd448faaf5c4a423033(
    service_network: IServiceNetwork,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c4cee15734969107c7bc804a65dcb9a92b7a78bbe3690cb36405f531b98bdb(
    principals: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IPrincipal],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d36f2c70158faece2d30ac5a65d0145e34a90b550b76c3c67827c388fdda0a(
    value: _aws_cdk_aws_iam_ceddda9d.PolicyDocument,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__260aa4ceb0330c49c77c173a149e81fc9e9aeeba877134d2f44164c65e1c271d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44371e27a83554ed17ad32d0b903051edec2a60d31e2151e2bac2b2a69e32612(
    value: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa902b9cb442b40c6d2858638e478d4eeee07a846a3473c67f1927a5dcc4417(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f84ca3ed6facb06b8860be0bd622971c6437a32302316501d9f2ec0869c4aa(
    value: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea6ff9c2840e668bc6ba0ae4c2d75662f92448caa9b12b819c73607abd8dd77(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c92784ccec40fd5bbc425457ea7b2d583f16d81909b714b1db1487c3a33b4a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    service: IService,
    service_network_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e0f0596a05248b29caf1321d3ac1ea461640e88139abb0708fc6fa38216679(
    *,
    service: IService,
    service_network_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de151a2ad4bc98964269dae761de01f5e454e7dc434e2e1b4a0fb7f43ea5410a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    accessmode: typing.Optional[ServiceNetworkAccessMode] = None,
    auth_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    auth_type: typing.Optional[AuthType] = None,
    logging_destinations: typing.Optional[typing.Sequence[LoggingDestination]] = None,
    name: typing.Optional[builtins.str] = None,
    services: typing.Optional[typing.Sequence[IService]] = None,
    vpcs: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.IVpc]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9243fcd9f7589f40cf588ea260858b4b3eec8f1368ceadc62e433f7715c522cc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    service_network_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ec1a40d648e8ddf40761db7d89c9fc1a1cfe16a9b8c657725d7bcffcd38fd0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    service_network_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e786816186e43e34cc91b53da5c90a18cf73c201e5c0dd2c2d5970a23526f9(
    statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e980f16275c01a927459b29042c01b665e25c653f12f3ddb4cb88f9a2d13901(
    value: _aws_cdk_aws_iam_ceddda9d.PolicyDocument,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283532f01625f252eaef51db2c0cfa7ae01d90dab5f5f659bc84dcf8aea1eac6(
    value: typing.Optional[AuthType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e45e0945bfa3da60848fec97f96879fb705e79c77723361651f24f55d8804e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    service_id: builtins.str,
    service_network: IServiceNetwork,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bafe9c29c25ac5fb0f856db1bbf30cab5fac093a313d72c236eded05925d762(
    *,
    service_id: builtins.str,
    service_network: IServiceNetwork,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c5b474503b3d82c41ab24892bfd41523b749529c0d3b3060a5058d4a0226d6(
    *,
    accessmode: typing.Optional[ServiceNetworkAccessMode] = None,
    auth_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    auth_type: typing.Optional[AuthType] = None,
    logging_destinations: typing.Optional[typing.Sequence[LoggingDestination]] = None,
    name: typing.Optional[builtins.str] = None,
    services: typing.Optional[typing.Sequence[IService]] = None,
    vpcs: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.IVpc]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46d70cae814eabdfefba7001e4d74ae5941b4dfac46989c922623f9c2c6e54c(
    *,
    auth_type: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.Certificate] = None,
    custom_domain: typing.Optional[builtins.str] = None,
    hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
    listeners: typing.Optional[typing.Sequence[IListener]] = None,
    name: typing.Optional[builtins.str] = None,
    service_network: typing.Optional[IServiceNetwork] = None,
    shares: typing.Optional[typing.Sequence[typing.Union[ShareServiceProps, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fedf0cf4f5d543e3ab39b8f8e7dac5b1f8a6f8c1ed0923cb1d1264ea676fccf(
    *,
    accounts: typing.Sequence[builtins.str],
    name: builtins.str,
    access_mode: typing.Optional[ServiceNetworkAccessMode] = None,
    allow_external_principals: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    disable_discovery: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e29e3fa88298a4e4928c04749904336e3eacf2b5a4bfee01853dd10bfda192(
    *,
    name: builtins.str,
    accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_external_principals: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a176a630861c516852778a8ed1f5049196b91a41c7e45a8e1acd70bf582bcaf8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    target: ITarget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47f30a4764ceb906bba13a9afa50eab0d3d4c412fc4de8631056c26d8ef3203(
    *,
    name: builtins.str,
    target: ITarget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09cf15092c702ea025dfe6852c3cb360bbc14e79272beccfa8a13e66a0c48c4(
    *,
    target_group: TargetGroup,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
