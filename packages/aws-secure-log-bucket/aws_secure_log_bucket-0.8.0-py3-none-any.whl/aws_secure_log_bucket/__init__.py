'''
# AWS Secure Log Bucket

secure multiple transition phases in a single lifecycle policy bucket.

## Lifecycle rule

The storage class will be changed with the following lifecycle configuration.

| Storage Class       | Defaul transition after days |
| ------------------- |------------------------------|
| INFREQUENT_ACCESS   | 60 days                      |
| INTELLIGENT_TIERING | 120 days                     |
| GLACIER             | 180 days                     |
| DEEP_ARCHIVE        | 360 days                     |

## Install

### TypeScript

```shell
npm install aws-secure-log-bucket
```

or

```shell
yarn add aws-secure-log-bucket
```

### Python

```shell
pip install aws-secure-log-bucket
```

## Example

```shell
npm install aws-secure-log-bucket
```

```python
import { SecureLogBucket } from 'aws-secure-log-bucket';

new SecureLogBucket(stack, 'SecureLogBucket');
```

## License

This project is licensed under the Apache-2.0 License.
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

import aws_secure_bucket as _aws_secure_bucket_ae9bb41b
import constructs as _constructs_77d1e7e8


class SecureLogBucket(
    _aws_secure_bucket_ae9bb41b.SecureBucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-secure-log-bucket.SecureLogBucket",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        change_class_transition: typing.Optional[typing.Union["StorageClassTransitionProperty", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_name: 
        :param change_class_transition: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8264cea01228aa6e52b29da152e8b2f0857c5bfadb18e46b4271b61545cfcef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecureLogBucketProps(
            bucket_name=bucket_name, change_class_transition=change_class_transition
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-secure-log-bucket.SecureLogBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "change_class_transition": "changeClassTransition",
    },
)
class SecureLogBucketProps:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        change_class_transition: typing.Optional[typing.Union["StorageClassTransitionProperty", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_name: 
        :param change_class_transition: 
        '''
        if isinstance(change_class_transition, dict):
            change_class_transition = StorageClassTransitionProperty(**change_class_transition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bf1a01388aaea55160c779ad1e8c059d1beb5a3c25576875a7be310154155d1)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument change_class_transition", value=change_class_transition, expected_type=type_hints["change_class_transition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if change_class_transition is not None:
            self._values["change_class_transition"] = change_class_transition

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def change_class_transition(
        self,
    ) -> typing.Optional["StorageClassTransitionProperty"]:
        result = self._values.get("change_class_transition")
        return typing.cast(typing.Optional["StorageClassTransitionProperty"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecureLogBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-secure-log-bucket.StorageClassTransitionProperty",
    jsii_struct_bases=[],
    name_mapping={
        "deep_archive_days": "deepArchiveDays",
        "glacier_days": "glacierDays",
        "infrequent_access_days": "infrequentAccessDays",
        "intelligent_tiering_days": "intelligentTieringDays",
    },
)
class StorageClassTransitionProperty:
    def __init__(
        self,
        *,
        deep_archive_days: jsii.Number,
        glacier_days: jsii.Number,
        infrequent_access_days: jsii.Number,
        intelligent_tiering_days: jsii.Number,
    ) -> None:
        '''
        :param deep_archive_days: 
        :param glacier_days: 
        :param infrequent_access_days: 
        :param intelligent_tiering_days: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e3590347e6e78f5e7467dc8719a17e4bf6ea44b6def92134b8db1f6d6e0c27)
            check_type(argname="argument deep_archive_days", value=deep_archive_days, expected_type=type_hints["deep_archive_days"])
            check_type(argname="argument glacier_days", value=glacier_days, expected_type=type_hints["glacier_days"])
            check_type(argname="argument infrequent_access_days", value=infrequent_access_days, expected_type=type_hints["infrequent_access_days"])
            check_type(argname="argument intelligent_tiering_days", value=intelligent_tiering_days, expected_type=type_hints["intelligent_tiering_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deep_archive_days": deep_archive_days,
            "glacier_days": glacier_days,
            "infrequent_access_days": infrequent_access_days,
            "intelligent_tiering_days": intelligent_tiering_days,
        }

    @builtins.property
    def deep_archive_days(self) -> jsii.Number:
        result = self._values.get("deep_archive_days")
        assert result is not None, "Required property 'deep_archive_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def glacier_days(self) -> jsii.Number:
        result = self._values.get("glacier_days")
        assert result is not None, "Required property 'glacier_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def infrequent_access_days(self) -> jsii.Number:
        result = self._values.get("infrequent_access_days")
        assert result is not None, "Required property 'infrequent_access_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def intelligent_tiering_days(self) -> jsii.Number:
        result = self._values.get("intelligent_tiering_days")
        assert result is not None, "Required property 'intelligent_tiering_days' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageClassTransitionProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SecureLogBucket",
    "SecureLogBucketProps",
    "StorageClassTransitionProperty",
]

publication.publish()

def _typecheckingstub__a8264cea01228aa6e52b29da152e8b2f0857c5bfadb18e46b4271b61545cfcef(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    change_class_transition: typing.Optional[typing.Union[StorageClassTransitionProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf1a01388aaea55160c779ad1e8c059d1beb5a3c25576875a7be310154155d1(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    change_class_transition: typing.Optional[typing.Union[StorageClassTransitionProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e3590347e6e78f5e7467dc8719a17e4bf6ea44b6def92134b8db1f6d6e0c27(
    *,
    deep_archive_days: jsii.Number,
    glacier_days: jsii.Number,
    infrequent_access_days: jsii.Number,
    intelligent_tiering_days: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass
