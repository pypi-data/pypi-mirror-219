'''
# AWS Secure Bucket

This is a Simple S3 Secure Bucket.

* Bucket Access Control is Private
* Public Read Access is false
* Enforce SSL
* All Block public access
* Require encryption

## Install

### TypeScript

```shell
npm install @birdroid/aws-secure-bucket
```

or

```shell
yarn add @birdroid/aws-secure-bucket
```

### Python

```shell
pip install birdroid.aws-secure-bucket
```

## Example

### TypeScript

```shell
npm install @birdroid/aws-secure-bucket
```

```python
import { SecureBucket } from '@birdroid/aws-secure-bucket';

const bucket = new SecureBucket(stack, 'SecureBucket', {
  bucketName: 'example-secure-bucket',
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

from ._jsii import *

import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


class SecureBucket(
    _aws_cdk_aws_s3_ceddda9d.Bucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="@birdroid/aws-secure-bucket.SecureBucket",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        encryption: typing.Optional["SecureBucketEncryption"] = None,
        event_bridge_enabled: typing.Optional[builtins.bool] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        versioned: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_name: 
        :param encryption: 
        :param event_bridge_enabled: 
        :param lifecycle_rules: 
        :param versioned: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f782873b0449e8c0a28366ae052b8e545ea51863640d309a5e58b8aaa6618158)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecureBucketProps(
            bucket_name=bucket_name,
            encryption=encryption,
            event_bridge_enabled=event_bridge_enabled,
            lifecycle_rules=lifecycle_rules,
            versioned=versioned,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.enum(jsii_type="@birdroid/aws-secure-bucket.SecureBucketEncryption")
class SecureBucketEncryption(enum.Enum):
    KMS_MANAGED = "KMS_MANAGED"
    '''Server-side KMS encryption with a master key managed by KMS.'''
    S3_MANAGED = "S3_MANAGED"
    '''Server-side encryption with a master key managed by S3.'''


@jsii.data_type(
    jsii_type="@birdroid/aws-secure-bucket.SecureBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "encryption": "encryption",
        "event_bridge_enabled": "eventBridgeEnabled",
        "lifecycle_rules": "lifecycleRules",
        "versioned": "versioned",
    },
)
class SecureBucketProps:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        encryption: typing.Optional[SecureBucketEncryption] = None,
        event_bridge_enabled: typing.Optional[builtins.bool] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        versioned: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param bucket_name: 
        :param encryption: 
        :param event_bridge_enabled: 
        :param lifecycle_rules: 
        :param versioned: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd69d5c35c5e8a601f834ba22e790b83f44a45ebc1e0af1fae1ac2f5496d74b6)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument event_bridge_enabled", value=event_bridge_enabled, expected_type=type_hints["event_bridge_enabled"])
            check_type(argname="argument lifecycle_rules", value=lifecycle_rules, expected_type=type_hints["lifecycle_rules"])
            check_type(argname="argument versioned", value=versioned, expected_type=type_hints["versioned"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if encryption is not None:
            self._values["encryption"] = encryption
        if event_bridge_enabled is not None:
            self._values["event_bridge_enabled"] = event_bridge_enabled
        if lifecycle_rules is not None:
            self._values["lifecycle_rules"] = lifecycle_rules
        if versioned is not None:
            self._values["versioned"] = versioned

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption(self) -> typing.Optional[SecureBucketEncryption]:
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[SecureBucketEncryption], result)

    @builtins.property
    def event_bridge_enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("event_bridge_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def lifecycle_rules(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.LifecycleRule]]:
        result = self._values.get("lifecycle_rules")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.LifecycleRule]], result)

    @builtins.property
    def versioned(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("versioned")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecureBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SecureBucket",
    "SecureBucketEncryption",
    "SecureBucketProps",
]

publication.publish()

def _typecheckingstub__f782873b0449e8c0a28366ae052b8e545ea51863640d309a5e58b8aaa6618158(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[SecureBucketEncryption] = None,
    event_bridge_enabled: typing.Optional[builtins.bool] = None,
    lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    versioned: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd69d5c35c5e8a601f834ba22e790b83f44a45ebc1e0af1fae1ac2f5496d74b6(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[SecureBucketEncryption] = None,
    event_bridge_enabled: typing.Optional[builtins.bool] = None,
    lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    versioned: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
