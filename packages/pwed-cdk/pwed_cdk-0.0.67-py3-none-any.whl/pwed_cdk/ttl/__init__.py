import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


class Ttl(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="pwed-cdk.ttl.Ttl",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ttl: _aws_cdk_ceddda9d.Duration,
        poll_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ttl: 
        :param poll_interval: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d02d058f14f98bb829ea97bcc63057f9c95eba1474a8c5c3338d2b48fdcd96fa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TtlProps(ttl=ttl, poll_interval=poll_interval)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="pwed-cdk.ttl.TtlProps",
    jsii_struct_bases=[],
    name_mapping={"ttl": "ttl", "poll_interval": "pollInterval"},
)
class TtlProps:
    def __init__(
        self,
        *,
        ttl: _aws_cdk_ceddda9d.Duration,
        poll_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param ttl: 
        :param poll_interval: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0535dba4a4808b3b82dfc120bc7e6325a559fa07d17bd62e5ac010a5dc5ab03)
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            check_type(argname="argument poll_interval", value=poll_interval, expected_type=type_hints["poll_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ttl": ttl,
        }
        if poll_interval is not None:
            self._values["poll_interval"] = poll_interval

    @builtins.property
    def ttl(self) -> _aws_cdk_ceddda9d.Duration:
        '''
        :stability: experimental
        '''
        result = self._values.get("ttl")
        assert result is not None, "Required property 'ttl' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Duration, result)

    @builtins.property
    def poll_interval(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''
        :stability: experimental
        '''
        result = self._values.get("poll_interval")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TtlProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Ttl",
    "TtlProps",
]

publication.publish()

def _typecheckingstub__d02d058f14f98bb829ea97bcc63057f9c95eba1474a8c5c3338d2b48fdcd96fa(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ttl: _aws_cdk_ceddda9d.Duration,
    poll_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0535dba4a4808b3b82dfc120bc7e6325a559fa07d17bd62e5ac010a5dc5ab03(
    *,
    ttl: _aws_cdk_ceddda9d.Duration,
    poll_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass
