'''
# static-site

Easily deploy a static site backed by s3 and CloudFront

## Usage

```python
import { pwed_static_site } from 'pwed-cdk';
import * as path from 'path';

const website = new pwed_static_site.StaticSite(this, 'PwedDotMe', {
  domain: 'pwed.me',                     // Required
  path: path.join(__dirname, 'static'),  // Required - path to static files
  alternativeDomains: ['blog.pwed.me'],  // Optional - Other names
  hostedZone: zone,                      // Optional - will lookup using the domain if not provided
  enablePrettyPaths: true,               // Optional - will look for index.html in urls ending with a '/' or with no file type
});
```
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

from .._jsii import *

import aws_cdk.aws_cloudfront as _aws_cdk_aws_cloudfront_ceddda9d
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_ceddda9d
import constructs as _constructs_77d1e7e8


class StaticSite(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="pwed-cdk.static_site.StaticSite",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domain: builtins.str,
        path: builtins.str,
        alternative_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        alternative_hosted_zones: typing.Optional[typing.Sequence[_aws_cdk_aws_route53_ceddda9d.IHostedZone]] = None,
        enable_pretty_paths: typing.Optional[builtins.bool] = None,
        hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domain: 
        :param path: 
        :param alternative_domains: 
        :param alternative_hosted_zones: 
        :param enable_pretty_paths: 
        :param hosted_zone: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed8466d7da06664a56f05f55b92c95bcfddb61b022f83d61345bc142a5b3657)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StaticSiteProps(
            domain=domain,
            path=path,
            alternative_domains=alternative_domains,
            alternative_hosted_zones=alternative_hosted_zones,
            enable_pretty_paths=enable_pretty_paths,
            hosted_zone=hosted_zone,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> _aws_cdk_aws_cloudfront_ceddda9d.IDistribution:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.IDistribution, jsii.get(self, "distribution"))

    @distribution.setter
    def distribution(
        self,
        value: _aws_cdk_aws_cloudfront_ceddda9d.IDistribution,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b149df278d5548e73ee6c057b1fc55c7aa4543216fcdd0b41398b0b5f8096b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distribution", value)


@jsii.data_type(
    jsii_type="pwed-cdk.static_site.StaticSiteProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain": "domain",
        "path": "path",
        "alternative_domains": "alternativeDomains",
        "alternative_hosted_zones": "alternativeHostedZones",
        "enable_pretty_paths": "enablePrettyPaths",
        "hosted_zone": "hostedZone",
    },
)
class StaticSiteProps:
    def __init__(
        self,
        *,
        domain: builtins.str,
        path: builtins.str,
        alternative_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        alternative_hosted_zones: typing.Optional[typing.Sequence[_aws_cdk_aws_route53_ceddda9d.IHostedZone]] = None,
        enable_pretty_paths: typing.Optional[builtins.bool] = None,
        hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
    ) -> None:
        '''
        :param domain: 
        :param path: 
        :param alternative_domains: 
        :param alternative_hosted_zones: 
        :param enable_pretty_paths: 
        :param hosted_zone: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3ee73abba2e493435356c49bec2ee8012f02cae7c49dcea794a5c6bc9c404e)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument alternative_domains", value=alternative_domains, expected_type=type_hints["alternative_domains"])
            check_type(argname="argument alternative_hosted_zones", value=alternative_hosted_zones, expected_type=type_hints["alternative_hosted_zones"])
            check_type(argname="argument enable_pretty_paths", value=enable_pretty_paths, expected_type=type_hints["enable_pretty_paths"])
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
            "path": path,
        }
        if alternative_domains is not None:
            self._values["alternative_domains"] = alternative_domains
        if alternative_hosted_zones is not None:
            self._values["alternative_hosted_zones"] = alternative_hosted_zones
        if enable_pretty_paths is not None:
            self._values["enable_pretty_paths"] = enable_pretty_paths
        if hosted_zone is not None:
            self._values["hosted_zone"] = hosted_zone

    @builtins.property
    def domain(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alternative_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("alternative_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def alternative_hosted_zones(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_route53_ceddda9d.IHostedZone]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("alternative_hosted_zones")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_route53_ceddda9d.IHostedZone]], result)

    @builtins.property
    def enable_pretty_paths(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("enable_pretty_paths")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def hosted_zone(self) -> typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone]:
        '''
        :stability: experimental
        '''
        result = self._values.get("hosted_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StaticSiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "StaticSite",
    "StaticSiteProps",
]

publication.publish()

def _typecheckingstub__7ed8466d7da06664a56f05f55b92c95bcfddb61b022f83d61345bc142a5b3657(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domain: builtins.str,
    path: builtins.str,
    alternative_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    alternative_hosted_zones: typing.Optional[typing.Sequence[_aws_cdk_aws_route53_ceddda9d.IHostedZone]] = None,
    enable_pretty_paths: typing.Optional[builtins.bool] = None,
    hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b149df278d5548e73ee6c057b1fc55c7aa4543216fcdd0b41398b0b5f8096b(
    value: _aws_cdk_aws_cloudfront_ceddda9d.IDistribution,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3ee73abba2e493435356c49bec2ee8012f02cae7c49dcea794a5c6bc9c404e(
    *,
    domain: builtins.str,
    path: builtins.str,
    alternative_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    alternative_hosted_zones: typing.Optional[typing.Sequence[_aws_cdk_aws_route53_ceddda9d.IHostedZone]] = None,
    enable_pretty_paths: typing.Optional[builtins.bool] = None,
    hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
) -> None:
    """Type checking stubs"""
    pass
