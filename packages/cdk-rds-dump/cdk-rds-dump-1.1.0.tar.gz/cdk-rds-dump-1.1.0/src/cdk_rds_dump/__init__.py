'''
# Under construction!!!!!!!

# cdk-rds-dump

CDK constructs that dump the contents of AWS RDS, generate SQL files, and save them to S3

# Welcome to your CDK TypeScript Construct Library project

You should explore the contents of this project. It demonstrates a CDK Construct Library that includes a construct (`CdkRdsDump`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The construct defines an interface (`CdkRdsDumpProps`) to configure the visibility timeout of the queue.

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
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

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_rds as _aws_cdk_aws_rds_ceddda9d
import constructs as _constructs_77d1e7e8


class RdsDump(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-rds-dump.RdsDump",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        create_secrets_manager_vpc_endpoint: builtins.bool,
        database_name: builtins.str,
        db_engine: builtins.str,
        rds_cluster: _aws_cdk_aws_rds_ceddda9d.DatabaseCluster,
        schedule: _aws_cdk_aws_events_ceddda9d.Schedule,
        id_suffix: typing.Optional[builtins.str] = None,
        lambda_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lambda_nsg: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        secret_id: typing.Optional[builtins.str] = None,
        secrets_manager_vpc_endpoint_nsg_id: typing.Optional[builtins.str] = None,
        unsecure_password: typing.Optional[builtins.str] = None,
        unsecure_user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param create_secrets_manager_vpc_endpoint: 
        :param database_name: 
        :param db_engine: 
        :param rds_cluster: 
        :param schedule: 
        :param id_suffix: 
        :param lambda_env: 
        :param lambda_nsg: 
        :param secret_id: 
        :param secrets_manager_vpc_endpoint_nsg_id: 
        :param unsecure_password: 
        :param unsecure_user_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a38fc7ecfd277f87fd8e580c47c6b6b6ef0f7559271578ac203a7ce2e09649b7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        __2 = RdsDumpProps(
            create_secrets_manager_vpc_endpoint=create_secrets_manager_vpc_endpoint,
            database_name=database_name,
            db_engine=db_engine,
            rds_cluster=rds_cluster,
            schedule=schedule,
            id_suffix=id_suffix,
            lambda_env=lambda_env,
            lambda_nsg=lambda_nsg,
            secret_id=secret_id,
            secrets_manager_vpc_endpoint_nsg_id=secrets_manager_vpc_endpoint_nsg_id,
            unsecure_password=unsecure_password,
            unsecure_user_name=unsecure_user_name,
        )

        jsii.create(self.__class__, self, [scope, id, __2])


@jsii.data_type(
    jsii_type="cdk-rds-dump.RdsDumpProps",
    jsii_struct_bases=[],
    name_mapping={
        "create_secrets_manager_vpc_endpoint": "createSecretsManagerVPCEndpoint",
        "database_name": "databaseName",
        "db_engine": "dbEngine",
        "rds_cluster": "rdsCluster",
        "schedule": "schedule",
        "id_suffix": "idSuffix",
        "lambda_env": "lambdaEnv",
        "lambda_nsg": "lambdaNsg",
        "secret_id": "secretId",
        "secrets_manager_vpc_endpoint_nsg_id": "secretsManagerVPCEndpointNsgId",
        "unsecure_password": "unsecurePassword",
        "unsecure_user_name": "unsecureUserName",
    },
)
class RdsDumpProps:
    def __init__(
        self,
        *,
        create_secrets_manager_vpc_endpoint: builtins.bool,
        database_name: builtins.str,
        db_engine: builtins.str,
        rds_cluster: _aws_cdk_aws_rds_ceddda9d.DatabaseCluster,
        schedule: _aws_cdk_aws_events_ceddda9d.Schedule,
        id_suffix: typing.Optional[builtins.str] = None,
        lambda_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lambda_nsg: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        secret_id: typing.Optional[builtins.str] = None,
        secrets_manager_vpc_endpoint_nsg_id: typing.Optional[builtins.str] = None,
        unsecure_password: typing.Optional[builtins.str] = None,
        unsecure_user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create_secrets_manager_vpc_endpoint: 
        :param database_name: 
        :param db_engine: 
        :param rds_cluster: 
        :param schedule: 
        :param id_suffix: 
        :param lambda_env: 
        :param lambda_nsg: 
        :param secret_id: 
        :param secrets_manager_vpc_endpoint_nsg_id: 
        :param unsecure_password: 
        :param unsecure_user_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e5f91888e54819ce8e66b2c7e425c251eafd75500758ab8d657b3e1e91f875)
            check_type(argname="argument create_secrets_manager_vpc_endpoint", value=create_secrets_manager_vpc_endpoint, expected_type=type_hints["create_secrets_manager_vpc_endpoint"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument db_engine", value=db_engine, expected_type=type_hints["db_engine"])
            check_type(argname="argument rds_cluster", value=rds_cluster, expected_type=type_hints["rds_cluster"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument id_suffix", value=id_suffix, expected_type=type_hints["id_suffix"])
            check_type(argname="argument lambda_env", value=lambda_env, expected_type=type_hints["lambda_env"])
            check_type(argname="argument lambda_nsg", value=lambda_nsg, expected_type=type_hints["lambda_nsg"])
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            check_type(argname="argument secrets_manager_vpc_endpoint_nsg_id", value=secrets_manager_vpc_endpoint_nsg_id, expected_type=type_hints["secrets_manager_vpc_endpoint_nsg_id"])
            check_type(argname="argument unsecure_password", value=unsecure_password, expected_type=type_hints["unsecure_password"])
            check_type(argname="argument unsecure_user_name", value=unsecure_user_name, expected_type=type_hints["unsecure_user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "create_secrets_manager_vpc_endpoint": create_secrets_manager_vpc_endpoint,
            "database_name": database_name,
            "db_engine": db_engine,
            "rds_cluster": rds_cluster,
            "schedule": schedule,
        }
        if id_suffix is not None:
            self._values["id_suffix"] = id_suffix
        if lambda_env is not None:
            self._values["lambda_env"] = lambda_env
        if lambda_nsg is not None:
            self._values["lambda_nsg"] = lambda_nsg
        if secret_id is not None:
            self._values["secret_id"] = secret_id
        if secrets_manager_vpc_endpoint_nsg_id is not None:
            self._values["secrets_manager_vpc_endpoint_nsg_id"] = secrets_manager_vpc_endpoint_nsg_id
        if unsecure_password is not None:
            self._values["unsecure_password"] = unsecure_password
        if unsecure_user_name is not None:
            self._values["unsecure_user_name"] = unsecure_user_name

    @builtins.property
    def create_secrets_manager_vpc_endpoint(self) -> builtins.bool:
        result = self._values.get("create_secrets_manager_vpc_endpoint")
        assert result is not None, "Required property 'create_secrets_manager_vpc_endpoint' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def database_name(self) -> builtins.str:
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def db_engine(self) -> builtins.str:
        result = self._values.get("db_engine")
        assert result is not None, "Required property 'db_engine' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rds_cluster(self) -> _aws_cdk_aws_rds_ceddda9d.DatabaseCluster:
        result = self._values.get("rds_cluster")
        assert result is not None, "Required property 'rds_cluster' is missing"
        return typing.cast(_aws_cdk_aws_rds_ceddda9d.DatabaseCluster, result)

    @builtins.property
    def schedule(self) -> _aws_cdk_aws_events_ceddda9d.Schedule:
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(_aws_cdk_aws_events_ceddda9d.Schedule, result)

    @builtins.property
    def id_suffix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("id_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("lambda_env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def lambda_nsg(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        result = self._values.get("lambda_nsg")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def secret_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets_manager_vpc_endpoint_nsg_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("secrets_manager_vpc_endpoint_nsg_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unsecure_password(self) -> typing.Optional[builtins.str]:
        result = self._values.get("unsecure_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unsecure_user_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("unsecure_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsDumpProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "RdsDump",
    "RdsDumpProps",
]

publication.publish()

def _typecheckingstub__a38fc7ecfd277f87fd8e580c47c6b6b6ef0f7559271578ac203a7ce2e09649b7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    create_secrets_manager_vpc_endpoint: builtins.bool,
    database_name: builtins.str,
    db_engine: builtins.str,
    rds_cluster: _aws_cdk_aws_rds_ceddda9d.DatabaseCluster,
    schedule: _aws_cdk_aws_events_ceddda9d.Schedule,
    id_suffix: typing.Optional[builtins.str] = None,
    lambda_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lambda_nsg: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    secret_id: typing.Optional[builtins.str] = None,
    secrets_manager_vpc_endpoint_nsg_id: typing.Optional[builtins.str] = None,
    unsecure_password: typing.Optional[builtins.str] = None,
    unsecure_user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e5f91888e54819ce8e66b2c7e425c251eafd75500758ab8d657b3e1e91f875(
    *,
    create_secrets_manager_vpc_endpoint: builtins.bool,
    database_name: builtins.str,
    db_engine: builtins.str,
    rds_cluster: _aws_cdk_aws_rds_ceddda9d.DatabaseCluster,
    schedule: _aws_cdk_aws_events_ceddda9d.Schedule,
    id_suffix: typing.Optional[builtins.str] = None,
    lambda_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lambda_nsg: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    secret_id: typing.Optional[builtins.str] = None,
    secrets_manager_vpc_endpoint_nsg_id: typing.Optional[builtins.str] = None,
    unsecure_password: typing.Optional[builtins.str] = None,
    unsecure_user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
