'''
# bastion

A set of constructs to create and access bastion hosts using SSO or IAM. By using session manager for shell access and GUI Connect for Windows RDP access, no ports need to be exposed to the internet and all access can be managed and audited through AWS services.

## Todo

* Allow choco installs
* fix aws cli not installing with winget
* Allow picking and choosing of services in the access policy
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_sso as _aws_cdk_aws_sso_ceddda9d
import constructs as _constructs_77d1e7e8


class BastionAccessPolicy(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="pwed-cdk.bastion.BastionAccessPolicy",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param security_tag: Tag used by all bastion resources for managing access to resources. Default: - {Key: "security:bastion", value: "true"}

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3438482c03f10f8df56bea614ddaf54b0674ca6d8e1a6536e5385a6571400f20)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BastionAccessPolicyProps(security_tag=security_tag)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> _aws_cdk_aws_iam_ceddda9d.PolicyDocument:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.PolicyDocument, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: _aws_cdk_aws_iam_ceddda9d.PolicyDocument) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd3b52afb9549a419244123e57e1aa3709344327bdaebb1da485abbbf61422b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)


class BastionPermissionSet(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="pwed-cdk.bastion.BastionPermissionSet",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_arn: builtins.str,
        name: builtins.str,
        customer_managed_policy_references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[typing.Union[_aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.CustomerManagedPolicyReferenceProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_ceddda9d.IResolvable]]]] = None,
        description: typing.Optional[builtins.str] = None,
        inline_policy: typing.Any = None,
        managed_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        permissions_boundary: typing.Optional[typing.Union[typing.Union[_aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.PermissionsBoundaryProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_ceddda9d.IResolvable]] = None,
        relay_state_type: typing.Optional[builtins.str] = None,
        session_duration: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param instance_arn: The ARN of the SSO instance under which the operation will be executed. For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param name: The name of the permission set.
        :param customer_managed_policy_references: ``AWS::SSO::PermissionSet.CustomerManagedPolicyReferences``.
        :param description: The description of the ``PermissionSet`` .
        :param inline_policy: The IAM inline policy that is attached to the permission set.
        :param managed_policies: A structure that stores the details of the IAM managed policy.
        :param permissions_boundary: ``AWS::SSO::PermissionSet.PermissionsBoundary``.
        :param relay_state_type: Used to redirect users within the application during the federation authentication process.
        :param session_duration: The length of time that the application user sessions are valid for in the ISO-8601 standard.
        :param tags: The tags to attach to the new ``PermissionSet`` .
        :param security_tag: Tag used by all bastion resources for managing access to resources. Default: - {Key: "security:bastion", value: "true"}

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acee9c91646023001be186b214af056d75c326a1c5668900898ba369fc16c3da)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BastionPermissionSetProps(
            instance_arn=instance_arn,
            name=name,
            customer_managed_policy_references=customer_managed_policy_references,
            description=description,
            inline_policy=inline_policy,
            managed_policies=managed_policies,
            permissions_boundary=permissions_boundary,
            relay_state_type=relay_state_type,
            session_duration=session_duration,
            tags=tags,
            security_tag=security_tag,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="assign")
    def assign(
        self,
        account_id: builtins.str,
        principal_id: builtins.str,
        principal_type: builtins.str,
    ) -> None:
        '''
        :param account_id: -
        :param principal_id: -
        :param principal_type: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f175092b59f9395f54dfd79787bac20b2b506103f459fed7490e50841e8e5360)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
            check_type(argname="argument principal_type", value=principal_type, expected_type=type_hints["principal_type"])
        return typing.cast(None, jsii.invoke(self, "assign", [account_id, principal_id, principal_type]))

    @builtins.property
    @jsii.member(jsii_name="securityTag")
    def security_tag(self) -> _aws_cdk_ceddda9d.Tag:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_ceddda9d.Tag, jsii.get(self, "securityTag"))

    @security_tag.setter
    def security_tag(self, value: _aws_cdk_ceddda9d.Tag) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e0137d528e0877d7c146b17de6752dd1c189fa22bd453c1b63e0df1fbbf680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityTag", value)


@jsii.implements(_aws_cdk_aws_ec2_ceddda9d.IInstance)
class LinuxBastion(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="pwed-cdk.bastion.LinuxBastion",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        package_manager: typing.Optional["LinuxPackageManager"] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
        block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
        security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param package_manager: (experimental) Package manager used for installing packages. Default: - dnf
        :param packages: (experimental) List of packages to be installed as part of the userdata using winget. Default: - []
        :param vpc: VPC to launch the instance in.
        :param vpc_subnets: Where to place the instance within the VPC. Default: - Private subnets.
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param instance_name: The name of the instance. Default: - CDK generated name
        :param instance_type: Type of instance to launch. Default: - t3a.large
        :param machine_image: AMI to launch. Default: - latest windows server 2022 full base
        :param private_ip_address: Defines a private IP address to associate with an instance. Private IP should be available within the VPC that the instance is build within. Default: - no association
        :param role: An IAM role to associate with the instance profile assigned to this Auto Scaling Group. The role must be assumable by the service principal ``ec2.amazonaws.com``: Default: - A role will automatically be created, it can be accessed via the ``role`` property
        :param security_group: Security Group to assign to this instance. Default: - create new security group
        :param user_data: Specific UserData to use. The UserData may still be mutated after creation. Default: - A UserData object appropriate for the MachineImage's Operating System is created.
        :param security_tag: Tag used by all bastion resources for managing access to resources. Default: - {Key: "security:bastion", value: "true"}

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d2fe143301dd3d265f5f1750dd6ab247959291aa58d9bce05f8c56b4f344c8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LinuxBastionProps(
            package_manager=package_manager,
            packages=packages,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            block_devices=block_devices,
            instance_name=instance_name,
            instance_type=instance_type,
            machine_image=machine_image,
            private_ip_address=private_ip_address,
            role=role,
            security_group=security_group,
            user_data=user_data,
            security_tag=security_tag,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="instanceAvailabilityZone")
    def instance_availability_zone(self) -> builtins.str:
        '''(experimental) The availability zone the instance was launched in.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceAvailabilityZone"))

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        '''(experimental) The instance's ID.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @builtins.property
    @jsii.member(jsii_name="instancePrivateDnsName")
    def instance_private_dns_name(self) -> builtins.str:
        '''(experimental) Private DNS name for this instance.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instancePrivateDnsName"))

    @builtins.property
    @jsii.member(jsii_name="instancePrivateIp")
    def instance_private_ip(self) -> builtins.str:
        '''(experimental) Private IP for this instance.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instancePrivateIp"))

    @builtins.property
    @jsii.member(jsii_name="instancePublicDnsName")
    def instance_public_dns_name(self) -> builtins.str:
        '''(experimental) Publicly-routable DNS name for this instance.

        (May be an empty string if the instance does not have a public name).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instancePublicDnsName"))

    @builtins.property
    @jsii.member(jsii_name="instancePublicIp")
    def instance_public_ip(self) -> builtins.str:
        '''(experimental) Publicly-routable IP  address for this instance.

        (May be an empty string if the instance does not have a public IP).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instancePublicIp"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, jsii.get(self, "securityGroup"))


@jsii.enum(jsii_type="pwed-cdk.bastion.LinuxPackageManager")
class LinuxPackageManager(enum.Enum):
    '''
    :stability: experimental
    '''

    APT = "APT"
    '''
    :stability: experimental
    '''
    YUM = "YUM"
    '''
    :stability: experimental
    '''
    DNF = "DNF"
    '''
    :stability: experimental
    '''


class ScheduleShutdown(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="pwed-cdk.bastion.ScheduleShutdown",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        shutdown_schedule: typing.Optional[builtins.str] = None,
        timezone: typing.Optional[builtins.str] = None,
        security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param shutdown_schedule: 
        :param timezone: 
        :param security_tag: Tag used by all bastion resources for managing access to resources. Default: - {Key: "security:bastion", value: "true"}

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c20c5f3a4a96d24bc2a31eacda3939a11c2035b5e4fcf9380137489c17341945)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ScheduleShutdownProps(
            shutdown_schedule=shutdown_schedule,
            timezone=timezone,
            security_tag=security_tag,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="pwed-cdk.bastion.SecurityTagable",
    jsii_struct_bases=[],
    name_mapping={"security_tag": "securityTag"},
)
class SecurityTagable:
    def __init__(
        self,
        *,
        security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    ) -> None:
        '''
        :param security_tag: Tag used by all bastion resources for managing access to resources. Default: - {Key: "security:bastion", value: "true"}

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49c5eb5d2425a6ba047212fdbb212bb22b5ea4f715a07994187a46e224e783d0)
            check_type(argname="argument security_tag", value=security_tag, expected_type=type_hints["security_tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_tag is not None:
            self._values["security_tag"] = security_tag

    @builtins.property
    def security_tag(self) -> typing.Optional[_aws_cdk_ceddda9d.Tag]:
        '''Tag used by all bastion resources for managing access to resources.

        :default: - {Key: "security:bastion", value: "true"}
        '''
        result = self._values.get("security_tag")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Tag], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityTagable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_ec2_ceddda9d.IInstance)
class WindowsBastion(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="pwed-cdk.bastion.WindowsBastion",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        create_key_pair: typing.Optional[builtins.bool] = None,
        windows_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
        block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
        security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param create_key_pair: If a keypair should be created and saved into Secrets Manager. This can be used to get Administrator user access Default: - false
        :param windows_packages: (experimental) List of packages to be installed as part of the userdata using winget. Default: - no association
        :param vpc: VPC to launch the instance in.
        :param vpc_subnets: Where to place the instance within the VPC. Default: - Private subnets.
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param instance_name: The name of the instance. Default: - CDK generated name
        :param instance_type: Type of instance to launch. Default: - t3a.large
        :param machine_image: AMI to launch. Default: - latest windows server 2022 full base
        :param private_ip_address: Defines a private IP address to associate with an instance. Private IP should be available within the VPC that the instance is build within. Default: - no association
        :param role: An IAM role to associate with the instance profile assigned to this Auto Scaling Group. The role must be assumable by the service principal ``ec2.amazonaws.com``: Default: - A role will automatically be created, it can be accessed via the ``role`` property
        :param security_group: Security Group to assign to this instance. Default: - create new security group
        :param user_data: Specific UserData to use. The UserData may still be mutated after creation. Default: - A UserData object appropriate for the MachineImage's Operating System is created.
        :param security_tag: Tag used by all bastion resources for managing access to resources. Default: - {Key: "security:bastion", value: "true"}

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f233056224dad4198c6b3840156f81e4d4651903cf5991bd969b5058007b8de)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WindowsBastionProps(
            create_key_pair=create_key_pair,
            windows_packages=windows_packages,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            block_devices=block_devices,
            instance_name=instance_name,
            instance_type=instance_type,
            machine_image=machine_image,
            private_ip_address=private_ip_address,
            role=role,
            security_group=security_group,
            user_data=user_data,
            security_tag=security_tag,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="instanceAvailabilityZone")
    def instance_availability_zone(self) -> builtins.str:
        '''(experimental) The availability zone the instance was launched in.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceAvailabilityZone"))

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        '''(experimental) The instance's ID.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @builtins.property
    @jsii.member(jsii_name="instancePrivateDnsName")
    def instance_private_dns_name(self) -> builtins.str:
        '''(experimental) Private DNS name for this instance.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instancePrivateDnsName"))

    @builtins.property
    @jsii.member(jsii_name="instancePrivateIp")
    def instance_private_ip(self) -> builtins.str:
        '''(experimental) Private IP for this instance.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instancePrivateIp"))

    @builtins.property
    @jsii.member(jsii_name="instancePublicDnsName")
    def instance_public_dns_name(self) -> builtins.str:
        '''(experimental) Publicly-routable DNS name for this instance.

        (May be an empty string if the instance does not have a public name).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instancePublicDnsName"))

    @builtins.property
    @jsii.member(jsii_name="instancePublicIp")
    def instance_public_ip(self) -> builtins.str:
        '''(experimental) Publicly-routable IP  address for this instance.

        (May be an empty string if the instance does not have a public IP).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instancePublicIp"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, jsii.get(self, "securityGroup"))


@jsii.data_type(
    jsii_type="pwed-cdk.bastion.BastionAccessPolicyProps",
    jsii_struct_bases=[SecurityTagable],
    name_mapping={"security_tag": "securityTag"},
)
class BastionAccessPolicyProps(SecurityTagable):
    def __init__(
        self,
        *,
        security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    ) -> None:
        '''
        :param security_tag: Tag used by all bastion resources for managing access to resources. Default: - {Key: "security:bastion", value: "true"}

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd5f7707a4e08252b5f9ab03f5c0075fb9d021c347cdc3d91379038feae5f18)
            check_type(argname="argument security_tag", value=security_tag, expected_type=type_hints["security_tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_tag is not None:
            self._values["security_tag"] = security_tag

    @builtins.property
    def security_tag(self) -> typing.Optional[_aws_cdk_ceddda9d.Tag]:
        '''Tag used by all bastion resources for managing access to resources.

        :default: - {Key: "security:bastion", value: "true"}
        '''
        result = self._values.get("security_tag")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Tag], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BastionAccessPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="pwed-cdk.bastion.BastionInstanceProps",
    jsii_struct_bases=[SecurityTagable],
    name_mapping={
        "security_tag": "securityTag",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "block_devices": "blockDevices",
        "instance_name": "instanceName",
        "instance_type": "instanceType",
        "machine_image": "machineImage",
        "private_ip_address": "privateIpAddress",
        "role": "role",
        "security_group": "securityGroup",
        "user_data": "userData",
    },
)
class BastionInstanceProps(SecurityTagable):
    def __init__(
        self,
        *,
        security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
        block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    ) -> None:
        '''
        :param security_tag: Tag used by all bastion resources for managing access to resources. Default: - {Key: "security:bastion", value: "true"}
        :param vpc: VPC to launch the instance in.
        :param vpc_subnets: Where to place the instance within the VPC. Default: - Private subnets.
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param instance_name: The name of the instance. Default: - CDK generated name
        :param instance_type: Type of instance to launch. Default: - t3a.large
        :param machine_image: AMI to launch. Default: - latest windows server 2022 full base
        :param private_ip_address: Defines a private IP address to associate with an instance. Private IP should be available within the VPC that the instance is build within. Default: - no association
        :param role: An IAM role to associate with the instance profile assigned to this Auto Scaling Group. The role must be assumable by the service principal ``ec2.amazonaws.com``: Default: - A role will automatically be created, it can be accessed via the ``role`` property
        :param security_group: Security Group to assign to this instance. Default: - create new security group
        :param user_data: Specific UserData to use. The UserData may still be mutated after creation. Default: - A UserData object appropriate for the MachineImage's Operating System is created.

        :stability: experimental
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a68e0a887b77501e8f814e7a5042ac8edeaa36ce71a6cbdfa11a401db9291002)
            check_type(argname="argument security_tag", value=security_tag, expected_type=type_hints["security_tag"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument block_devices", value=block_devices, expected_type=type_hints["block_devices"])
            check_type(argname="argument instance_name", value=instance_name, expected_type=type_hints["instance_name"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument machine_image", value=machine_image, expected_type=type_hints["machine_image"])
            check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
            "vpc_subnets": vpc_subnets,
        }
        if security_tag is not None:
            self._values["security_tag"] = security_tag
        if block_devices is not None:
            self._values["block_devices"] = block_devices
        if instance_name is not None:
            self._values["instance_name"] = instance_name
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if machine_image is not None:
            self._values["machine_image"] = machine_image
        if private_ip_address is not None:
            self._values["private_ip_address"] = private_ip_address
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if user_data is not None:
            self._values["user_data"] = user_data

    @builtins.property
    def security_tag(self) -> typing.Optional[_aws_cdk_ceddda9d.Tag]:
        '''Tag used by all bastion resources for managing access to resources.

        :default: - {Key: "security:bastion", value: "true"}
        '''
        result = self._values.get("security_tag")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Tag], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''VPC to launch the instance in.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def vpc_subnets(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetSelection:
        '''Where to place the instance within the VPC.

        :default: - Private subnets.
        '''
        result = self._values.get("vpc_subnets")
        assert result is not None, "Required property 'vpc_subnets' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, result)

    @builtins.property
    def block_devices(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.BlockDevice]]:
        '''Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes.

        Each instance that is launched has an associated root device volume,
        either an Amazon EBS volume or an instance store volume.
        You can use block device mappings to specify additional EBS volumes or
        instance store volumes to attach to an instance when it is launched.

        :default: - Uses the block device mapping of the AMI

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html
        '''
        result = self._values.get("block_devices")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.BlockDevice]], result)

    @builtins.property
    def instance_name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance.

        :default: - CDK generated name
        '''
        result = self._values.get("instance_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''Type of instance to launch.

        :default: - t3a.large
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def machine_image(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage]:
        '''AMI to launch.

        :default: - latest windows server 2022 full base
        '''
        result = self._values.get("machine_image")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage], result)

    @builtins.property
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''Defines a private IP address to associate with an instance.

        Private IP should be available within the VPC that the instance is build within.

        :default: - no association
        '''
        result = self._values.get("private_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''An IAM role to associate with the instance profile assigned to this Auto Scaling Group.

        The role must be assumable by the service principal ``ec2.amazonaws.com``:

        :default: - A role will automatically be created, it can be accessed via the ``role`` property

        Example::

            const role = new iam.Role(this, 'MyRole', {
              assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com')
            });
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''Security Group to assign to this instance.

        :default: - create new security group
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def user_data(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData]:
        '''Specific UserData to use.

        The UserData may still be mutated after creation.

        :default:

        - A UserData object appropriate for the MachineImage's
        Operating System is created.
        '''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BastionInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="pwed-cdk.bastion.BastionPermissionSetProps",
    jsii_struct_bases=[
        _aws_cdk_aws_sso_ceddda9d.CfnPermissionSetProps, BastionAccessPolicyProps
    ],
    name_mapping={
        "instance_arn": "instanceArn",
        "name": "name",
        "customer_managed_policy_references": "customerManagedPolicyReferences",
        "description": "description",
        "inline_policy": "inlinePolicy",
        "managed_policies": "managedPolicies",
        "permissions_boundary": "permissionsBoundary",
        "relay_state_type": "relayStateType",
        "session_duration": "sessionDuration",
        "tags": "tags",
        "security_tag": "securityTag",
    },
)
class BastionPermissionSetProps(
    _aws_cdk_aws_sso_ceddda9d.CfnPermissionSetProps,
    BastionAccessPolicyProps,
):
    def __init__(
        self,
        *,
        instance_arn: builtins.str,
        name: builtins.str,
        customer_managed_policy_references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[typing.Union[_aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.CustomerManagedPolicyReferenceProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_ceddda9d.IResolvable]]]] = None,
        description: typing.Optional[builtins.str] = None,
        inline_policy: typing.Any = None,
        managed_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        permissions_boundary: typing.Optional[typing.Union[typing.Union[_aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.PermissionsBoundaryProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_ceddda9d.IResolvable]] = None,
        relay_state_type: typing.Optional[builtins.str] = None,
        session_duration: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    ) -> None:
        '''
        :param instance_arn: The ARN of the SSO instance under which the operation will be executed. For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param name: The name of the permission set.
        :param customer_managed_policy_references: ``AWS::SSO::PermissionSet.CustomerManagedPolicyReferences``.
        :param description: The description of the ``PermissionSet`` .
        :param inline_policy: The IAM inline policy that is attached to the permission set.
        :param managed_policies: A structure that stores the details of the IAM managed policy.
        :param permissions_boundary: ``AWS::SSO::PermissionSet.PermissionsBoundary``.
        :param relay_state_type: Used to redirect users within the application during the federation authentication process.
        :param session_duration: The length of time that the application user sessions are valid for in the ISO-8601 standard.
        :param tags: The tags to attach to the new ``PermissionSet`` .
        :param security_tag: Tag used by all bastion resources for managing access to resources. Default: - {Key: "security:bastion", value: "true"}

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f8df5f28512d4245b00b07930ac2c7864db6bbfcfdcdb0ad97e356a8ee11124)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument customer_managed_policy_references", value=customer_managed_policy_references, expected_type=type_hints["customer_managed_policy_references"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument inline_policy", value=inline_policy, expected_type=type_hints["inline_policy"])
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument relay_state_type", value=relay_state_type, expected_type=type_hints["relay_state_type"])
            check_type(argname="argument session_duration", value=session_duration, expected_type=type_hints["session_duration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument security_tag", value=security_tag, expected_type=type_hints["security_tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_arn": instance_arn,
            "name": name,
        }
        if customer_managed_policy_references is not None:
            self._values["customer_managed_policy_references"] = customer_managed_policy_references
        if description is not None:
            self._values["description"] = description
        if inline_policy is not None:
            self._values["inline_policy"] = inline_policy
        if managed_policies is not None:
            self._values["managed_policies"] = managed_policies
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if relay_state_type is not None:
            self._values["relay_state_type"] = relay_state_type
        if session_duration is not None:
            self._values["session_duration"] = session_duration
        if tags is not None:
            self._values["tags"] = tags
        if security_tag is not None:
            self._values["security_tag"] = security_tag

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The ARN of the SSO instance under which the operation will be executed.

        For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the permission set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def customer_managed_policy_references(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.CustomerManagedPolicyReferenceProperty, _aws_cdk_ceddda9d.IResolvable]]]]:
        '''``AWS::SSO::PermissionSet.CustomerManagedPolicyReferences``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-customermanagedpolicyreferences
        '''
        result = self._values.get("customer_managed_policy_references")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.CustomerManagedPolicyReferenceProperty, _aws_cdk_ceddda9d.IResolvable]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the ``PermissionSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inline_policy(self) -> typing.Any:
        '''The IAM inline policy that is attached to the permission set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-inlinepolicy
        '''
        result = self._values.get("inline_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def managed_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A structure that stores the details of the IAM managed policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-managedpolicies
        '''
        result = self._values.get("managed_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permissions_boundary(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.PermissionsBoundaryProperty, _aws_cdk_ceddda9d.IResolvable]]:
        '''``AWS::SSO::PermissionSet.PermissionsBoundary``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-permissionsboundary
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.PermissionsBoundaryProperty, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def relay_state_type(self) -> typing.Optional[builtins.str]:
        '''Used to redirect users within the application during the federation authentication process.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-relaystatetype
        '''
        result = self._values.get("relay_state_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_duration(self) -> typing.Optional[builtins.str]:
        '''The length of time that the application user sessions are valid for in the ISO-8601 standard.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-sessionduration
        '''
        result = self._values.get("session_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to attach to the new ``PermissionSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def security_tag(self) -> typing.Optional[_aws_cdk_ceddda9d.Tag]:
        '''Tag used by all bastion resources for managing access to resources.

        :default: - {Key: "security:bastion", value: "true"}
        '''
        result = self._values.get("security_tag")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Tag], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BastionPermissionSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="pwed-cdk.bastion.LinuxBastionProps",
    jsii_struct_bases=[BastionInstanceProps],
    name_mapping={
        "security_tag": "securityTag",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "block_devices": "blockDevices",
        "instance_name": "instanceName",
        "instance_type": "instanceType",
        "machine_image": "machineImage",
        "private_ip_address": "privateIpAddress",
        "role": "role",
        "security_group": "securityGroup",
        "user_data": "userData",
        "package_manager": "packageManager",
        "packages": "packages",
    },
)
class LinuxBastionProps(BastionInstanceProps):
    def __init__(
        self,
        *,
        security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
        block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
        package_manager: typing.Optional[LinuxPackageManager] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_tag: Tag used by all bastion resources for managing access to resources. Default: - {Key: "security:bastion", value: "true"}
        :param vpc: VPC to launch the instance in.
        :param vpc_subnets: Where to place the instance within the VPC. Default: - Private subnets.
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param instance_name: The name of the instance. Default: - CDK generated name
        :param instance_type: Type of instance to launch. Default: - t3a.large
        :param machine_image: AMI to launch. Default: - latest windows server 2022 full base
        :param private_ip_address: Defines a private IP address to associate with an instance. Private IP should be available within the VPC that the instance is build within. Default: - no association
        :param role: An IAM role to associate with the instance profile assigned to this Auto Scaling Group. The role must be assumable by the service principal ``ec2.amazonaws.com``: Default: - A role will automatically be created, it can be accessed via the ``role`` property
        :param security_group: Security Group to assign to this instance. Default: - create new security group
        :param user_data: Specific UserData to use. The UserData may still be mutated after creation. Default: - A UserData object appropriate for the MachineImage's Operating System is created.
        :param package_manager: (experimental) Package manager used for installing packages. Default: - dnf
        :param packages: (experimental) List of packages to be installed as part of the userdata using winget. Default: - []

        :stability: experimental
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb363a409be0a64d6a7ca2d28fc197b4a7666564292443b03c94ac6894b7adf3)
            check_type(argname="argument security_tag", value=security_tag, expected_type=type_hints["security_tag"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument block_devices", value=block_devices, expected_type=type_hints["block_devices"])
            check_type(argname="argument instance_name", value=instance_name, expected_type=type_hints["instance_name"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument machine_image", value=machine_image, expected_type=type_hints["machine_image"])
            check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
            check_type(argname="argument package_manager", value=package_manager, expected_type=type_hints["package_manager"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
            "vpc_subnets": vpc_subnets,
        }
        if security_tag is not None:
            self._values["security_tag"] = security_tag
        if block_devices is not None:
            self._values["block_devices"] = block_devices
        if instance_name is not None:
            self._values["instance_name"] = instance_name
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if machine_image is not None:
            self._values["machine_image"] = machine_image
        if private_ip_address is not None:
            self._values["private_ip_address"] = private_ip_address
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if user_data is not None:
            self._values["user_data"] = user_data
        if package_manager is not None:
            self._values["package_manager"] = package_manager
        if packages is not None:
            self._values["packages"] = packages

    @builtins.property
    def security_tag(self) -> typing.Optional[_aws_cdk_ceddda9d.Tag]:
        '''Tag used by all bastion resources for managing access to resources.

        :default: - {Key: "security:bastion", value: "true"}
        '''
        result = self._values.get("security_tag")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Tag], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''VPC to launch the instance in.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def vpc_subnets(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetSelection:
        '''Where to place the instance within the VPC.

        :default: - Private subnets.
        '''
        result = self._values.get("vpc_subnets")
        assert result is not None, "Required property 'vpc_subnets' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, result)

    @builtins.property
    def block_devices(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.BlockDevice]]:
        '''Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes.

        Each instance that is launched has an associated root device volume,
        either an Amazon EBS volume or an instance store volume.
        You can use block device mappings to specify additional EBS volumes or
        instance store volumes to attach to an instance when it is launched.

        :default: - Uses the block device mapping of the AMI

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html
        '''
        result = self._values.get("block_devices")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.BlockDevice]], result)

    @builtins.property
    def instance_name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance.

        :default: - CDK generated name
        '''
        result = self._values.get("instance_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''Type of instance to launch.

        :default: - t3a.large
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def machine_image(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage]:
        '''AMI to launch.

        :default: - latest windows server 2022 full base
        '''
        result = self._values.get("machine_image")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage], result)

    @builtins.property
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''Defines a private IP address to associate with an instance.

        Private IP should be available within the VPC that the instance is build within.

        :default: - no association
        '''
        result = self._values.get("private_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''An IAM role to associate with the instance profile assigned to this Auto Scaling Group.

        The role must be assumable by the service principal ``ec2.amazonaws.com``:

        :default: - A role will automatically be created, it can be accessed via the ``role`` property

        Example::

            const role = new iam.Role(this, 'MyRole', {
              assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com')
            });
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''Security Group to assign to this instance.

        :default: - create new security group
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def user_data(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData]:
        '''Specific UserData to use.

        The UserData may still be mutated after creation.

        :default:

        - A UserData object appropriate for the MachineImage's
        Operating System is created.
        '''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData], result)

    @builtins.property
    def package_manager(self) -> typing.Optional[LinuxPackageManager]:
        '''(experimental) Package manager used for installing packages.

        :default: - dnf

        :stability: experimental
        '''
        result = self._values.get("package_manager")
        return typing.cast(typing.Optional[LinuxPackageManager], result)

    @builtins.property
    def packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of packages to be installed as part of the userdata using winget.

        :default: - []

        :stability: experimental
        '''
        result = self._values.get("packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxBastionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="pwed-cdk.bastion.ScheduleShutdownProps",
    jsii_struct_bases=[SecurityTagable],
    name_mapping={
        "security_tag": "securityTag",
        "shutdown_schedule": "shutdownSchedule",
        "timezone": "timezone",
    },
)
class ScheduleShutdownProps(SecurityTagable):
    def __init__(
        self,
        *,
        security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
        shutdown_schedule: typing.Optional[builtins.str] = None,
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param security_tag: Tag used by all bastion resources for managing access to resources. Default: - {Key: "security:bastion", value: "true"}
        :param shutdown_schedule: 
        :param timezone: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2250f6eba1c2f7b5e4c4442234b20fefee08efc82b11f3d707dbaea416fe3634)
            check_type(argname="argument security_tag", value=security_tag, expected_type=type_hints["security_tag"])
            check_type(argname="argument shutdown_schedule", value=shutdown_schedule, expected_type=type_hints["shutdown_schedule"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_tag is not None:
            self._values["security_tag"] = security_tag
        if shutdown_schedule is not None:
            self._values["shutdown_schedule"] = shutdown_schedule
        if timezone is not None:
            self._values["timezone"] = timezone

    @builtins.property
    def security_tag(self) -> typing.Optional[_aws_cdk_ceddda9d.Tag]:
        '''Tag used by all bastion resources for managing access to resources.

        :default: - {Key: "security:bastion", value: "true"}
        '''
        result = self._values.get("security_tag")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Tag], result)

    @builtins.property
    def shutdown_schedule(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("shutdown_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleShutdownProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="pwed-cdk.bastion.WindowsBastionProps",
    jsii_struct_bases=[BastionInstanceProps],
    name_mapping={
        "security_tag": "securityTag",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "block_devices": "blockDevices",
        "instance_name": "instanceName",
        "instance_type": "instanceType",
        "machine_image": "machineImage",
        "private_ip_address": "privateIpAddress",
        "role": "role",
        "security_group": "securityGroup",
        "user_data": "userData",
        "create_key_pair": "createKeyPair",
        "windows_packages": "windowsPackages",
    },
)
class WindowsBastionProps(BastionInstanceProps):
    def __init__(
        self,
        *,
        security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
        block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
        create_key_pair: typing.Optional[builtins.bool] = None,
        windows_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_tag: Tag used by all bastion resources for managing access to resources. Default: - {Key: "security:bastion", value: "true"}
        :param vpc: VPC to launch the instance in.
        :param vpc_subnets: Where to place the instance within the VPC. Default: - Private subnets.
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param instance_name: The name of the instance. Default: - CDK generated name
        :param instance_type: Type of instance to launch. Default: - t3a.large
        :param machine_image: AMI to launch. Default: - latest windows server 2022 full base
        :param private_ip_address: Defines a private IP address to associate with an instance. Private IP should be available within the VPC that the instance is build within. Default: - no association
        :param role: An IAM role to associate with the instance profile assigned to this Auto Scaling Group. The role must be assumable by the service principal ``ec2.amazonaws.com``: Default: - A role will automatically be created, it can be accessed via the ``role`` property
        :param security_group: Security Group to assign to this instance. Default: - create new security group
        :param user_data: Specific UserData to use. The UserData may still be mutated after creation. Default: - A UserData object appropriate for the MachineImage's Operating System is created.
        :param create_key_pair: If a keypair should be created and saved into Secrets Manager. This can be used to get Administrator user access Default: - false
        :param windows_packages: (experimental) List of packages to be installed as part of the userdata using winget. Default: - no association

        :stability: experimental
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d31883eb5756a6741d041ca9007f0375ef0c0ac7f012ef1da368dbb92b236957)
            check_type(argname="argument security_tag", value=security_tag, expected_type=type_hints["security_tag"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument block_devices", value=block_devices, expected_type=type_hints["block_devices"])
            check_type(argname="argument instance_name", value=instance_name, expected_type=type_hints["instance_name"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument machine_image", value=machine_image, expected_type=type_hints["machine_image"])
            check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
            check_type(argname="argument create_key_pair", value=create_key_pair, expected_type=type_hints["create_key_pair"])
            check_type(argname="argument windows_packages", value=windows_packages, expected_type=type_hints["windows_packages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
            "vpc_subnets": vpc_subnets,
        }
        if security_tag is not None:
            self._values["security_tag"] = security_tag
        if block_devices is not None:
            self._values["block_devices"] = block_devices
        if instance_name is not None:
            self._values["instance_name"] = instance_name
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if machine_image is not None:
            self._values["machine_image"] = machine_image
        if private_ip_address is not None:
            self._values["private_ip_address"] = private_ip_address
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if user_data is not None:
            self._values["user_data"] = user_data
        if create_key_pair is not None:
            self._values["create_key_pair"] = create_key_pair
        if windows_packages is not None:
            self._values["windows_packages"] = windows_packages

    @builtins.property
    def security_tag(self) -> typing.Optional[_aws_cdk_ceddda9d.Tag]:
        '''Tag used by all bastion resources for managing access to resources.

        :default: - {Key: "security:bastion", value: "true"}
        '''
        result = self._values.get("security_tag")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Tag], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''VPC to launch the instance in.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def vpc_subnets(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetSelection:
        '''Where to place the instance within the VPC.

        :default: - Private subnets.
        '''
        result = self._values.get("vpc_subnets")
        assert result is not None, "Required property 'vpc_subnets' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, result)

    @builtins.property
    def block_devices(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.BlockDevice]]:
        '''Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes.

        Each instance that is launched has an associated root device volume,
        either an Amazon EBS volume or an instance store volume.
        You can use block device mappings to specify additional EBS volumes or
        instance store volumes to attach to an instance when it is launched.

        :default: - Uses the block device mapping of the AMI

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html
        '''
        result = self._values.get("block_devices")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.BlockDevice]], result)

    @builtins.property
    def instance_name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance.

        :default: - CDK generated name
        '''
        result = self._values.get("instance_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''Type of instance to launch.

        :default: - t3a.large
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def machine_image(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage]:
        '''AMI to launch.

        :default: - latest windows server 2022 full base
        '''
        result = self._values.get("machine_image")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage], result)

    @builtins.property
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''Defines a private IP address to associate with an instance.

        Private IP should be available within the VPC that the instance is build within.

        :default: - no association
        '''
        result = self._values.get("private_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''An IAM role to associate with the instance profile assigned to this Auto Scaling Group.

        The role must be assumable by the service principal ``ec2.amazonaws.com``:

        :default: - A role will automatically be created, it can be accessed via the ``role`` property

        Example::

            const role = new iam.Role(this, 'MyRole', {
              assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com')
            });
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''Security Group to assign to this instance.

        :default: - create new security group
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def user_data(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData]:
        '''Specific UserData to use.

        The UserData may still be mutated after creation.

        :default:

        - A UserData object appropriate for the MachineImage's
        Operating System is created.
        '''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData], result)

    @builtins.property
    def create_key_pair(self) -> typing.Optional[builtins.bool]:
        '''If a keypair should be created and saved into Secrets Manager.

        This can be used to get Administrator user access

        :default: - false
        '''
        result = self._values.get("create_key_pair")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def windows_packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of packages to be installed as part of the userdata using winget.

        :default: - no association

        :stability: experimental
        '''
        result = self._values.get("windows_packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsBastionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BastionAccessPolicy",
    "BastionAccessPolicyProps",
    "BastionInstanceProps",
    "BastionPermissionSet",
    "BastionPermissionSetProps",
    "LinuxBastion",
    "LinuxBastionProps",
    "LinuxPackageManager",
    "ScheduleShutdown",
    "ScheduleShutdownProps",
    "SecurityTagable",
    "WindowsBastion",
    "WindowsBastionProps",
]

publication.publish()

def _typecheckingstub__3438482c03f10f8df56bea614ddaf54b0674ca6d8e1a6536e5385a6571400f20(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd3b52afb9549a419244123e57e1aa3709344327bdaebb1da485abbbf61422b(
    value: _aws_cdk_aws_iam_ceddda9d.PolicyDocument,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acee9c91646023001be186b214af056d75c326a1c5668900898ba369fc16c3da(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    name: builtins.str,
    customer_managed_policy_references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[typing.Union[_aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.CustomerManagedPolicyReferenceProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_ceddda9d.IResolvable]]]] = None,
    description: typing.Optional[builtins.str] = None,
    inline_policy: typing.Any = None,
    managed_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    permissions_boundary: typing.Optional[typing.Union[typing.Union[_aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.PermissionsBoundaryProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_ceddda9d.IResolvable]] = None,
    relay_state_type: typing.Optional[builtins.str] = None,
    session_duration: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f175092b59f9395f54dfd79787bac20b2b506103f459fed7490e50841e8e5360(
    account_id: builtins.str,
    principal_id: builtins.str,
    principal_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e0137d528e0877d7c146b17de6752dd1c189fa22bd453c1b63e0df1fbbf680(
    value: _aws_cdk_ceddda9d.Tag,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d2fe143301dd3d265f5f1750dd6ab247959291aa58d9bce05f8c56b4f344c8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    package_manager: typing.Optional[LinuxPackageManager] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20c5f3a4a96d24bc2a31eacda3939a11c2035b5e4fcf9380137489c17341945(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    shutdown_schedule: typing.Optional[builtins.str] = None,
    timezone: typing.Optional[builtins.str] = None,
    security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c5eb5d2425a6ba047212fdbb212bb22b5ea4f715a07994187a46e224e783d0(
    *,
    security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f233056224dad4198c6b3840156f81e4d4651903cf5991bd969b5058007b8de(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    create_key_pair: typing.Optional[builtins.bool] = None,
    windows_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd5f7707a4e08252b5f9ab03f5c0075fb9d021c347cdc3d91379038feae5f18(
    *,
    security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68e0a887b77501e8f814e7a5042ac8edeaa36ce71a6cbdfa11a401db9291002(
    *,
    security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8df5f28512d4245b00b07930ac2c7864db6bbfcfdcdb0ad97e356a8ee11124(
    *,
    instance_arn: builtins.str,
    name: builtins.str,
    customer_managed_policy_references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[typing.Union[_aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.CustomerManagedPolicyReferenceProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_ceddda9d.IResolvable]]]] = None,
    description: typing.Optional[builtins.str] = None,
    inline_policy: typing.Any = None,
    managed_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    permissions_boundary: typing.Optional[typing.Union[typing.Union[_aws_cdk_aws_sso_ceddda9d.CfnPermissionSet.PermissionsBoundaryProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_ceddda9d.IResolvable]] = None,
    relay_state_type: typing.Optional[builtins.str] = None,
    session_duration: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb363a409be0a64d6a7ca2d28fc197b4a7666564292443b03c94ac6894b7adf3(
    *,
    security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    package_manager: typing.Optional[LinuxPackageManager] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2250f6eba1c2f7b5e4c4442234b20fefee08efc82b11f3d707dbaea416fe3634(
    *,
    security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    shutdown_schedule: typing.Optional[builtins.str] = None,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31883eb5756a6741d041ca9007f0375ef0c0ac7f012ef1da368dbb92b236957(
    *,
    security_tag: typing.Optional[_aws_cdk_ceddda9d.Tag] = None,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    block_devices: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.BlockDevice, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    create_key_pair: typing.Optional[builtins.bool] = None,
    windows_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
