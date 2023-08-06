'''
<h1 align="center">
  <div align="center">
      <img align="middle" alt="Typescript" src="./resources/typescript.svg" width=15>
      <img align="middle" alt="Java" src="./resources/java.svg" width=20>
      <img align="middle" alt="Go" src="./resources/go.svg" width=30>
      <img align="middle" alt="Python" src="./resources/python.svg" width=15>
      <img align="middle" alt=".NET" src="./resources/dotnet.svg" width=30>
  </div>
  OpenNext CDK
</h1>
<div align="center">
  <a href="https://github.com/datasprayio/open-next-cdk/actions?query=workflow%3A%22build%22">
    <img align="middle" alt="Build Status" src="https://img.shields.io/github/actions/workflow/status/datasprayio/open-next-cdk/build.yml?style=for-the-badge">
  </a>
  <a href="https://github.com/datasprayio/open-next-cdk/blob/master/LICENSE">
    <img align="middle" alt="License" src="https://img.shields.io/github/license/datasprayio/open-next-cdk?style=for-the-badge">
  </a>
  <a href="https://www.npmjs.com/package/open-next-cdk">
    <img align="middle" alt="NPM release" src="https://img.shields.io/npm/v/open-next-cdk?label=RELEASE&color=blue&style=for-the-badge">
  </a>
</div>
<h3 align="center">Deploy NextJS on AWS using CDK IaC and OpenNext packaging</h3>

### Contents

* [What is this?](#what-is-this)
* [Quickstart](#quickstart)
* [Requirements](#requirements)
* [Advanced](#advanced)

  * [Pre-built OpenNext package](#pre-built-opennext-package)
  * [Additional security](#additional-security)
* [About](#about)

  * [Benefits](#benefits)
  * [Dependencies](#dependencies)
  * [Similar projects](#similar-projects)
* [Contributing](#contributing)

  * [Using Projen](#using-projen)

# What is this?

A building block for Amazon's infrastructure-as-code CDK toolkit to deploy a NextJS app using AWS serverless services.

Your NextJS app is packaged using OpenNext to fit the serverless format on Lambda

# Requirements

NextJs versions: >=12.3.0+ (includes 13.0.0+)

Platforms: darwin-x64, linux-arm64, linux-x64, win32-arm64, win32-x64

# Quickstart

### NextJS setup

Add a dev dependency `esbuild@0.17.16` to your NextJS project.

```shell
npm install --save-dev esbuild@0.17.16
```

### CDK Construct

Use this construct in your CDK application to deploy your NextJS app to AWS.

<details>
  <summary><img align="middle" alt="Typescript" src="./resources/typescript.svg" width=20> Typescript</summary>  <a href="https://www.npmjs.com/package/open-next-cdk">
    <img align="middle" alt="NPM release" src="https://img.shields.io/npm/v/open-next-cdk?style=for-the-badge">
  </a>

Install the dependency using npm:

```shell
npm install --save-dev esbuild@0.17.16 open-next-cdk
```

Use the construct in your CDK application:

```python
import { Nextjs } from 'open-next-cdk';

new Nextjs(this, 'Web', {
  nextjsPath: './web', // relative path to nextjs project root
});
```

</details>
<details>
  <summary><img align="middle" alt="Java" src="./resources/java.svg" width=20> Java</summary>
  <a href="https://search.maven.org/artifact/io.dataspray/open-next-cdk">
    <img align="middle" alt="Maven Central release" src="https://img.shields.io/maven-central/v/io.dataspray/open-next-cdk?style=for-the-badge">
  </a>

Install the dependency using Maven:

```xml
<dependency>
  <groupId>io.dataspray</groupId>
  <artifactId>open-next-cdk</artifactId>
  <version>x.y.z</version>
</dependency>
```

Use the construct in your CDK application:

```java
Nextjs.Builder.create(this, getConstructId())
        .nextjsPath("./web")
        .build();
```

</details>
<details>
  <summary><img align="middle" alt="Go" src="./resources/go.svg" width=20> Go</summary>  <a href="https://github.com/datasprayio/open-next-cdk/tree/main/opennextcdk">
    <img align="middle" alt="Go release" src="https://img.shields.io/github/go-mod/go-version/datasprayio/open-next-cdk/main?filename=opennextcdk%2Fgo.mod&label=GO&style=for-the-badge">
  </a>

Install the dependency:

```shell
go get github.com:datasprayio/open-next-cdk.git@go
```

</details>
<details>
  <summary><img align="middle" alt="Python" src="./resources/python.svg" width=20> Python</summary>  <a href="https://pypi.org/project/open-next-cdk/">
    <img align="middle" alt="Pypi release" src="https://img.shields.io/pypi/v/open-next-cdk?style=for-the-badge">
  </a>

Install the dependency:

```shell
pip install open-next-cdk
```

</details>
<details>
  <summary><img align="middle" alt=".NET" src="./resources/dotnet.svg" width=20> .NET</summary>  <a href="https://www.nuget.org/packages/Dataspray.OpenNextCdk">
    <img align="middle" alt="Nuget release" src="https://img.shields.io/nuget/v/Dataspray.OpenNextCdk?style=for-the-badge">
  </a>

Install the dependency:

```shell
dotnet add package Dataspray.OpenNextCdk
```

</details>
<br/>

This will automatically build your NextJS app and package it for you as part of the CDK construct.

If you would prefer to package it separately, see below:

# Advanced

### Pre-built OpenNext package

<details>
  <summary>How-to</summary>

You may also provide already pre-built OpenNext package directly by building it yourself first:

```shell
open-next build
```

You will find a new folder `.open-next` which contains the packaging for your NextJS App. Now you can use the construct by instructing it not to build your app, just use the OpenNext folder directly:

```python
import { Nextjs } from 'open-next-cdk';

new Nextjs(this, 'Web', {
  openNextPath: './web/.open-next', // relative path to .open-next folder
});
```

</details>

### Additional security

<details>
  <summary>How-to</summary>

```python
import { RemovalPolicy, Stack } from "aws-cdk-lib";
import { Construct } from "constructs";
import { CfnWebAcl } from "aws-cdk-lib/aws-wafv2";
import { SecurityPolicyProtocol, type DistributionProps } from "aws-cdk-lib/aws-cloudfront";
import { Nextjs, type NextjsDistributionProps } from "cdk-nextjs-standalone";
import { Bucket, BlockPublicAccess, BucketEncryption } from "aws-cdk-lib/aws-s3";

// Because of `WebAcl`, this stack must be deployed in us-east-1. If you want
// to deploy Nextjs in another region, add WAF in separate stack deployed in us-east-1
export class UiStack {
  constructor(scope: Construct, id: string) {
    const webAcl = new CfnWebAcl(this, "WebAcl", { ... });
    new Nextjs(this, "NextSite", {
      nextjsPath: "...",
      defaults: {
        assetDeployment: {
          bucket: new Bucket(this, "NextjsAssetDeploymentBucket", {
            autoDeleteObjects: true,
            removalPolicy: RemovalPolicy.DESTROY,
            encryption: BucketEncryption.S3_MANAGED,
            enforceSSL: true,
            blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
          }),
        },
        distribution: {
          functionUrlAuthType: FunctionUrlAuthType.AWS_IAM,
          cdk: {
            distribution: {
              webAclId: webAcl.attrArn,
              minimumProtocolVersion: SecurityPolicyProtocol.TLS_V1_2_2021,
            } as DistributionProps,
          },
        } satisfies Partial<NextjsDistributionProps>,
      },
    });
  }
}
```

</details>
<br />

# About

Deploys a NextJs static site with server-side rendering and API support. Uses AWS lambda and CloudFront.

There is a new (since Next 12) [standalone output mode which uses output tracing](https://nextjs.org/docs/advanced-features/output-file-tracing) to generate a minimal server and static files.
This standalone server can be converted into a CloudFront distribution and a lambda handler that handles SSR, API, and routing.

The CloudFront default origin first checks S3 for static files and falls back to an HTTP origin using a lambda function URL.

## Benefits

This approach is most compatible with new NextJs features such as ESM configuration, [middleware](https://nextjs.org/docs/advanced-features/middleware), next-auth, and React server components ("appDir").

The unmaintained [@serverless-nextjs project](https://github.com/serverless-nextjs/serverless-next.js) uses the deprecated `serverless` NextJs build target which [prevents the use of new features](https://github.com/serverless-nextjs/serverless-next.js/pull/2478).
This construct was created to use the new `standalone` output build and newer AWS features like lambda function URLs and fallback origins.

You may want to look at [Serverless Stack](https://sst.dev) and its [NextjsSite](https://docs.sst.dev/constructs/NextjsSite) construct for an improved developer experience if you are building serverless applications on CDK.

## Dependencies

Built on top of [open-next](https://open-next.js.org/), which was partially built using the original core of cdk-nextjs-standalone.

## Similar projects

### Heavily based on

* [Open-next](https://open-next.js.org/)
* [https://github.com/iiroj/iiro.fi/commit/bd43222032d0dbb765e1111825f64dbb5db851d9](https://github.com/iiroj/iiro.fi/commit/bd43222032d0dbb765e1111825f64dbb5db851d9)
* [https://github.com/sladg/nextjs-lambda](https://github.com/sladg/nextjs-lambda)
* [https://github.com/serverless-nextjs/serverless-next.js/tree/master/packages/compat-layers/apigw-lambda-compat](https://github.com/serverless-nextjs/serverless-next.js/tree/master/packages/compat-layers/apigw-lambda-compat)
* [Serverless Stack](https://github.com/serverless-stack/sst)

  * [RemixSite](https://github.com/serverless-stack/sst/blob/master/packages/resources/src/NextjsSite.ts) construct
  * [NextjsSite](https://github.com/serverless-stack/sst/blob/master/packages/resources/src/RemixSite.ts) construct

### Fork from cdk-nextjs

This project has been initially forked from [cdk-nextjs](https://github.com/jetbridge/cdk-nextjs) in order to [publish the package to other langugages](https://github.com/jetbridge/cdk-nextjs/issues/120#issuecomment-1634926223). So far notable changes are:

* Extended language support: TS, Java, Go, .NET, Python.
* Extended platform support: darwin-x64, linux-arm64, linux-x64, win32-arm64, win32-x64
* Use pre-built open-next package

# Contributing

Hey there, we value every new contribution a lot 🙏🏼 thank you. Open an issue or a PR and we'll gladly help you out.

## Using Projen

Most boilerplate files are pre-generated including package.json. Don't update it directly, rather update `.projenrc.js` then run `yarn projen` to re-generate the files.
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
import aws_cdk.aws_cloudfront as _aws_cdk_aws_cloudfront_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_s3_deployment as _aws_cdk_aws_s3_deployment_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="open-next-cdk.BaseSiteDomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "alternate_names": "alternateNames",
        "certificate": "certificate",
        "domain_alias": "domainAlias",
        "hosted_zone": "hostedZone",
        "is_external_domain": "isExternalDomain",
    },
)
class BaseSiteDomainProps:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        alternate_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        domain_alias: typing.Optional[builtins.str] = None,
        hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
        is_external_domain: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param domain_name: The domain to be assigned to the website URL (ie. domain.com). Supports domains that are hosted either on `Route 53 <https://aws.amazon.com/route53/>`_ or externally.
        :param alternate_names: Specify additional names that should route to the Cloudfront Distribution. Note, certificates for these names will not be automatically generated so the ``certificate`` option must be specified.
        :param certificate: Import the certificate for the domain. By default, SST will create a certificate with the domain name. The certificate will be created in the ``us-east-1``(N. Virginia) region as required by AWS CloudFront. Set this option if you have an existing certificate in the ``us-east-1`` region in AWS Certificate Manager you want to use.
        :param domain_alias: An alternative domain to be assigned to the website URL. Visitors to the alias will be redirected to the main domain. (ie. ``www.domain.com``). Use this to create a ``www.`` version of your domain and redirect visitors to the root domain.
        :param hosted_zone: Import the underlying Route 53 hosted zone.
        :param is_external_domain: Set this option if the domain is not hosted on Amazon Route 53.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__019eb9cb658a919f238ec89c2ac4f8d4f430a39ae77b8e15a0af0e839efefa8f)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument alternate_names", value=alternate_names, expected_type=type_hints["alternate_names"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument domain_alias", value=domain_alias, expected_type=type_hints["domain_alias"])
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
            check_type(argname="argument is_external_domain", value=is_external_domain, expected_type=type_hints["is_external_domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
        }
        if alternate_names is not None:
            self._values["alternate_names"] = alternate_names
        if certificate is not None:
            self._values["certificate"] = certificate
        if domain_alias is not None:
            self._values["domain_alias"] = domain_alias
        if hosted_zone is not None:
            self._values["hosted_zone"] = hosted_zone
        if is_external_domain is not None:
            self._values["is_external_domain"] = is_external_domain

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''The domain to be assigned to the website URL (ie. domain.com).

        Supports domains that are hosted either on `Route 53 <https://aws.amazon.com/route53/>`_ or externally.
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alternate_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify additional names that should route to the Cloudfront Distribution.

        Note, certificates for these names will not be automatically generated so the ``certificate`` option must be specified.
        '''
        result = self._values.get("alternate_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        '''Import the certificate for the domain.

        By default, SST will create a certificate with the domain name. The certificate will be created in the ``us-east-1``(N. Virginia) region as required by AWS CloudFront.

        Set this option if you have an existing certificate in the ``us-east-1`` region in AWS Certificate Manager you want to use.
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], result)

    @builtins.property
    def domain_alias(self) -> typing.Optional[builtins.str]:
        '''An alternative domain to be assigned to the website URL.

        Visitors to the alias will be redirected to the main domain. (ie. ``www.domain.com``).

        Use this to create a ``www.`` version of your domain and redirect visitors to the root domain.
        '''
        result = self._values.get("domain_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hosted_zone(self) -> typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone]:
        '''Import the underlying Route 53 hosted zone.'''
        result = self._values.get("hosted_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone], result)

    @builtins.property
    def is_external_domain(self) -> typing.Optional[builtins.bool]:
        '''Set this option if the domain is not hosted on Amazon Route 53.'''
        result = self._values.get("is_external_domain")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseSiteDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="open-next-cdk.BaseSiteEnvironmentOutputsInfo",
    jsii_struct_bases=[],
    name_mapping={
        "environment_outputs": "environmentOutputs",
        "path": "path",
        "stack": "stack",
    },
)
class BaseSiteEnvironmentOutputsInfo:
    def __init__(
        self,
        *,
        environment_outputs: typing.Mapping[builtins.str, builtins.str],
        path: builtins.str,
        stack: builtins.str,
    ) -> None:
        '''
        :param environment_outputs: 
        :param path: 
        :param stack: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a37ab543538565e7eca2e38a6e7c09a4a90a2a5367294a1559439e7e1971a4b)
            check_type(argname="argument environment_outputs", value=environment_outputs, expected_type=type_hints["environment_outputs"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "environment_outputs": environment_outputs,
            "path": path,
            "stack": stack,
        }

    @builtins.property
    def environment_outputs(self) -> typing.Mapping[builtins.str, builtins.str]:
        result = self._values.get("environment_outputs")
        assert result is not None, "Required property 'environment_outputs' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def path(self) -> builtins.str:
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stack(self) -> builtins.str:
        result = self._values.get("stack")
        assert result is not None, "Required property 'stack' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseSiteEnvironmentOutputsInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="open-next-cdk.BaseSiteReplaceProps",
    jsii_struct_bases=[],
    name_mapping={"files": "files", "replace": "replace", "search": "search"},
)
class BaseSiteReplaceProps:
    def __init__(
        self,
        *,
        files: builtins.str,
        replace: builtins.str,
        search: builtins.str,
    ) -> None:
        '''
        :param files: 
        :param replace: 
        :param search: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc26084934caab47ace3ffcee4e6b0cac75371bb903717a566b321e735a5830e)
            check_type(argname="argument files", value=files, expected_type=type_hints["files"])
            check_type(argname="argument replace", value=replace, expected_type=type_hints["replace"])
            check_type(argname="argument search", value=search, expected_type=type_hints["search"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "files": files,
            "replace": replace,
            "search": search,
        }

    @builtins.property
    def files(self) -> builtins.str:
        result = self._values.get("files")
        assert result is not None, "Required property 'files' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replace(self) -> builtins.str:
        result = self._values.get("replace")
        assert result is not None, "Required property 'replace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def search(self) -> builtins.str:
        result = self._values.get("search")
        assert result is not None, "Required property 'search' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseSiteReplaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="open-next-cdk.CreateArchiveArgs",
    jsii_struct_bases=[],
    name_mapping={
        "directory": "directory",
        "zip_file_name": "zipFileName",
        "zip_out_dir": "zipOutDir",
        "compression_level": "compressionLevel",
        "file_glob": "fileGlob",
        "quiet": "quiet",
    },
)
class CreateArchiveArgs:
    def __init__(
        self,
        *,
        directory: builtins.str,
        zip_file_name: builtins.str,
        zip_out_dir: builtins.str,
        compression_level: typing.Optional[jsii.Number] = None,
        file_glob: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param directory: 
        :param zip_file_name: 
        :param zip_out_dir: 
        :param compression_level: 
        :param file_glob: 
        :param quiet: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee680970a366f95bf6ef80132b6eadd2e646f8f195c4e8dfbfa95337d5878bf0)
            check_type(argname="argument directory", value=directory, expected_type=type_hints["directory"])
            check_type(argname="argument zip_file_name", value=zip_file_name, expected_type=type_hints["zip_file_name"])
            check_type(argname="argument zip_out_dir", value=zip_out_dir, expected_type=type_hints["zip_out_dir"])
            check_type(argname="argument compression_level", value=compression_level, expected_type=type_hints["compression_level"])
            check_type(argname="argument file_glob", value=file_glob, expected_type=type_hints["file_glob"])
            check_type(argname="argument quiet", value=quiet, expected_type=type_hints["quiet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "directory": directory,
            "zip_file_name": zip_file_name,
            "zip_out_dir": zip_out_dir,
        }
        if compression_level is not None:
            self._values["compression_level"] = compression_level
        if file_glob is not None:
            self._values["file_glob"] = file_glob
        if quiet is not None:
            self._values["quiet"] = quiet

    @builtins.property
    def directory(self) -> builtins.str:
        result = self._values.get("directory")
        assert result is not None, "Required property 'directory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zip_file_name(self) -> builtins.str:
        result = self._values.get("zip_file_name")
        assert result is not None, "Required property 'zip_file_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zip_out_dir(self) -> builtins.str:
        result = self._values.get("zip_out_dir")
        assert result is not None, "Required property 'zip_out_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compression_level(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("compression_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def file_glob(self) -> typing.Optional[builtins.str]:
        result = self._values.get("file_glob")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quiet(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("quiet")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateArchiveArgs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImageOptimizationLambda(
    _aws_cdk_aws_lambda_ceddda9d.Function,
    metaclass=jsii.JSIIMeta,
    jsii_type="open-next-cdk.ImageOptimizationLambda",
):
    '''This lambda handles image optimization.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        next_build: "NextjsBuild",
        lambda_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_command: typing.Optional[builtins.str] = None,
        build_path: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_placeholder: typing.Optional[builtins.bool] = None,
        nextjs_path: typing.Optional[builtins.str] = None,
        next_js_path: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        open_next_path: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
        sharp_layer_arn: typing.Optional[builtins.str] = None,
        temp_build_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket: The S3 bucket holding application images.
        :param next_build: The ``NextjsBuild`` instance representing the built Nextjs application.
        :param lambda_options: Override function properties.
        :param build_command: Optional value used to install NextJS node dependencies. It defaults to 'npx --yes open-next@latest build'
        :param build_path: The directory to execute ``npm run build`` from. By default, it is ``nextjsPath``. Can be overridden, particularly useful for monorepos where ``build`` is expected to run at the root of the project.
        :param compression_level: 0 - no compression, fastest 9 - maximum compression, slowest. Default: 1
        :param environment: Custom environment variables to pass to the NextJS build and runtime.
        :param is_placeholder: (deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.
        :param nextjs_path: (deprecated) Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.
        :param next_js_path: Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param node_env: Optional value for NODE_ENV during build and runtime.
        :param open_next_path: Relative path to the OpenNext package named ``.open-next`` by default. One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param quiet: Less build output.
        :param sharp_layer_arn: Optional arn for the sharp lambda layer. If omitted, the layer will be created.
        :param temp_build_dir: Directory to store temporary build files in. Defaults to os.tmpdir().
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__157f5efeb550e21797ac19dc1f9b4330b5c51b7bdb58c9e7b911cfb50c9195cb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ImageOptimizationProps(
            bucket=bucket,
            next_build=next_build,
            lambda_options=lambda_options,
            build_command=build_command,
            build_path=build_path,
            compression_level=compression_level,
            environment=environment,
            is_placeholder=is_placeholder,
            nextjs_path=nextjs_path,
            next_js_path=next_js_path,
            node_env=node_env,
            open_next_path=open_next_path,
            quiet=quiet,
            sharp_layer_arn=sharp_layer_arn,
            temp_build_dir=temp_build_dir,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: _aws_cdk_aws_s3_ceddda9d.IBucket) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588b2f02789bdd1c109803091defa80aeaec7785450eaa47be42a9971c720cb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value)


class NextJsAssetsDeployment(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="open-next-cdk.NextJsAssetsDeployment",
):
    '''Uploads NextJS-built static and public files to S3.

    Will rewrite CloudFormation references with their resolved values after uploading.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        next_build: "NextjsBuild",
        cache_policies: typing.Optional[typing.Union["NextjsAssetsCachePolicyProps", typing.Dict[builtins.str, typing.Any]]] = None,
        distribution: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution] = None,
        ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
        prune: typing.Optional[builtins.bool] = None,
        use_efs: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        build_command: typing.Optional[builtins.str] = None,
        build_path: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_placeholder: typing.Optional[builtins.bool] = None,
        nextjs_path: typing.Optional[builtins.str] = None,
        next_js_path: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        open_next_path: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
        sharp_layer_arn: typing.Optional[builtins.str] = None,
        temp_build_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket: Properties for the S3 bucket containing the NextJS assets.
        :param next_build: The ``NextjsBuild`` instance representing the built Nextjs application.
        :param cache_policies: Override the default S3 cache policies created internally.
        :param distribution: Distribution to invalidate when assets change.
        :param ephemeral_storage_size: ephemeralStorageSize for lambda function which been run by BucketDeployment.
        :param memory_limit: memoryLimit for lambda function which been run by BucketDeployment.
        :param prune: Set to true to delete old assets (defaults to false). Recommended to only set to true if you don't need the ability to roll back deployments.
        :param use_efs: In case of useEfs, vpc is required.
        :param vpc: In case of useEfs, vpc is required.
        :param build_command: Optional value used to install NextJS node dependencies. It defaults to 'npx --yes open-next@latest build'
        :param build_path: The directory to execute ``npm run build`` from. By default, it is ``nextjsPath``. Can be overridden, particularly useful for monorepos where ``build`` is expected to run at the root of the project.
        :param compression_level: 0 - no compression, fastest 9 - maximum compression, slowest. Default: 1
        :param environment: Custom environment variables to pass to the NextJS build and runtime.
        :param is_placeholder: (deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.
        :param nextjs_path: (deprecated) Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.
        :param next_js_path: Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param node_env: Optional value for NODE_ENV during build and runtime.
        :param open_next_path: Relative path to the OpenNext package named ``.open-next`` by default. One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param quiet: Less build output.
        :param sharp_layer_arn: Optional arn for the sharp lambda layer. If omitted, the layer will be created.
        :param temp_build_dir: Directory to store temporary build files in. Defaults to os.tmpdir().
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6045d57fb31451fb936db3248c52f6b83aefddab050f147e709aae07a940f439)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NextjsAssetsDeploymentProps(
            bucket=bucket,
            next_build=next_build,
            cache_policies=cache_policies,
            distribution=distribution,
            ephemeral_storage_size=ephemeral_storage_size,
            memory_limit=memory_limit,
            prune=prune,
            use_efs=use_efs,
            vpc=vpc,
            build_command=build_command,
            build_path=build_path,
            compression_level=compression_level,
            environment=environment,
            is_placeholder=is_placeholder,
            nextjs_path=nextjs_path,
            next_js_path=next_js_path,
            node_env=node_env,
            open_next_path=open_next_path,
            quiet=quiet,
            sharp_layer_arn=sharp_layer_arn,
            temp_build_dir=temp_build_dir,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="prepareArchiveDirectory")
    def _prepare_archive_directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "prepareArchiveDirectory", []))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''Bucket containing assets.'''
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: _aws_cdk_aws_s3_ceddda9d.IBucket) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c6cec02d84c8bc3e73efd718be681e79029f97892a72e5bca357aa036a4f81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value)

    @builtins.property
    @jsii.member(jsii_name="deployments")
    def deployments(
        self,
    ) -> typing.List[_aws_cdk_aws_s3_deployment_ceddda9d.BucketDeployment]:
        '''Asset deployments to S3.'''
        return typing.cast(typing.List[_aws_cdk_aws_s3_deployment_ceddda9d.BucketDeployment], jsii.get(self, "deployments"))

    @deployments.setter
    def deployments(
        self,
        value: typing.List[_aws_cdk_aws_s3_deployment_ceddda9d.BucketDeployment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1327f99f641d04415d8421d141b6f78b0eee4bd2f8cbdae17d1e886c56fdebd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployments", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "NextjsAssetsDeploymentProps":
        return typing.cast("NextjsAssetsDeploymentProps", jsii.get(self, "props"))

    @_props.setter
    def _props(self, value: "NextjsAssetsDeploymentProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d32aed5501f7c71e063a4c5cf333b32b8c9996b9b5b4279619c90dc83c3320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)

    @builtins.property
    @jsii.member(jsii_name="staticTempDir")
    def static_temp_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "staticTempDir"))

    @static_temp_dir.setter
    def static_temp_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5cc7ae950eb1bae0bda3e0bd18762fa2dcd8c4ccf2c768de9e35455c00610ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "staticTempDir", value)

    @builtins.property
    @jsii.member(jsii_name="rewriter")
    def rewriter(self) -> typing.Optional["NextjsS3EnvRewriter"]:
        return typing.cast(typing.Optional["NextjsS3EnvRewriter"], jsii.get(self, "rewriter"))

    @rewriter.setter
    def rewriter(self, value: typing.Optional["NextjsS3EnvRewriter"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c66b1fadb3e68f42b191aa2a4aefa30763ca59ece898c809f8228a9c2621a651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rewriter", value)


class NextJsLambda(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="open-next-cdk.NextJsLambda",
):
    '''Build a lambda function from a NextJS application to handle server-side rendering, API routes, and image optimization.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        next_build: "NextjsBuild",
        lambda_: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        build_command: typing.Optional[builtins.str] = None,
        build_path: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_placeholder: typing.Optional[builtins.bool] = None,
        nextjs_path: typing.Optional[builtins.str] = None,
        next_js_path: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        open_next_path: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
        sharp_layer_arn: typing.Optional[builtins.str] = None,
        temp_build_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param next_build: Built nextJS application.
        :param lambda_: Override function properties.
        :param build_command: Optional value used to install NextJS node dependencies. It defaults to 'npx --yes open-next@latest build'
        :param build_path: The directory to execute ``npm run build`` from. By default, it is ``nextjsPath``. Can be overridden, particularly useful for monorepos where ``build`` is expected to run at the root of the project.
        :param compression_level: 0 - no compression, fastest 9 - maximum compression, slowest. Default: 1
        :param environment: Custom environment variables to pass to the NextJS build and runtime.
        :param is_placeholder: (deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.
        :param nextjs_path: (deprecated) Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.
        :param next_js_path: Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param node_env: Optional value for NODE_ENV during build and runtime.
        :param open_next_path: Relative path to the OpenNext package named ``.open-next`` by default. One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param quiet: Less build output.
        :param sharp_layer_arn: Optional arn for the sharp lambda layer. If omitted, the layer will be created.
        :param temp_build_dir: Directory to store temporary build files in. Defaults to os.tmpdir().
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c85864266153cb3d4005ca79b503771e7b9925308a48822000a74f5e033e14)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NextjsLambdaProps(
            next_build=next_build,
            lambda_=lambda_,
            build_command=build_command,
            build_path=build_path,
            compression_level=compression_level,
            environment=environment,
            is_placeholder=is_placeholder,
            nextjs_path=nextjs_path,
            next_js_path=next_js_path,
            node_env=node_env,
            open_next_path=open_next_path,
            quiet=quiet,
            sharp_layer_arn=sharp_layer_arn,
            temp_build_dir=temp_build_dir,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createConfigBucket")
    def _create_config_bucket(
        self,
        replacement_params: typing.Mapping[builtins.str, builtins.str],
    ) -> typing.Mapping[typing.Any, typing.Any]:
        '''
        :param replacement_params: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c8396a4420e3be6327f0a446fbeed1d617d702af6b5e586d255aa297905b3f)
            check_type(argname="argument replacement_params", value=replacement_params, expected_type=type_hints["replacement_params"])
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "createConfigBucket", [replacement_params]))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "lambdaFunction"))

    @lambda_function.setter
    def lambda_function(self, value: _aws_cdk_aws_lambda_ceddda9d.Function) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa71d4dacf5733f40404eadc2057462b59e9bf42dad339819d7a812526a14ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaFunction", value)

    @builtins.property
    @jsii.member(jsii_name="configBucket")
    def config_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket]:
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket], jsii.get(self, "configBucket"))

    @config_bucket.setter
    def config_bucket(
        self,
        value: typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82994df33753e5860e831c81987bda0fc5c3272885fe48c387dde700c530c5fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configBucket", value)


class Nextjs(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="open-next-cdk.Nextjs",
):
    '''The ``Nextjs`` construct is a higher level construct that makes it easy to create a NextJS app.

    Your standalone server application will be bundled using o(utput tracing and will be deployed to a Lambda function.
    Static assets will be deployed to an S3 bucket and served via CloudFront.
    You must use Next.js 10.3.0 or newer.

    Please provide a ``nextjsPath`` to the Next.js app inside your project.

    Example::

        new Nextjs(this, "Web", {
          nextjsPath: path.resolve("packages/web"),
        })
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        defaults: typing.Optional[typing.Union["NextjsDefaultsProps", typing.Dict[builtins.str, typing.Any]]] = None,
        image_optimization_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        build_command: typing.Optional[builtins.str] = None,
        build_path: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_placeholder: typing.Optional[builtins.bool] = None,
        nextjs_path: typing.Optional[builtins.str] = None,
        next_js_path: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        open_next_path: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
        sharp_layer_arn: typing.Optional[builtins.str] = None,
        temp_build_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param defaults: Allows you to override defaults for the resources created by this construct.
        :param image_optimization_bucket: Optional S3 Bucket to use, defaults to assets bucket.
        :param build_command: Optional value used to install NextJS node dependencies. It defaults to 'npx --yes open-next@latest build'
        :param build_path: The directory to execute ``npm run build`` from. By default, it is ``nextjsPath``. Can be overridden, particularly useful for monorepos where ``build`` is expected to run at the root of the project.
        :param compression_level: 0 - no compression, fastest 9 - maximum compression, slowest. Default: 1
        :param environment: Custom environment variables to pass to the NextJS build and runtime.
        :param is_placeholder: (deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.
        :param nextjs_path: (deprecated) Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.
        :param next_js_path: Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param node_env: Optional value for NODE_ENV during build and runtime.
        :param open_next_path: Relative path to the OpenNext package named ``.open-next`` by default. One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param quiet: Less build output.
        :param sharp_layer_arn: Optional arn for the sharp lambda layer. If omitted, the layer will be created.
        :param temp_build_dir: Directory to store temporary build files in. Defaults to os.tmpdir().
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9535918ed268c2e0e473996077280651fd58778071f4e8b0956e46fc71e19aa0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NextjsProps(
            defaults=defaults,
            image_optimization_bucket=image_optimization_bucket,
            build_command=build_command,
            build_path=build_path,
            compression_level=compression_level,
            environment=environment,
            is_placeholder=is_placeholder,
            nextjs_path=nextjs_path,
            next_js_path=next_js_path,
            node_env=node_env,
            open_next_path=open_next_path,
            quiet=quiet,
            sharp_layer_arn=sharp_layer_arn,
            temp_build_dir=temp_build_dir,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="assetsDeployment")
    def assets_deployment(self) -> NextJsAssetsDeployment:
        '''Asset deployment to S3.'''
        return typing.cast(NextJsAssetsDeployment, jsii.get(self, "assetsDeployment"))

    @assets_deployment.setter
    def assets_deployment(self, value: NextJsAssetsDeployment) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a96beea058283d44fc69a720bc3146dd7665681fdf587d8317b98f31848a54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetsDeployment", value)

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> "NextjsDistribution":
        '''CloudFront distribution.'''
        return typing.cast("NextjsDistribution", jsii.get(self, "distribution"))

    @distribution.setter
    def distribution(self, value: "NextjsDistribution") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66115b1083ac96ae90c36905d71a1899c5b2996a05bc48371059c5f0772a29f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distribution", value)

    @builtins.property
    @jsii.member(jsii_name="imageOptimizationFunction")
    def image_optimization_function(self) -> ImageOptimizationLambda:
        '''The image optimization handler lambda function.'''
        return typing.cast(ImageOptimizationLambda, jsii.get(self, "imageOptimizationFunction"))

    @image_optimization_function.setter
    def image_optimization_function(self, value: ImageOptimizationLambda) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d1482f66c73ff51ce110fad7c441e89de7c4233253f987165cc337cdd7e4dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageOptimizationFunction", value)

    @builtins.property
    @jsii.member(jsii_name="imageOptimizationLambdaFunctionUrl")
    def image_optimization_lambda_function_url(
        self,
    ) -> _aws_cdk_aws_lambda_ceddda9d.FunctionUrl:
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.FunctionUrl, jsii.get(self, "imageOptimizationLambdaFunctionUrl"))

    @image_optimization_lambda_function_url.setter
    def image_optimization_lambda_function_url(
        self,
        value: _aws_cdk_aws_lambda_ceddda9d.FunctionUrl,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f79cf5e6d7eec23d62a041e6a112917a27fc15aced738d0167375b4036920ae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageOptimizationLambdaFunctionUrl", value)

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionUrl")
    def lambda_function_url(self) -> _aws_cdk_aws_lambda_ceddda9d.FunctionUrl:
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.FunctionUrl, jsii.get(self, "lambdaFunctionUrl"))

    @lambda_function_url.setter
    def lambda_function_url(
        self,
        value: _aws_cdk_aws_lambda_ceddda9d.FunctionUrl,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10cf35c72782073e027c09dd0f89e4828580bd26ee19b53f61fc82d1628d63c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaFunctionUrl", value)

    @builtins.property
    @jsii.member(jsii_name="nextBuild")
    def next_build(self) -> "NextjsBuild":
        '''Built NextJS project output.'''
        return typing.cast("NextjsBuild", jsii.get(self, "nextBuild"))

    @next_build.setter
    def next_build(self, value: "NextjsBuild") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f37641bca890433f71effb5852c463b6e8ed0687407757ac84e4ea541f2ef3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextBuild", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "NextjsProps":
        return typing.cast("NextjsProps", jsii.get(self, "props"))

    @_props.setter
    def _props(self, value: "NextjsProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53482f9991762e4bf6015d390d17745121e2f9388a6aca4c38ea04c090958889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)

    @builtins.property
    @jsii.member(jsii_name="serverFunction")
    def server_function(self) -> NextJsLambda:
        '''The main NextJS server handler lambda function.'''
        return typing.cast(NextJsLambda, jsii.get(self, "serverFunction"))

    @server_function.setter
    def server_function(self, value: NextJsLambda) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d42ca1a45458c5f184ac29830e2c4f0f57574d4025ebc989c7876b17578d2090)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverFunction", value)

    @builtins.property
    @jsii.member(jsii_name="staticAssetBucket")
    def _static_asset_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "staticAssetBucket"))

    @_static_asset_bucket.setter
    def _static_asset_bucket(self, value: _aws_cdk_aws_s3_ceddda9d.IBucket) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d6273ad4e83f2dc262e098a33cae7c5b7c352a80269b88e1329f3893ad019c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "staticAssetBucket", value)

    @builtins.property
    @jsii.member(jsii_name="tempBuildDir")
    def temp_build_dir(self) -> builtins.str:
        '''Where build-time assets for deployment are stored.'''
        return typing.cast(builtins.str, jsii.get(self, "tempBuildDir"))

    @temp_build_dir.setter
    def temp_build_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2f88c2afe3d23d88a89f83eccb3397f0da1c0f7b2b95c12828733706b87319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tempBuildDir", value)

    @builtins.property
    @jsii.member(jsii_name="configBucket")
    def config_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket]:
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket], jsii.get(self, "configBucket"))

    @config_bucket.setter
    def config_bucket(
        self,
        value: typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de266f92ce9933a969eb89db4385680a75d24dd79fa1a114ae884255d2e9f14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configBucket", value)


@jsii.data_type(
    jsii_type="open-next-cdk.NextjsAssetsCachePolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "static_max_age_default": "staticMaxAgeDefault",
        "static_stale_while_revalidate_default": "staticStaleWhileRevalidateDefault",
    },
)
class NextjsAssetsCachePolicyProps:
    def __init__(
        self,
        *,
        static_max_age_default: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        static_stale_while_revalidate_default: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param static_max_age_default: Cache-control max-age default for S3 static assets. Default: 30 days.
        :param static_stale_while_revalidate_default: Cache-control stale-while-revalidate default for S3 static assets. Default: 1 day.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b262b89d865ef0d9906001dc575f0c2d26b5595c39ca421bc05d0350e73d33)
            check_type(argname="argument static_max_age_default", value=static_max_age_default, expected_type=type_hints["static_max_age_default"])
            check_type(argname="argument static_stale_while_revalidate_default", value=static_stale_while_revalidate_default, expected_type=type_hints["static_stale_while_revalidate_default"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if static_max_age_default is not None:
            self._values["static_max_age_default"] = static_max_age_default
        if static_stale_while_revalidate_default is not None:
            self._values["static_stale_while_revalidate_default"] = static_stale_while_revalidate_default

    @builtins.property
    def static_max_age_default(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''Cache-control max-age default for S3 static assets.

        Default: 30 days.
        '''
        result = self._values.get("static_max_age_default")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def static_stale_while_revalidate_default(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''Cache-control stale-while-revalidate default for S3 static assets.

        Default: 1 day.
        '''
        result = self._values.get("static_stale_while_revalidate_default")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsAssetsCachePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="open-next-cdk.NextjsBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "build_command": "buildCommand",
        "build_path": "buildPath",
        "compression_level": "compressionLevel",
        "environment": "environment",
        "is_placeholder": "isPlaceholder",
        "nextjs_path": "nextjsPath",
        "next_js_path": "nextJsPath",
        "node_env": "nodeEnv",
        "open_next_path": "openNextPath",
        "quiet": "quiet",
        "sharp_layer_arn": "sharpLayerArn",
        "temp_build_dir": "tempBuildDir",
    },
)
class NextjsBaseProps:
    def __init__(
        self,
        *,
        build_command: typing.Optional[builtins.str] = None,
        build_path: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_placeholder: typing.Optional[builtins.bool] = None,
        nextjs_path: typing.Optional[builtins.str] = None,
        next_js_path: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        open_next_path: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
        sharp_layer_arn: typing.Optional[builtins.str] = None,
        temp_build_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Common props shared across NextJS-related CDK constructs.

        :param build_command: Optional value used to install NextJS node dependencies. It defaults to 'npx --yes open-next@latest build'
        :param build_path: The directory to execute ``npm run build`` from. By default, it is ``nextjsPath``. Can be overridden, particularly useful for monorepos where ``build`` is expected to run at the root of the project.
        :param compression_level: 0 - no compression, fastest 9 - maximum compression, slowest. Default: 1
        :param environment: Custom environment variables to pass to the NextJS build and runtime.
        :param is_placeholder: (deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.
        :param nextjs_path: (deprecated) Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.
        :param next_js_path: Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param node_env: Optional value for NODE_ENV during build and runtime.
        :param open_next_path: Relative path to the OpenNext package named ``.open-next`` by default. One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param quiet: Less build output.
        :param sharp_layer_arn: Optional arn for the sharp lambda layer. If omitted, the layer will be created.
        :param temp_build_dir: Directory to store temporary build files in. Defaults to os.tmpdir().
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ec93c51d94a84969d4927564d798c246740d1434e27b5b273de694bcb20eb7)
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument build_path", value=build_path, expected_type=type_hints["build_path"])
            check_type(argname="argument compression_level", value=compression_level, expected_type=type_hints["compression_level"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument is_placeholder", value=is_placeholder, expected_type=type_hints["is_placeholder"])
            check_type(argname="argument nextjs_path", value=nextjs_path, expected_type=type_hints["nextjs_path"])
            check_type(argname="argument next_js_path", value=next_js_path, expected_type=type_hints["next_js_path"])
            check_type(argname="argument node_env", value=node_env, expected_type=type_hints["node_env"])
            check_type(argname="argument open_next_path", value=open_next_path, expected_type=type_hints["open_next_path"])
            check_type(argname="argument quiet", value=quiet, expected_type=type_hints["quiet"])
            check_type(argname="argument sharp_layer_arn", value=sharp_layer_arn, expected_type=type_hints["sharp_layer_arn"])
            check_type(argname="argument temp_build_dir", value=temp_build_dir, expected_type=type_hints["temp_build_dir"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_command is not None:
            self._values["build_command"] = build_command
        if build_path is not None:
            self._values["build_path"] = build_path
        if compression_level is not None:
            self._values["compression_level"] = compression_level
        if environment is not None:
            self._values["environment"] = environment
        if is_placeholder is not None:
            self._values["is_placeholder"] = is_placeholder
        if nextjs_path is not None:
            self._values["nextjs_path"] = nextjs_path
        if next_js_path is not None:
            self._values["next_js_path"] = next_js_path
        if node_env is not None:
            self._values["node_env"] = node_env
        if open_next_path is not None:
            self._values["open_next_path"] = open_next_path
        if quiet is not None:
            self._values["quiet"] = quiet
        if sharp_layer_arn is not None:
            self._values["sharp_layer_arn"] = sharp_layer_arn
        if temp_build_dir is not None:
            self._values["temp_build_dir"] = temp_build_dir

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''Optional value used to install NextJS node dependencies.

        It defaults to 'npx --yes open-next@latest build'
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_path(self) -> typing.Optional[builtins.str]:
        '''The directory to execute ``npm run build`` from.

        By default, it is ``nextjsPath``.
        Can be overridden, particularly useful for monorepos where ``build`` is expected to run
        at the root of the project.
        '''
        result = self._values.get("build_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression_level(self) -> typing.Optional[jsii.Number]:
        '''0 - no compression, fastest 9 - maximum compression, slowest.

        :default: 1
        '''
        result = self._values.get("compression_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom environment variables to pass to the NextJS build and runtime.'''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def is_placeholder(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.

        :deprecated: use ``openNextPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("is_placeholder")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def nextjs_path(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.

        :deprecated: use ``nextJsPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("nextjs_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_js_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("next_js_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_env(self) -> typing.Optional[builtins.str]:
        '''Optional value for NODE_ENV during build and runtime.'''
        result = self._values.get("node_env")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_next_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the OpenNext package named ``.open-next`` by default.

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("open_next_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quiet(self) -> typing.Optional[builtins.bool]:
        '''Less build output.'''
        result = self._values.get("quiet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sharp_layer_arn(self) -> typing.Optional[builtins.str]:
        '''Optional arn for the sharp lambda layer.

        If omitted, the layer will be created.
        '''
        result = self._values.get("sharp_layer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_build_dir(self) -> typing.Optional[builtins.str]:
        '''Directory to store temporary build files in.

        Defaults to os.tmpdir().
        '''
        result = self._values.get("temp_build_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NextjsBuild(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="open-next-cdk.NextjsBuild",
):
    '''Represents a built NextJS application.

    This construct runs ``npm build`` in standalone output mode inside your ``nextjsPath``.
    This construct can be used by higher level constructs or used directly.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        build_command: typing.Optional[builtins.str] = None,
        build_path: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_placeholder: typing.Optional[builtins.bool] = None,
        nextjs_path: typing.Optional[builtins.str] = None,
        next_js_path: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        open_next_path: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
        sharp_layer_arn: typing.Optional[builtins.str] = None,
        temp_build_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param build_command: Optional value used to install NextJS node dependencies. It defaults to 'npx --yes open-next@latest build'
        :param build_path: The directory to execute ``npm run build`` from. By default, it is ``nextjsPath``. Can be overridden, particularly useful for monorepos where ``build`` is expected to run at the root of the project.
        :param compression_level: 0 - no compression, fastest 9 - maximum compression, slowest. Default: 1
        :param environment: Custom environment variables to pass to the NextJS build and runtime.
        :param is_placeholder: (deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.
        :param nextjs_path: (deprecated) Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.
        :param next_js_path: Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param node_env: Optional value for NODE_ENV during build and runtime.
        :param open_next_path: Relative path to the OpenNext package named ``.open-next`` by default. One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param quiet: Less build output.
        :param sharp_layer_arn: Optional arn for the sharp lambda layer. If omitted, the layer will be created.
        :param temp_build_dir: Directory to store temporary build files in. Defaults to os.tmpdir().
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9d80a1ea2ef48546f31aefe8a0be85957df79feb9c7df063a9bd3bbdb52d29)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NextjsBuildProps(
            build_command=build_command,
            build_path=build_path,
            compression_level=compression_level,
            environment=environment,
            is_placeholder=is_placeholder,
            nextjs_path=nextjs_path,
            next_js_path=next_js_path,
            node_env=node_env,
            open_next_path=open_next_path,
            quiet=quiet,
            sharp_layer_arn=sharp_layer_arn,
            temp_build_dir=temp_build_dir,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="readPublicFileList")
    def read_public_file_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "readPublicFileList", []))

    @builtins.property
    @jsii.member(jsii_name="openNextPath")
    def open_next_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "openNextPath"))

    @builtins.property
    @jsii.member(jsii_name="nextImageFnDir")
    def next_image_fn_dir(self) -> builtins.str:
        '''Contains function for processessing image requests.

        Should be arm64.
        '''
        return typing.cast(builtins.str, jsii.get(self, "nextImageFnDir"))

    @next_image_fn_dir.setter
    def next_image_fn_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a912e3a54c42492f785a9d372ca82465f6ff9b69009e400d852c360b67f76f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextImageFnDir", value)

    @builtins.property
    @jsii.member(jsii_name="nextServerFnDir")
    def next_server_fn_dir(self) -> builtins.str:
        '''Contains server code and dependencies.'''
        return typing.cast(builtins.str, jsii.get(self, "nextServerFnDir"))

    @next_server_fn_dir.setter
    def next_server_fn_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30ace1ca8dd1b78da960b5d20cce2b57b05dee340f64f297db89f59417ee6478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextServerFnDir", value)

    @builtins.property
    @jsii.member(jsii_name="nextStaticDir")
    def next_static_dir(self) -> builtins.str:
        '''Static files containing client-side code.'''
        return typing.cast(builtins.str, jsii.get(self, "nextStaticDir"))

    @next_static_dir.setter
    def next_static_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__235fe242c6d21213443c40d48046f33d758998c7da50aa59cd543cabf16fa5f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextStaticDir", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "NextjsBuildProps":
        return typing.cast("NextjsBuildProps", jsii.get(self, "props"))

    @props.setter
    def props(self, value: "NextjsBuildProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49f5d5dbc76a5b36128a18058a86db2c28f8d473a64027f62353357ab989fd97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)

    @builtins.property
    @jsii.member(jsii_name="nextMiddlewareFnDir")
    def next_middleware_fn_dir(self) -> typing.Optional[builtins.str]:
        '''Contains code for middleware.

        Not currently used.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextMiddlewareFnDir"))

    @next_middleware_fn_dir.setter
    def next_middleware_fn_dir(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa960e2f5007cf0398b02a4d3d88cea2967cc0b60b1817da2432a756414ff24e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextMiddlewareFnDir", value)


@jsii.data_type(
    jsii_type="open-next-cdk.NextjsBuildProps",
    jsii_struct_bases=[NextjsBaseProps],
    name_mapping={
        "build_command": "buildCommand",
        "build_path": "buildPath",
        "compression_level": "compressionLevel",
        "environment": "environment",
        "is_placeholder": "isPlaceholder",
        "nextjs_path": "nextjsPath",
        "next_js_path": "nextJsPath",
        "node_env": "nodeEnv",
        "open_next_path": "openNextPath",
        "quiet": "quiet",
        "sharp_layer_arn": "sharpLayerArn",
        "temp_build_dir": "tempBuildDir",
    },
)
class NextjsBuildProps(NextjsBaseProps):
    def __init__(
        self,
        *,
        build_command: typing.Optional[builtins.str] = None,
        build_path: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_placeholder: typing.Optional[builtins.bool] = None,
        nextjs_path: typing.Optional[builtins.str] = None,
        next_js_path: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        open_next_path: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
        sharp_layer_arn: typing.Optional[builtins.str] = None,
        temp_build_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param build_command: Optional value used to install NextJS node dependencies. It defaults to 'npx --yes open-next@latest build'
        :param build_path: The directory to execute ``npm run build`` from. By default, it is ``nextjsPath``. Can be overridden, particularly useful for monorepos where ``build`` is expected to run at the root of the project.
        :param compression_level: 0 - no compression, fastest 9 - maximum compression, slowest. Default: 1
        :param environment: Custom environment variables to pass to the NextJS build and runtime.
        :param is_placeholder: (deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.
        :param nextjs_path: (deprecated) Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.
        :param next_js_path: Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param node_env: Optional value for NODE_ENV during build and runtime.
        :param open_next_path: Relative path to the OpenNext package named ``.open-next`` by default. One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param quiet: Less build output.
        :param sharp_layer_arn: Optional arn for the sharp lambda layer. If omitted, the layer will be created.
        :param temp_build_dir: Directory to store temporary build files in. Defaults to os.tmpdir().
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f76be60c8fe54d3eedb4892d9d0ad058323cadecd0198fd368c07f2d16541ce)
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument build_path", value=build_path, expected_type=type_hints["build_path"])
            check_type(argname="argument compression_level", value=compression_level, expected_type=type_hints["compression_level"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument is_placeholder", value=is_placeholder, expected_type=type_hints["is_placeholder"])
            check_type(argname="argument nextjs_path", value=nextjs_path, expected_type=type_hints["nextjs_path"])
            check_type(argname="argument next_js_path", value=next_js_path, expected_type=type_hints["next_js_path"])
            check_type(argname="argument node_env", value=node_env, expected_type=type_hints["node_env"])
            check_type(argname="argument open_next_path", value=open_next_path, expected_type=type_hints["open_next_path"])
            check_type(argname="argument quiet", value=quiet, expected_type=type_hints["quiet"])
            check_type(argname="argument sharp_layer_arn", value=sharp_layer_arn, expected_type=type_hints["sharp_layer_arn"])
            check_type(argname="argument temp_build_dir", value=temp_build_dir, expected_type=type_hints["temp_build_dir"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_command is not None:
            self._values["build_command"] = build_command
        if build_path is not None:
            self._values["build_path"] = build_path
        if compression_level is not None:
            self._values["compression_level"] = compression_level
        if environment is not None:
            self._values["environment"] = environment
        if is_placeholder is not None:
            self._values["is_placeholder"] = is_placeholder
        if nextjs_path is not None:
            self._values["nextjs_path"] = nextjs_path
        if next_js_path is not None:
            self._values["next_js_path"] = next_js_path
        if node_env is not None:
            self._values["node_env"] = node_env
        if open_next_path is not None:
            self._values["open_next_path"] = open_next_path
        if quiet is not None:
            self._values["quiet"] = quiet
        if sharp_layer_arn is not None:
            self._values["sharp_layer_arn"] = sharp_layer_arn
        if temp_build_dir is not None:
            self._values["temp_build_dir"] = temp_build_dir

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''Optional value used to install NextJS node dependencies.

        It defaults to 'npx --yes open-next@latest build'
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_path(self) -> typing.Optional[builtins.str]:
        '''The directory to execute ``npm run build`` from.

        By default, it is ``nextjsPath``.
        Can be overridden, particularly useful for monorepos where ``build`` is expected to run
        at the root of the project.
        '''
        result = self._values.get("build_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression_level(self) -> typing.Optional[jsii.Number]:
        '''0 - no compression, fastest 9 - maximum compression, slowest.

        :default: 1
        '''
        result = self._values.get("compression_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom environment variables to pass to the NextJS build and runtime.'''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def is_placeholder(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.

        :deprecated: use ``openNextPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("is_placeholder")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def nextjs_path(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.

        :deprecated: use ``nextJsPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("nextjs_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_js_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("next_js_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_env(self) -> typing.Optional[builtins.str]:
        '''Optional value for NODE_ENV during build and runtime.'''
        result = self._values.get("node_env")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_next_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the OpenNext package named ``.open-next`` by default.

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("open_next_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quiet(self) -> typing.Optional[builtins.bool]:
        '''Less build output.'''
        result = self._values.get("quiet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sharp_layer_arn(self) -> typing.Optional[builtins.str]:
        '''Optional arn for the sharp lambda layer.

        If omitted, the layer will be created.
        '''
        result = self._values.get("sharp_layer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_build_dir(self) -> typing.Optional[builtins.str]:
        '''Directory to store temporary build files in.

        Defaults to os.tmpdir().
        '''
        result = self._values.get("temp_build_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsBuildProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="open-next-cdk.NextjsCachePolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_cache_policy": "imageCachePolicy",
        "lambda_cache_policy": "lambdaCachePolicy",
        "static_cache_policy": "staticCachePolicy",
        "static_client_max_age_default": "staticClientMaxAgeDefault",
    },
)
class NextjsCachePolicyProps:
    def __init__(
        self,
        *,
        image_cache_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy] = None,
        lambda_cache_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy] = None,
        static_cache_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy] = None,
        static_client_max_age_default: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param image_cache_policy: 
        :param lambda_cache_policy: 
        :param static_cache_policy: 
        :param static_client_max_age_default: Cache-control max-age default for static assets (/_next/*). Default: 30 days.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5beab1443400ede62a629403d54e15d235c8d7e5e8675ca115a14d1897afe74a)
            check_type(argname="argument image_cache_policy", value=image_cache_policy, expected_type=type_hints["image_cache_policy"])
            check_type(argname="argument lambda_cache_policy", value=lambda_cache_policy, expected_type=type_hints["lambda_cache_policy"])
            check_type(argname="argument static_cache_policy", value=static_cache_policy, expected_type=type_hints["static_cache_policy"])
            check_type(argname="argument static_client_max_age_default", value=static_client_max_age_default, expected_type=type_hints["static_client_max_age_default"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if image_cache_policy is not None:
            self._values["image_cache_policy"] = image_cache_policy
        if lambda_cache_policy is not None:
            self._values["lambda_cache_policy"] = lambda_cache_policy
        if static_cache_policy is not None:
            self._values["static_cache_policy"] = static_cache_policy
        if static_client_max_age_default is not None:
            self._values["static_client_max_age_default"] = static_client_max_age_default

    @builtins.property
    def image_cache_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy]:
        result = self._values.get("image_cache_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy], result)

    @builtins.property
    def lambda_cache_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy]:
        result = self._values.get("lambda_cache_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy], result)

    @builtins.property
    def static_cache_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy]:
        result = self._values.get("static_cache_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy], result)

    @builtins.property
    def static_client_max_age_default(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''Cache-control max-age default for static assets (/_next/*).

        Default: 30 days.
        '''
        result = self._values.get("static_client_max_age_default")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsCachePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="open-next-cdk.NextjsDefaultsProps",
    jsii_struct_bases=[],
    name_mapping={
        "asset_deployment": "assetDeployment",
        "distribution": "distribution",
        "lambda_": "lambda",
    },
)
class NextjsDefaultsProps:
    def __init__(
        self,
        *,
        asset_deployment: typing.Any = None,
        distribution: typing.Any = None,
        lambda_: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Defaults for created resources.

        Why ``any``? see https://github.com/aws/jsii/issues/2901

        :param asset_deployment: Override static file deployment settings.
        :param distribution: Override CloudFront distribution settings. These properties should all be optional but cannot be due to a limitation in jsii.
        :param lambda_: Override server lambda function settings.
        '''
        if isinstance(lambda_, dict):
            lambda_ = _aws_cdk_aws_lambda_ceddda9d.FunctionOptions(**lambda_)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3281f9f114cf2d3432895c9f007c24b74abbc116d63e7a103aa11263e265642)
            check_type(argname="argument asset_deployment", value=asset_deployment, expected_type=type_hints["asset_deployment"])
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asset_deployment is not None:
            self._values["asset_deployment"] = asset_deployment
        if distribution is not None:
            self._values["distribution"] = distribution
        if lambda_ is not None:
            self._values["lambda_"] = lambda_

    @builtins.property
    def asset_deployment(self) -> typing.Any:
        '''Override static file deployment settings.'''
        result = self._values.get("asset_deployment")
        return typing.cast(typing.Any, result)

    @builtins.property
    def distribution(self) -> typing.Any:
        '''Override CloudFront distribution settings.

        These properties should all be optional but cannot be due to a limitation in jsii.
        '''
        result = self._values.get("distribution")
        return typing.cast(typing.Any, result)

    @builtins.property
    def lambda_(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions]:
        '''Override server lambda function settings.'''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsDefaultsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NextjsDistribution(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="open-next-cdk.NextjsDistribution",
):
    '''Create a CloudFront distribution to serve a Next.js application.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_opt_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        next_build: NextjsBuild,
        server_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        static_assets_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        cache_policies: typing.Optional[typing.Union[NextjsCachePolicyProps, typing.Dict[builtins.str, typing.Any]]] = None,
        cdk: typing.Optional[typing.Union["NextjsDistributionCdkProps", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_domain: typing.Optional[typing.Union[builtins.str, typing.Union["NextjsDomainProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        function_url_auth_type: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionUrlAuthType] = None,
        origin_request_policies: typing.Optional[typing.Union["NextjsOriginRequestPolicyProps", typing.Dict[builtins.str, typing.Any]]] = None,
        stack_prefix: typing.Optional[builtins.str] = None,
        stage_name: typing.Optional[builtins.str] = None,
        build_command: typing.Optional[builtins.str] = None,
        build_path: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_placeholder: typing.Optional[builtins.bool] = None,
        nextjs_path: typing.Optional[builtins.str] = None,
        next_js_path: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        open_next_path: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
        sharp_layer_arn: typing.Optional[builtins.str] = None,
        temp_build_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param image_opt_function: Lambda function to optimize images. Must be provided if you want to serve dynamic requests.
        :param next_build: Built NextJS app.
        :param server_function: Lambda function to route all non-static requests to. Must be provided if you want to serve dynamic requests.
        :param static_assets_bucket: Bucket containing static assets. Must be provided if you want to serve static files.
        :param cache_policies: Override the default CloudFront cache policies created internally.
        :param cdk: Overrides for created CDK resources.
        :param custom_domain: The customDomain for this website. Supports domains that are hosted either on `Route 53 <https://aws.amazon.com/route53/>`_ or externally. Note that you can also migrate externally hosted domains to Route 53 by `following this guide <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/MigratingDNS.html>`_.
        :param function_url_auth_type: Override lambda function url auth type. Default: "NONE"
        :param origin_request_policies: Override the default CloudFront origin request policies created internally.
        :param stack_prefix: Optional value to prefix the edge function stack It defaults to "Nextjs".
        :param stage_name: Include the name of your deployment stage if present. Used to name the edge functions stack. Required if using SST.
        :param build_command: Optional value used to install NextJS node dependencies. It defaults to 'npx --yes open-next@latest build'
        :param build_path: The directory to execute ``npm run build`` from. By default, it is ``nextjsPath``. Can be overridden, particularly useful for monorepos where ``build`` is expected to run at the root of the project.
        :param compression_level: 0 - no compression, fastest 9 - maximum compression, slowest. Default: 1
        :param environment: Custom environment variables to pass to the NextJS build and runtime.
        :param is_placeholder: (deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.
        :param nextjs_path: (deprecated) Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.
        :param next_js_path: Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param node_env: Optional value for NODE_ENV during build and runtime.
        :param open_next_path: Relative path to the OpenNext package named ``.open-next`` by default. One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param quiet: Less build output.
        :param sharp_layer_arn: Optional arn for the sharp lambda layer. If omitted, the layer will be created.
        :param temp_build_dir: Directory to store temporary build files in. Defaults to os.tmpdir().
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96429686a12d62c6a68e5becfb0bb1fee7ad2eb8691d4394d55362a261b4c253)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NextjsDistributionProps(
            image_opt_function=image_opt_function,
            next_build=next_build,
            server_function=server_function,
            static_assets_bucket=static_assets_bucket,
            cache_policies=cache_policies,
            cdk=cdk,
            custom_domain=custom_domain,
            function_url_auth_type=function_url_auth_type,
            origin_request_policies=origin_request_policies,
            stack_prefix=stack_prefix,
            stage_name=stage_name,
            build_command=build_command,
            build_path=build_path,
            compression_level=compression_level,
            environment=environment,
            is_placeholder=is_placeholder,
            nextjs_path=nextjs_path,
            next_js_path=next_js_path,
            node_env=node_env,
            open_next_path=open_next_path,
            quiet=quiet,
            sharp_layer_arn=sharp_layer_arn,
            temp_build_dir=temp_build_dir,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="lookupHostedZone")
    def _lookup_hosted_zone(
        self,
    ) -> typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone]:
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone], jsii.invoke(self, "lookupHostedZone", []))

    @jsii.member(jsii_name="validateCustomDomainSettings")
    def _validate_custom_domain_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "validateCustomDomainSettings", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="fallbackOriginRequestPolicyProps")
    def fallback_origin_request_policy_props(
        cls,
    ) -> _aws_cdk_aws_cloudfront_ceddda9d.OriginRequestPolicyProps:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.OriginRequestPolicyProps, jsii.sget(cls, "fallbackOriginRequestPolicyProps"))

    @fallback_origin_request_policy_props.setter # type: ignore[no-redef]
    def fallback_origin_request_policy_props(
        cls,
        value: _aws_cdk_aws_cloudfront_ceddda9d.OriginRequestPolicyProps,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4f3e3041a6f9373eb4e476ca58b65574cd2fc90f10e0fe83eb833b55aa4c4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "fallbackOriginRequestPolicyProps", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="imageCachePolicyProps")
    def image_cache_policy_props(
        cls,
    ) -> _aws_cdk_aws_cloudfront_ceddda9d.CachePolicyProps:  # pyright: ignore [reportGeneralTypeIssues]
        '''The default CloudFront cache policy properties for images.'''
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.CachePolicyProps, jsii.sget(cls, "imageCachePolicyProps"))

    @image_cache_policy_props.setter # type: ignore[no-redef]
    def image_cache_policy_props(
        cls,
        value: _aws_cdk_aws_cloudfront_ceddda9d.CachePolicyProps,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6adf7f3d1cd4d7aa682ec6290c2383de65e020a5feb9c92694fa04db3bd04d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "imageCachePolicyProps", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="imageOptimizationOriginRequestPolicyProps")
    def image_optimization_origin_request_policy_props(
        cls,
    ) -> _aws_cdk_aws_cloudfront_ceddda9d.OriginRequestPolicyProps:  # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.OriginRequestPolicyProps, jsii.sget(cls, "imageOptimizationOriginRequestPolicyProps"))

    @image_optimization_origin_request_policy_props.setter # type: ignore[no-redef]
    def image_optimization_origin_request_policy_props(
        cls,
        value: _aws_cdk_aws_cloudfront_ceddda9d.OriginRequestPolicyProps,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdc609a1f2cd4e3d6079cc5d3384f9c1b9c7a2b83d6b12b6f0f6598f78dfaec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "imageOptimizationOriginRequestPolicyProps", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="lambdaCachePolicyProps")
    def lambda_cache_policy_props(
        cls,
    ) -> _aws_cdk_aws_cloudfront_ceddda9d.CachePolicyProps:  # pyright: ignore [reportGeneralTypeIssues]
        '''The default CloudFront cache policy properties for the Lambda server handler.'''
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.CachePolicyProps, jsii.sget(cls, "lambdaCachePolicyProps"))

    @lambda_cache_policy_props.setter # type: ignore[no-redef]
    def lambda_cache_policy_props(
        cls,
        value: _aws_cdk_aws_cloudfront_ceddda9d.CachePolicyProps,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53820e7c1766a05033b5c7c3f60eac49d0ee4dac99da8aaaf8bcf4251a088708)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "lambdaCachePolicyProps", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="lambdaOriginRequestPolicyProps")
    def lambda_origin_request_policy_props(
        cls,
    ) -> _aws_cdk_aws_cloudfront_ceddda9d.OriginRequestPolicyProps:  # pyright: ignore [reportGeneralTypeIssues]
        '''The default CloudFront lambda origin request policy.'''
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.OriginRequestPolicyProps, jsii.sget(cls, "lambdaOriginRequestPolicyProps"))

    @lambda_origin_request_policy_props.setter # type: ignore[no-redef]
    def lambda_origin_request_policy_props(
        cls,
        value: _aws_cdk_aws_cloudfront_ceddda9d.OriginRequestPolicyProps,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394dfd623fd21e3cefb89b421c91ea0a1bff35a5b3ec33c4cd100e0a601cbd7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "lambdaOriginRequestPolicyProps", value)

    @jsii.python.classproperty
    @jsii.member(jsii_name="staticCachePolicyProps")
    def static_cache_policy_props(
        cls,
    ) -> _aws_cdk_aws_cloudfront_ceddda9d.CachePolicyProps:  # pyright: ignore [reportGeneralTypeIssues]
        '''The default CloudFront cache policy properties for static pages.'''
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.CachePolicyProps, jsii.sget(cls, "staticCachePolicyProps"))

    @static_cache_policy_props.setter # type: ignore[no-redef]
    def static_cache_policy_props(
        cls,
        value: _aws_cdk_aws_cloudfront_ceddda9d.CachePolicyProps,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5966ac5eec38e82772f0bc21221c45e008e0ef917275c9b23d95c0758b7d4eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.sset(cls, "staticCachePolicyProps", value)

    @builtins.property
    @jsii.member(jsii_name="distributionDomain")
    def distribution_domain(self) -> builtins.str:
        '''The domain name of the internally created CloudFront Distribution.'''
        return typing.cast(builtins.str, jsii.get(self, "distributionDomain"))

    @builtins.property
    @jsii.member(jsii_name="distributionId")
    def distribution_id(self) -> builtins.str:
        '''The ID of the internally created CloudFront Distribution.'''
        return typing.cast(builtins.str, jsii.get(self, "distributionId"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        '''The CloudFront URL of the website.'''
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="customDomainName")
    def custom_domain_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDomainName"))

    @builtins.property
    @jsii.member(jsii_name="customDomainUrl")
    def custom_domain_url(self) -> typing.Optional[builtins.str]:
        '''If the custom domain is enabled, this is the URL of the website with the custom domain.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDomainUrl"))

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> _aws_cdk_aws_cloudfront_ceddda9d.Distribution:
        '''The internally created CloudFront ``Distribution`` instance.'''
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.Distribution, jsii.get(self, "distribution"))

    @distribution.setter
    def distribution(
        self,
        value: _aws_cdk_aws_cloudfront_ceddda9d.Distribution,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2003bb843dee56635b51a213e2427a1fcc2c2a3ae2489c5b26a13cb1dd8f12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distribution", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "NextjsDistributionProps":
        return typing.cast("NextjsDistributionProps", jsii.get(self, "props"))

    @_props.setter
    def _props(self, value: "NextjsDistributionProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58db2de3e18d039ca31d58b4ea3e6374131689393d94e20487cb2a876c030565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)

    @builtins.property
    @jsii.member(jsii_name="tempBuildDir")
    def temp_build_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tempBuildDir"))

    @temp_build_dir.setter
    def temp_build_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f1468fcfbed7bd8a91f5d103f84be21de64720a4ffaf85d52d6c44f0de940d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tempBuildDir", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        '''The AWS Certificate Manager certificate for the custom domain.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(
        self,
        value: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84af5c3db1ff8f4257a5a8213acd077dfb03c8e3462adbabbe438b172dcaf2e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="hostedZone")
    def hosted_zone(self) -> typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone]:
        '''The Route 53 hosted zone for the custom domain.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone], jsii.get(self, "hostedZone"))

    @hosted_zone.setter
    def hosted_zone(
        self,
        value: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ef90d5029061afa1511d648182b8db1a888e8a9ec071985f61b9162d9a23bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostedZone", value)


@jsii.data_type(
    jsii_type="open-next-cdk.NextjsDistributionCdkProps",
    jsii_struct_bases=[],
    name_mapping={"distribution": "distribution"},
)
class NextjsDistributionCdkProps:
    def __init__(
        self,
        *,
        distribution: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.DistributionProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param distribution: Pass in a value to override the default settings this construct uses to create the CloudFront ``Distribution`` internally.
        '''
        if isinstance(distribution, dict):
            distribution = _aws_cdk_aws_cloudfront_ceddda9d.DistributionProps(**distribution)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ebd22500c4f1cf1308ccffff6700bea18f32e4ec0fb2bf6fbcf119f0ff1bdda)
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if distribution is not None:
            self._values["distribution"] = distribution

    @builtins.property
    def distribution(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.DistributionProps]:
        '''Pass in a value to override the default settings this construct uses to create the CloudFront ``Distribution`` internally.'''
        result = self._values.get("distribution")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.DistributionProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsDistributionCdkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="open-next-cdk.NextjsDistributionProps",
    jsii_struct_bases=[NextjsBaseProps],
    name_mapping={
        "build_command": "buildCommand",
        "build_path": "buildPath",
        "compression_level": "compressionLevel",
        "environment": "environment",
        "is_placeholder": "isPlaceholder",
        "nextjs_path": "nextjsPath",
        "next_js_path": "nextJsPath",
        "node_env": "nodeEnv",
        "open_next_path": "openNextPath",
        "quiet": "quiet",
        "sharp_layer_arn": "sharpLayerArn",
        "temp_build_dir": "tempBuildDir",
        "image_opt_function": "imageOptFunction",
        "next_build": "nextBuild",
        "server_function": "serverFunction",
        "static_assets_bucket": "staticAssetsBucket",
        "cache_policies": "cachePolicies",
        "cdk": "cdk",
        "custom_domain": "customDomain",
        "function_url_auth_type": "functionUrlAuthType",
        "origin_request_policies": "originRequestPolicies",
        "stack_prefix": "stackPrefix",
        "stage_name": "stageName",
    },
)
class NextjsDistributionProps(NextjsBaseProps):
    def __init__(
        self,
        *,
        build_command: typing.Optional[builtins.str] = None,
        build_path: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_placeholder: typing.Optional[builtins.bool] = None,
        nextjs_path: typing.Optional[builtins.str] = None,
        next_js_path: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        open_next_path: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
        sharp_layer_arn: typing.Optional[builtins.str] = None,
        temp_build_dir: typing.Optional[builtins.str] = None,
        image_opt_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        next_build: NextjsBuild,
        server_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        static_assets_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        cache_policies: typing.Optional[typing.Union[NextjsCachePolicyProps, typing.Dict[builtins.str, typing.Any]]] = None,
        cdk: typing.Optional[typing.Union[NextjsDistributionCdkProps, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_domain: typing.Optional[typing.Union[builtins.str, typing.Union["NextjsDomainProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        function_url_auth_type: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionUrlAuthType] = None,
        origin_request_policies: typing.Optional[typing.Union["NextjsOriginRequestPolicyProps", typing.Dict[builtins.str, typing.Any]]] = None,
        stack_prefix: typing.Optional[builtins.str] = None,
        stage_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param build_command: Optional value used to install NextJS node dependencies. It defaults to 'npx --yes open-next@latest build'
        :param build_path: The directory to execute ``npm run build`` from. By default, it is ``nextjsPath``. Can be overridden, particularly useful for monorepos where ``build`` is expected to run at the root of the project.
        :param compression_level: 0 - no compression, fastest 9 - maximum compression, slowest. Default: 1
        :param environment: Custom environment variables to pass to the NextJS build and runtime.
        :param is_placeholder: (deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.
        :param nextjs_path: (deprecated) Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.
        :param next_js_path: Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param node_env: Optional value for NODE_ENV during build and runtime.
        :param open_next_path: Relative path to the OpenNext package named ``.open-next`` by default. One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param quiet: Less build output.
        :param sharp_layer_arn: Optional arn for the sharp lambda layer. If omitted, the layer will be created.
        :param temp_build_dir: Directory to store temporary build files in. Defaults to os.tmpdir().
        :param image_opt_function: Lambda function to optimize images. Must be provided if you want to serve dynamic requests.
        :param next_build: Built NextJS app.
        :param server_function: Lambda function to route all non-static requests to. Must be provided if you want to serve dynamic requests.
        :param static_assets_bucket: Bucket containing static assets. Must be provided if you want to serve static files.
        :param cache_policies: Override the default CloudFront cache policies created internally.
        :param cdk: Overrides for created CDK resources.
        :param custom_domain: The customDomain for this website. Supports domains that are hosted either on `Route 53 <https://aws.amazon.com/route53/>`_ or externally. Note that you can also migrate externally hosted domains to Route 53 by `following this guide <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/MigratingDNS.html>`_.
        :param function_url_auth_type: Override lambda function url auth type. Default: "NONE"
        :param origin_request_policies: Override the default CloudFront origin request policies created internally.
        :param stack_prefix: Optional value to prefix the edge function stack It defaults to "Nextjs".
        :param stage_name: Include the name of your deployment stage if present. Used to name the edge functions stack. Required if using SST.
        '''
        if isinstance(cache_policies, dict):
            cache_policies = NextjsCachePolicyProps(**cache_policies)
        if isinstance(cdk, dict):
            cdk = NextjsDistributionCdkProps(**cdk)
        if isinstance(origin_request_policies, dict):
            origin_request_policies = NextjsOriginRequestPolicyProps(**origin_request_policies)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b78b297e19da3fbc794e6c49aae016184b97ec8bc8d7a0bde99ac5866d11dc)
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument build_path", value=build_path, expected_type=type_hints["build_path"])
            check_type(argname="argument compression_level", value=compression_level, expected_type=type_hints["compression_level"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument is_placeholder", value=is_placeholder, expected_type=type_hints["is_placeholder"])
            check_type(argname="argument nextjs_path", value=nextjs_path, expected_type=type_hints["nextjs_path"])
            check_type(argname="argument next_js_path", value=next_js_path, expected_type=type_hints["next_js_path"])
            check_type(argname="argument node_env", value=node_env, expected_type=type_hints["node_env"])
            check_type(argname="argument open_next_path", value=open_next_path, expected_type=type_hints["open_next_path"])
            check_type(argname="argument quiet", value=quiet, expected_type=type_hints["quiet"])
            check_type(argname="argument sharp_layer_arn", value=sharp_layer_arn, expected_type=type_hints["sharp_layer_arn"])
            check_type(argname="argument temp_build_dir", value=temp_build_dir, expected_type=type_hints["temp_build_dir"])
            check_type(argname="argument image_opt_function", value=image_opt_function, expected_type=type_hints["image_opt_function"])
            check_type(argname="argument next_build", value=next_build, expected_type=type_hints["next_build"])
            check_type(argname="argument server_function", value=server_function, expected_type=type_hints["server_function"])
            check_type(argname="argument static_assets_bucket", value=static_assets_bucket, expected_type=type_hints["static_assets_bucket"])
            check_type(argname="argument cache_policies", value=cache_policies, expected_type=type_hints["cache_policies"])
            check_type(argname="argument cdk", value=cdk, expected_type=type_hints["cdk"])
            check_type(argname="argument custom_domain", value=custom_domain, expected_type=type_hints["custom_domain"])
            check_type(argname="argument function_url_auth_type", value=function_url_auth_type, expected_type=type_hints["function_url_auth_type"])
            check_type(argname="argument origin_request_policies", value=origin_request_policies, expected_type=type_hints["origin_request_policies"])
            check_type(argname="argument stack_prefix", value=stack_prefix, expected_type=type_hints["stack_prefix"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_opt_function": image_opt_function,
            "next_build": next_build,
            "server_function": server_function,
            "static_assets_bucket": static_assets_bucket,
        }
        if build_command is not None:
            self._values["build_command"] = build_command
        if build_path is not None:
            self._values["build_path"] = build_path
        if compression_level is not None:
            self._values["compression_level"] = compression_level
        if environment is not None:
            self._values["environment"] = environment
        if is_placeholder is not None:
            self._values["is_placeholder"] = is_placeholder
        if nextjs_path is not None:
            self._values["nextjs_path"] = nextjs_path
        if next_js_path is not None:
            self._values["next_js_path"] = next_js_path
        if node_env is not None:
            self._values["node_env"] = node_env
        if open_next_path is not None:
            self._values["open_next_path"] = open_next_path
        if quiet is not None:
            self._values["quiet"] = quiet
        if sharp_layer_arn is not None:
            self._values["sharp_layer_arn"] = sharp_layer_arn
        if temp_build_dir is not None:
            self._values["temp_build_dir"] = temp_build_dir
        if cache_policies is not None:
            self._values["cache_policies"] = cache_policies
        if cdk is not None:
            self._values["cdk"] = cdk
        if custom_domain is not None:
            self._values["custom_domain"] = custom_domain
        if function_url_auth_type is not None:
            self._values["function_url_auth_type"] = function_url_auth_type
        if origin_request_policies is not None:
            self._values["origin_request_policies"] = origin_request_policies
        if stack_prefix is not None:
            self._values["stack_prefix"] = stack_prefix
        if stage_name is not None:
            self._values["stage_name"] = stage_name

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''Optional value used to install NextJS node dependencies.

        It defaults to 'npx --yes open-next@latest build'
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_path(self) -> typing.Optional[builtins.str]:
        '''The directory to execute ``npm run build`` from.

        By default, it is ``nextjsPath``.
        Can be overridden, particularly useful for monorepos where ``build`` is expected to run
        at the root of the project.
        '''
        result = self._values.get("build_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression_level(self) -> typing.Optional[jsii.Number]:
        '''0 - no compression, fastest 9 - maximum compression, slowest.

        :default: 1
        '''
        result = self._values.get("compression_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom environment variables to pass to the NextJS build and runtime.'''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def is_placeholder(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.

        :deprecated: use ``openNextPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("is_placeholder")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def nextjs_path(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.

        :deprecated: use ``nextJsPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("nextjs_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_js_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("next_js_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_env(self) -> typing.Optional[builtins.str]:
        '''Optional value for NODE_ENV during build and runtime.'''
        result = self._values.get("node_env")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_next_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the OpenNext package named ``.open-next`` by default.

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("open_next_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quiet(self) -> typing.Optional[builtins.bool]:
        '''Less build output.'''
        result = self._values.get("quiet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sharp_layer_arn(self) -> typing.Optional[builtins.str]:
        '''Optional arn for the sharp lambda layer.

        If omitted, the layer will be created.
        '''
        result = self._values.get("sharp_layer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_build_dir(self) -> typing.Optional[builtins.str]:
        '''Directory to store temporary build files in.

        Defaults to os.tmpdir().
        '''
        result = self._values.get("temp_build_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_opt_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''Lambda function to optimize images.

        Must be provided if you want to serve dynamic requests.
        '''
        result = self._values.get("image_opt_function")
        assert result is not None, "Required property 'image_opt_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    @builtins.property
    def next_build(self) -> NextjsBuild:
        '''Built NextJS app.'''
        result = self._values.get("next_build")
        assert result is not None, "Required property 'next_build' is missing"
        return typing.cast(NextjsBuild, result)

    @builtins.property
    def server_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''Lambda function to route all non-static requests to.

        Must be provided if you want to serve dynamic requests.
        '''
        result = self._values.get("server_function")
        assert result is not None, "Required property 'server_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    @builtins.property
    def static_assets_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''Bucket containing static assets.

        Must be provided if you want to serve static files.
        '''
        result = self._values.get("static_assets_bucket")
        assert result is not None, "Required property 'static_assets_bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def cache_policies(self) -> typing.Optional[NextjsCachePolicyProps]:
        '''Override the default CloudFront cache policies created internally.'''
        result = self._values.get("cache_policies")
        return typing.cast(typing.Optional[NextjsCachePolicyProps], result)

    @builtins.property
    def cdk(self) -> typing.Optional[NextjsDistributionCdkProps]:
        '''Overrides for created CDK resources.'''
        result = self._values.get("cdk")
        return typing.cast(typing.Optional[NextjsDistributionCdkProps], result)

    @builtins.property
    def custom_domain(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "NextjsDomainProps"]]:
        '''The customDomain for this website. Supports domains that are hosted either on `Route 53 <https://aws.amazon.com/route53/>`_ or externally.

        Note that you can also migrate externally hosted domains to Route 53 by
        `following this guide <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/MigratingDNS.html>`_.

        Example::

            new NextjsDistribution(this, "Dist", {
              customDomain: "domain.com",
            });
            
            new NextjsDistribution(this, "Dist", {
              customDomain: {
                domainName: "domain.com",
                domainAlias: "www.domain.com",
                hostedZone: "domain.com"
              },
            });
        '''
        result = self._values.get("custom_domain")
        return typing.cast(typing.Optional[typing.Union[builtins.str, "NextjsDomainProps"]], result)

    @builtins.property
    def function_url_auth_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionUrlAuthType]:
        '''Override lambda function url auth type.

        :default: "NONE"
        '''
        result = self._values.get("function_url_auth_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionUrlAuthType], result)

    @builtins.property
    def origin_request_policies(
        self,
    ) -> typing.Optional["NextjsOriginRequestPolicyProps"]:
        '''Override the default CloudFront origin request policies created internally.'''
        result = self._values.get("origin_request_policies")
        return typing.cast(typing.Optional["NextjsOriginRequestPolicyProps"], result)

    @builtins.property
    def stack_prefix(self) -> typing.Optional[builtins.str]:
        '''Optional value to prefix the edge function stack It defaults to "Nextjs".'''
        result = self._values.get("stack_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''Include the name of your deployment stage if present.

        Used to name the edge functions stack.
        Required if using SST.
        '''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsDistributionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="open-next-cdk.NextjsDomainProps",
    jsii_struct_bases=[BaseSiteDomainProps],
    name_mapping={
        "domain_name": "domainName",
        "alternate_names": "alternateNames",
        "certificate": "certificate",
        "domain_alias": "domainAlias",
        "hosted_zone": "hostedZone",
        "is_external_domain": "isExternalDomain",
    },
)
class NextjsDomainProps(BaseSiteDomainProps):
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        alternate_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        domain_alias: typing.Optional[builtins.str] = None,
        hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
        is_external_domain: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param domain_name: The domain to be assigned to the website URL (ie. domain.com). Supports domains that are hosted either on `Route 53 <https://aws.amazon.com/route53/>`_ or externally.
        :param alternate_names: Specify additional names that should route to the Cloudfront Distribution. Note, certificates for these names will not be automatically generated so the ``certificate`` option must be specified.
        :param certificate: Import the certificate for the domain. By default, SST will create a certificate with the domain name. The certificate will be created in the ``us-east-1``(N. Virginia) region as required by AWS CloudFront. Set this option if you have an existing certificate in the ``us-east-1`` region in AWS Certificate Manager you want to use.
        :param domain_alias: An alternative domain to be assigned to the website URL. Visitors to the alias will be redirected to the main domain. (ie. ``www.domain.com``). Use this to create a ``www.`` version of your domain and redirect visitors to the root domain.
        :param hosted_zone: Import the underlying Route 53 hosted zone.
        :param is_external_domain: Set this option if the domain is not hosted on Amazon Route 53.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2f0e8acb48dbe67528492a569aeedd131e85a109a90d1a0fb6b1ce7dc3d365)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument alternate_names", value=alternate_names, expected_type=type_hints["alternate_names"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument domain_alias", value=domain_alias, expected_type=type_hints["domain_alias"])
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
            check_type(argname="argument is_external_domain", value=is_external_domain, expected_type=type_hints["is_external_domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
        }
        if alternate_names is not None:
            self._values["alternate_names"] = alternate_names
        if certificate is not None:
            self._values["certificate"] = certificate
        if domain_alias is not None:
            self._values["domain_alias"] = domain_alias
        if hosted_zone is not None:
            self._values["hosted_zone"] = hosted_zone
        if is_external_domain is not None:
            self._values["is_external_domain"] = is_external_domain

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''The domain to be assigned to the website URL (ie. domain.com).

        Supports domains that are hosted either on `Route 53 <https://aws.amazon.com/route53/>`_ or externally.
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alternate_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify additional names that should route to the Cloudfront Distribution.

        Note, certificates for these names will not be automatically generated so the ``certificate`` option must be specified.
        '''
        result = self._values.get("alternate_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        '''Import the certificate for the domain.

        By default, SST will create a certificate with the domain name. The certificate will be created in the ``us-east-1``(N. Virginia) region as required by AWS CloudFront.

        Set this option if you have an existing certificate in the ``us-east-1`` region in AWS Certificate Manager you want to use.
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], result)

    @builtins.property
    def domain_alias(self) -> typing.Optional[builtins.str]:
        '''An alternative domain to be assigned to the website URL.

        Visitors to the alias will be redirected to the main domain. (ie. ``www.domain.com``).

        Use this to create a ``www.`` version of your domain and redirect visitors to the root domain.
        '''
        result = self._values.get("domain_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hosted_zone(self) -> typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone]:
        '''Import the underlying Route 53 hosted zone.'''
        result = self._values.get("hosted_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone], result)

    @builtins.property
    def is_external_domain(self) -> typing.Optional[builtins.bool]:
        '''Set this option if the domain is not hosted on Amazon Route 53.'''
        result = self._values.get("is_external_domain")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="open-next-cdk.NextjsLambdaProps",
    jsii_struct_bases=[NextjsBaseProps],
    name_mapping={
        "build_command": "buildCommand",
        "build_path": "buildPath",
        "compression_level": "compressionLevel",
        "environment": "environment",
        "is_placeholder": "isPlaceholder",
        "nextjs_path": "nextjsPath",
        "next_js_path": "nextJsPath",
        "node_env": "nodeEnv",
        "open_next_path": "openNextPath",
        "quiet": "quiet",
        "sharp_layer_arn": "sharpLayerArn",
        "temp_build_dir": "tempBuildDir",
        "next_build": "nextBuild",
        "lambda_": "lambda",
    },
)
class NextjsLambdaProps(NextjsBaseProps):
    def __init__(
        self,
        *,
        build_command: typing.Optional[builtins.str] = None,
        build_path: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_placeholder: typing.Optional[builtins.bool] = None,
        nextjs_path: typing.Optional[builtins.str] = None,
        next_js_path: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        open_next_path: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
        sharp_layer_arn: typing.Optional[builtins.str] = None,
        temp_build_dir: typing.Optional[builtins.str] = None,
        next_build: NextjsBuild,
        lambda_: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param build_command: Optional value used to install NextJS node dependencies. It defaults to 'npx --yes open-next@latest build'
        :param build_path: The directory to execute ``npm run build`` from. By default, it is ``nextjsPath``. Can be overridden, particularly useful for monorepos where ``build`` is expected to run at the root of the project.
        :param compression_level: 0 - no compression, fastest 9 - maximum compression, slowest. Default: 1
        :param environment: Custom environment variables to pass to the NextJS build and runtime.
        :param is_placeholder: (deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.
        :param nextjs_path: (deprecated) Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.
        :param next_js_path: Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param node_env: Optional value for NODE_ENV during build and runtime.
        :param open_next_path: Relative path to the OpenNext package named ``.open-next`` by default. One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param quiet: Less build output.
        :param sharp_layer_arn: Optional arn for the sharp lambda layer. If omitted, the layer will be created.
        :param temp_build_dir: Directory to store temporary build files in. Defaults to os.tmpdir().
        :param next_build: Built nextJS application.
        :param lambda_: Override function properties.
        '''
        if isinstance(lambda_, dict):
            lambda_ = _aws_cdk_aws_lambda_ceddda9d.FunctionOptions(**lambda_)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b398354dc2cfe9832ff6a120234dbe8d3b199fc0b2d5d22bcf7dc901e36569d5)
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument build_path", value=build_path, expected_type=type_hints["build_path"])
            check_type(argname="argument compression_level", value=compression_level, expected_type=type_hints["compression_level"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument is_placeholder", value=is_placeholder, expected_type=type_hints["is_placeholder"])
            check_type(argname="argument nextjs_path", value=nextjs_path, expected_type=type_hints["nextjs_path"])
            check_type(argname="argument next_js_path", value=next_js_path, expected_type=type_hints["next_js_path"])
            check_type(argname="argument node_env", value=node_env, expected_type=type_hints["node_env"])
            check_type(argname="argument open_next_path", value=open_next_path, expected_type=type_hints["open_next_path"])
            check_type(argname="argument quiet", value=quiet, expected_type=type_hints["quiet"])
            check_type(argname="argument sharp_layer_arn", value=sharp_layer_arn, expected_type=type_hints["sharp_layer_arn"])
            check_type(argname="argument temp_build_dir", value=temp_build_dir, expected_type=type_hints["temp_build_dir"])
            check_type(argname="argument next_build", value=next_build, expected_type=type_hints["next_build"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "next_build": next_build,
        }
        if build_command is not None:
            self._values["build_command"] = build_command
        if build_path is not None:
            self._values["build_path"] = build_path
        if compression_level is not None:
            self._values["compression_level"] = compression_level
        if environment is not None:
            self._values["environment"] = environment
        if is_placeholder is not None:
            self._values["is_placeholder"] = is_placeholder
        if nextjs_path is not None:
            self._values["nextjs_path"] = nextjs_path
        if next_js_path is not None:
            self._values["next_js_path"] = next_js_path
        if node_env is not None:
            self._values["node_env"] = node_env
        if open_next_path is not None:
            self._values["open_next_path"] = open_next_path
        if quiet is not None:
            self._values["quiet"] = quiet
        if sharp_layer_arn is not None:
            self._values["sharp_layer_arn"] = sharp_layer_arn
        if temp_build_dir is not None:
            self._values["temp_build_dir"] = temp_build_dir
        if lambda_ is not None:
            self._values["lambda_"] = lambda_

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''Optional value used to install NextJS node dependencies.

        It defaults to 'npx --yes open-next@latest build'
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_path(self) -> typing.Optional[builtins.str]:
        '''The directory to execute ``npm run build`` from.

        By default, it is ``nextjsPath``.
        Can be overridden, particularly useful for monorepos where ``build`` is expected to run
        at the root of the project.
        '''
        result = self._values.get("build_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression_level(self) -> typing.Optional[jsii.Number]:
        '''0 - no compression, fastest 9 - maximum compression, slowest.

        :default: 1
        '''
        result = self._values.get("compression_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom environment variables to pass to the NextJS build and runtime.'''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def is_placeholder(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.

        :deprecated: use ``openNextPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("is_placeholder")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def nextjs_path(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.

        :deprecated: use ``nextJsPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("nextjs_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_js_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("next_js_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_env(self) -> typing.Optional[builtins.str]:
        '''Optional value for NODE_ENV during build and runtime.'''
        result = self._values.get("node_env")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_next_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the OpenNext package named ``.open-next`` by default.

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("open_next_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quiet(self) -> typing.Optional[builtins.bool]:
        '''Less build output.'''
        result = self._values.get("quiet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sharp_layer_arn(self) -> typing.Optional[builtins.str]:
        '''Optional arn for the sharp lambda layer.

        If omitted, the layer will be created.
        '''
        result = self._values.get("sharp_layer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_build_dir(self) -> typing.Optional[builtins.str]:
        '''Directory to store temporary build files in.

        Defaults to os.tmpdir().
        '''
        result = self._values.get("temp_build_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_build(self) -> NextjsBuild:
        '''Built nextJS application.'''
        result = self._values.get("next_build")
        assert result is not None, "Required property 'next_build' is missing"
        return typing.cast(NextjsBuild, result)

    @builtins.property
    def lambda_(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions]:
        '''Override function properties.'''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NextjsLayer(
    _aws_cdk_aws_lambda_ceddda9d.LayerVersion,
    metaclass=jsii.JSIIMeta,
    jsii_type="open-next-cdk.NextjsLayer",
):
    '''Lambda layer for Next.js. Contains Sharp 0.30.0.'''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d1eedb1aeead6789283febfffae0b4de96a8e41458d224f4ffdedbffaf2c9b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NextjsLayerProps()

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="open-next-cdk.NextjsLayerProps",
    jsii_struct_bases=[],
    name_mapping={},
)
class NextjsLayerProps:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsLayerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="open-next-cdk.NextjsOriginRequestPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "fallback_origin_request_policy": "fallbackOriginRequestPolicy",
        "image_optimization_origin_request_policy": "imageOptimizationOriginRequestPolicy",
        "lambda_origin_request_policy": "lambdaOriginRequestPolicy",
    },
)
class NextjsOriginRequestPolicyProps:
    def __init__(
        self,
        *,
        fallback_origin_request_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy] = None,
        image_optimization_origin_request_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy] = None,
        lambda_origin_request_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy] = None,
    ) -> None:
        '''
        :param fallback_origin_request_policy: 
        :param image_optimization_origin_request_policy: 
        :param lambda_origin_request_policy: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b6529cd61a993ba5195a67f3a7a1ddfa195058990804f8623c4880b612ce474)
            check_type(argname="argument fallback_origin_request_policy", value=fallback_origin_request_policy, expected_type=type_hints["fallback_origin_request_policy"])
            check_type(argname="argument image_optimization_origin_request_policy", value=image_optimization_origin_request_policy, expected_type=type_hints["image_optimization_origin_request_policy"])
            check_type(argname="argument lambda_origin_request_policy", value=lambda_origin_request_policy, expected_type=type_hints["lambda_origin_request_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fallback_origin_request_policy is not None:
            self._values["fallback_origin_request_policy"] = fallback_origin_request_policy
        if image_optimization_origin_request_policy is not None:
            self._values["image_optimization_origin_request_policy"] = image_optimization_origin_request_policy
        if lambda_origin_request_policy is not None:
            self._values["lambda_origin_request_policy"] = lambda_origin_request_policy

    @builtins.property
    def fallback_origin_request_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy]:
        result = self._values.get("fallback_origin_request_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy], result)

    @builtins.property
    def image_optimization_origin_request_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy]:
        result = self._values.get("image_optimization_origin_request_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy], result)

    @builtins.property
    def lambda_origin_request_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy]:
        result = self._values.get("lambda_origin_request_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsOriginRequestPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="open-next-cdk.NextjsProps",
    jsii_struct_bases=[NextjsBaseProps],
    name_mapping={
        "build_command": "buildCommand",
        "build_path": "buildPath",
        "compression_level": "compressionLevel",
        "environment": "environment",
        "is_placeholder": "isPlaceholder",
        "nextjs_path": "nextjsPath",
        "next_js_path": "nextJsPath",
        "node_env": "nodeEnv",
        "open_next_path": "openNextPath",
        "quiet": "quiet",
        "sharp_layer_arn": "sharpLayerArn",
        "temp_build_dir": "tempBuildDir",
        "defaults": "defaults",
        "image_optimization_bucket": "imageOptimizationBucket",
    },
)
class NextjsProps(NextjsBaseProps):
    def __init__(
        self,
        *,
        build_command: typing.Optional[builtins.str] = None,
        build_path: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_placeholder: typing.Optional[builtins.bool] = None,
        nextjs_path: typing.Optional[builtins.str] = None,
        next_js_path: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        open_next_path: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
        sharp_layer_arn: typing.Optional[builtins.str] = None,
        temp_build_dir: typing.Optional[builtins.str] = None,
        defaults: typing.Optional[typing.Union[NextjsDefaultsProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_optimization_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    ) -> None:
        '''
        :param build_command: Optional value used to install NextJS node dependencies. It defaults to 'npx --yes open-next@latest build'
        :param build_path: The directory to execute ``npm run build`` from. By default, it is ``nextjsPath``. Can be overridden, particularly useful for monorepos where ``build`` is expected to run at the root of the project.
        :param compression_level: 0 - no compression, fastest 9 - maximum compression, slowest. Default: 1
        :param environment: Custom environment variables to pass to the NextJS build and runtime.
        :param is_placeholder: (deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.
        :param nextjs_path: (deprecated) Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.
        :param next_js_path: Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param node_env: Optional value for NODE_ENV during build and runtime.
        :param open_next_path: Relative path to the OpenNext package named ``.open-next`` by default. One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param quiet: Less build output.
        :param sharp_layer_arn: Optional arn for the sharp lambda layer. If omitted, the layer will be created.
        :param temp_build_dir: Directory to store temporary build files in. Defaults to os.tmpdir().
        :param defaults: Allows you to override defaults for the resources created by this construct.
        :param image_optimization_bucket: Optional S3 Bucket to use, defaults to assets bucket.
        '''
        if isinstance(defaults, dict):
            defaults = NextjsDefaultsProps(**defaults)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014db87f37373e70d9930df2867cbc2bad2cafed8c75b1ffc138c1240a2fb0bf)
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument build_path", value=build_path, expected_type=type_hints["build_path"])
            check_type(argname="argument compression_level", value=compression_level, expected_type=type_hints["compression_level"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument is_placeholder", value=is_placeholder, expected_type=type_hints["is_placeholder"])
            check_type(argname="argument nextjs_path", value=nextjs_path, expected_type=type_hints["nextjs_path"])
            check_type(argname="argument next_js_path", value=next_js_path, expected_type=type_hints["next_js_path"])
            check_type(argname="argument node_env", value=node_env, expected_type=type_hints["node_env"])
            check_type(argname="argument open_next_path", value=open_next_path, expected_type=type_hints["open_next_path"])
            check_type(argname="argument quiet", value=quiet, expected_type=type_hints["quiet"])
            check_type(argname="argument sharp_layer_arn", value=sharp_layer_arn, expected_type=type_hints["sharp_layer_arn"])
            check_type(argname="argument temp_build_dir", value=temp_build_dir, expected_type=type_hints["temp_build_dir"])
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument image_optimization_bucket", value=image_optimization_bucket, expected_type=type_hints["image_optimization_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_command is not None:
            self._values["build_command"] = build_command
        if build_path is not None:
            self._values["build_path"] = build_path
        if compression_level is not None:
            self._values["compression_level"] = compression_level
        if environment is not None:
            self._values["environment"] = environment
        if is_placeholder is not None:
            self._values["is_placeholder"] = is_placeholder
        if nextjs_path is not None:
            self._values["nextjs_path"] = nextjs_path
        if next_js_path is not None:
            self._values["next_js_path"] = next_js_path
        if node_env is not None:
            self._values["node_env"] = node_env
        if open_next_path is not None:
            self._values["open_next_path"] = open_next_path
        if quiet is not None:
            self._values["quiet"] = quiet
        if sharp_layer_arn is not None:
            self._values["sharp_layer_arn"] = sharp_layer_arn
        if temp_build_dir is not None:
            self._values["temp_build_dir"] = temp_build_dir
        if defaults is not None:
            self._values["defaults"] = defaults
        if image_optimization_bucket is not None:
            self._values["image_optimization_bucket"] = image_optimization_bucket

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''Optional value used to install NextJS node dependencies.

        It defaults to 'npx --yes open-next@latest build'
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_path(self) -> typing.Optional[builtins.str]:
        '''The directory to execute ``npm run build`` from.

        By default, it is ``nextjsPath``.
        Can be overridden, particularly useful for monorepos where ``build`` is expected to run
        at the root of the project.
        '''
        result = self._values.get("build_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression_level(self) -> typing.Optional[jsii.Number]:
        '''0 - no compression, fastest 9 - maximum compression, slowest.

        :default: 1
        '''
        result = self._values.get("compression_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom environment variables to pass to the NextJS build and runtime.'''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def is_placeholder(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.

        :deprecated: use ``openNextPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("is_placeholder")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def nextjs_path(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.

        :deprecated: use ``nextJsPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("nextjs_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_js_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("next_js_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_env(self) -> typing.Optional[builtins.str]:
        '''Optional value for NODE_ENV during build and runtime.'''
        result = self._values.get("node_env")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_next_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the OpenNext package named ``.open-next`` by default.

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("open_next_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quiet(self) -> typing.Optional[builtins.bool]:
        '''Less build output.'''
        result = self._values.get("quiet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sharp_layer_arn(self) -> typing.Optional[builtins.str]:
        '''Optional arn for the sharp lambda layer.

        If omitted, the layer will be created.
        '''
        result = self._values.get("sharp_layer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_build_dir(self) -> typing.Optional[builtins.str]:
        '''Directory to store temporary build files in.

        Defaults to os.tmpdir().
        '''
        result = self._values.get("temp_build_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def defaults(self) -> typing.Optional[NextjsDefaultsProps]:
        '''Allows you to override defaults for the resources created by this construct.'''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[NextjsDefaultsProps], result)

    @builtins.property
    def image_optimization_bucket(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''Optional S3 Bucket to use, defaults to assets bucket.'''
        result = self._values.get("image_optimization_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NextjsS3EnvRewriter(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="open-next-cdk.NextjsS3EnvRewriter",
):
    '''Rewrites variables in S3 objects after a deployment happens to replace CloudFormation tokens with their values.

    These values are not resolved at build time because they are
    only known at deploy time.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        build_command: typing.Optional[builtins.str] = None,
        build_path: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_placeholder: typing.Optional[builtins.bool] = None,
        nextjs_path: typing.Optional[builtins.str] = None,
        next_js_path: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        open_next_path: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
        sharp_layer_arn: typing.Optional[builtins.str] = None,
        temp_build_dir: typing.Optional[builtins.str] = None,
        replacement_config: typing.Union["RewriteReplacementsConfig", typing.Dict[builtins.str, typing.Any]],
        s3_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        s3keys: typing.Sequence[builtins.str],
        cloudfront_distribution_id: typing.Optional[builtins.str] = None,
        debug: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param build_command: Optional value used to install NextJS node dependencies. It defaults to 'npx --yes open-next@latest build'
        :param build_path: The directory to execute ``npm run build`` from. By default, it is ``nextjsPath``. Can be overridden, particularly useful for monorepos where ``build`` is expected to run at the root of the project.
        :param compression_level: 0 - no compression, fastest 9 - maximum compression, slowest. Default: 1
        :param environment: Custom environment variables to pass to the NextJS build and runtime.
        :param is_placeholder: (deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.
        :param nextjs_path: (deprecated) Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.
        :param next_js_path: Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param node_env: Optional value for NODE_ENV during build and runtime.
        :param open_next_path: Relative path to the OpenNext package named ``.open-next`` by default. One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param quiet: Less build output.
        :param sharp_layer_arn: Optional arn for the sharp lambda layer. If omitted, the layer will be created.
        :param temp_build_dir: Directory to store temporary build files in. Defaults to os.tmpdir().
        :param replacement_config: 
        :param s3_bucket: 
        :param s3keys: 
        :param cloudfront_distribution_id: 
        :param debug: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df1a18724360cf1749ec444d4ce6c18a8aa9328a161d3fa5a00db5c5c695ffb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NextjsS3EnvRewriterProps(
            build_command=build_command,
            build_path=build_path,
            compression_level=compression_level,
            environment=environment,
            is_placeholder=is_placeholder,
            nextjs_path=nextjs_path,
            next_js_path=next_js_path,
            node_env=node_env,
            open_next_path=open_next_path,
            quiet=quiet,
            sharp_layer_arn=sharp_layer_arn,
            temp_build_dir=temp_build_dir,
            replacement_config=replacement_config,
            s3_bucket=s3_bucket,
            s3keys=s3keys,
            cloudfront_distribution_id=cloudfront_distribution_id,
            debug=debug,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="rewriteNode")
    def rewrite_node(self) -> typing.Optional[_constructs_77d1e7e8.Construct]:
        return typing.cast(typing.Optional[_constructs_77d1e7e8.Construct], jsii.get(self, "rewriteNode"))

    @rewrite_node.setter
    def rewrite_node(
        self,
        value: typing.Optional[_constructs_77d1e7e8.Construct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c5f8577d14ba37a10e5749b77bcd6b33b7f45799e6087b1a7caa5c0127d7f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rewriteNode", value)


@jsii.data_type(
    jsii_type="open-next-cdk.RewriteReplacementsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "env": "env",
        "json_s3_bucket": "jsonS3Bucket",
        "json_s3_key": "jsonS3Key",
    },
)
class RewriteReplacementsConfig:
    def __init__(
        self,
        *,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        json_s3_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        json_s3_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param env: 
        :param json_s3_bucket: 
        :param json_s3_key: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa704f388c7acf1d06e8f3f9dd9607914e4e88881ed5b95b0ffa74c3589de118)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument json_s3_bucket", value=json_s3_bucket, expected_type=type_hints["json_s3_bucket"])
            check_type(argname="argument json_s3_key", value=json_s3_key, expected_type=type_hints["json_s3_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if env is not None:
            self._values["env"] = env
        if json_s3_bucket is not None:
            self._values["json_s3_bucket"] = json_s3_bucket
        if json_s3_key is not None:
            self._values["json_s3_key"] = json_s3_key

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def json_s3_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        result = self._values.get("json_s3_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def json_s3_key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("json_s3_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RewriteReplacementsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="open-next-cdk.RewriterParams",
    jsii_struct_bases=[],
    name_mapping={
        "replacement_config": "replacementConfig",
        "s3_bucket": "s3Bucket",
        "s3keys": "s3keys",
        "cloudfront_distribution_id": "cloudfrontDistributionId",
        "debug": "debug",
    },
)
class RewriterParams:
    def __init__(
        self,
        *,
        replacement_config: typing.Union[RewriteReplacementsConfig, typing.Dict[builtins.str, typing.Any]],
        s3_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        s3keys: typing.Sequence[builtins.str],
        cloudfront_distribution_id: typing.Optional[builtins.str] = None,
        debug: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param replacement_config: 
        :param s3_bucket: 
        :param s3keys: 
        :param cloudfront_distribution_id: 
        :param debug: 
        '''
        if isinstance(replacement_config, dict):
            replacement_config = RewriteReplacementsConfig(**replacement_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff83d6924e35bccbe4afc1591f0143870d4b7531b5aeea0eccd14ab8c37c7bf)
            check_type(argname="argument replacement_config", value=replacement_config, expected_type=type_hints["replacement_config"])
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument s3keys", value=s3keys, expected_type=type_hints["s3keys"])
            check_type(argname="argument cloudfront_distribution_id", value=cloudfront_distribution_id, expected_type=type_hints["cloudfront_distribution_id"])
            check_type(argname="argument debug", value=debug, expected_type=type_hints["debug"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "replacement_config": replacement_config,
            "s3_bucket": s3_bucket,
            "s3keys": s3keys,
        }
        if cloudfront_distribution_id is not None:
            self._values["cloudfront_distribution_id"] = cloudfront_distribution_id
        if debug is not None:
            self._values["debug"] = debug

    @builtins.property
    def replacement_config(self) -> RewriteReplacementsConfig:
        result = self._values.get("replacement_config")
        assert result is not None, "Required property 'replacement_config' is missing"
        return typing.cast(RewriteReplacementsConfig, result)

    @builtins.property
    def s3_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def s3keys(self) -> typing.List[builtins.str]:
        result = self._values.get("s3keys")
        assert result is not None, "Required property 's3keys' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cloudfront_distribution_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cloudfront_distribution_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def debug(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("debug")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RewriterParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="open-next-cdk.ImageOptimizationProps",
    jsii_struct_bases=[NextjsBaseProps],
    name_mapping={
        "build_command": "buildCommand",
        "build_path": "buildPath",
        "compression_level": "compressionLevel",
        "environment": "environment",
        "is_placeholder": "isPlaceholder",
        "nextjs_path": "nextjsPath",
        "next_js_path": "nextJsPath",
        "node_env": "nodeEnv",
        "open_next_path": "openNextPath",
        "quiet": "quiet",
        "sharp_layer_arn": "sharpLayerArn",
        "temp_build_dir": "tempBuildDir",
        "bucket": "bucket",
        "next_build": "nextBuild",
        "lambda_options": "lambdaOptions",
    },
)
class ImageOptimizationProps(NextjsBaseProps):
    def __init__(
        self,
        *,
        build_command: typing.Optional[builtins.str] = None,
        build_path: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_placeholder: typing.Optional[builtins.bool] = None,
        nextjs_path: typing.Optional[builtins.str] = None,
        next_js_path: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        open_next_path: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
        sharp_layer_arn: typing.Optional[builtins.str] = None,
        temp_build_dir: typing.Optional[builtins.str] = None,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        next_build: NextjsBuild,
        lambda_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param build_command: Optional value used to install NextJS node dependencies. It defaults to 'npx --yes open-next@latest build'
        :param build_path: The directory to execute ``npm run build`` from. By default, it is ``nextjsPath``. Can be overridden, particularly useful for monorepos where ``build`` is expected to run at the root of the project.
        :param compression_level: 0 - no compression, fastest 9 - maximum compression, slowest. Default: 1
        :param environment: Custom environment variables to pass to the NextJS build and runtime.
        :param is_placeholder: (deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.
        :param nextjs_path: (deprecated) Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.
        :param next_js_path: Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param node_env: Optional value for NODE_ENV during build and runtime.
        :param open_next_path: Relative path to the OpenNext package named ``.open-next`` by default. One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param quiet: Less build output.
        :param sharp_layer_arn: Optional arn for the sharp lambda layer. If omitted, the layer will be created.
        :param temp_build_dir: Directory to store temporary build files in. Defaults to os.tmpdir().
        :param bucket: The S3 bucket holding application images.
        :param next_build: The ``NextjsBuild`` instance representing the built Nextjs application.
        :param lambda_options: Override function properties.
        '''
        if isinstance(lambda_options, dict):
            lambda_options = _aws_cdk_aws_lambda_ceddda9d.FunctionOptions(**lambda_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710ec40c82cf50feb374c3f2e6241ae54a2573c4abba6b30508027a8581722a1)
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument build_path", value=build_path, expected_type=type_hints["build_path"])
            check_type(argname="argument compression_level", value=compression_level, expected_type=type_hints["compression_level"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument is_placeholder", value=is_placeholder, expected_type=type_hints["is_placeholder"])
            check_type(argname="argument nextjs_path", value=nextjs_path, expected_type=type_hints["nextjs_path"])
            check_type(argname="argument next_js_path", value=next_js_path, expected_type=type_hints["next_js_path"])
            check_type(argname="argument node_env", value=node_env, expected_type=type_hints["node_env"])
            check_type(argname="argument open_next_path", value=open_next_path, expected_type=type_hints["open_next_path"])
            check_type(argname="argument quiet", value=quiet, expected_type=type_hints["quiet"])
            check_type(argname="argument sharp_layer_arn", value=sharp_layer_arn, expected_type=type_hints["sharp_layer_arn"])
            check_type(argname="argument temp_build_dir", value=temp_build_dir, expected_type=type_hints["temp_build_dir"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument next_build", value=next_build, expected_type=type_hints["next_build"])
            check_type(argname="argument lambda_options", value=lambda_options, expected_type=type_hints["lambda_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "next_build": next_build,
        }
        if build_command is not None:
            self._values["build_command"] = build_command
        if build_path is not None:
            self._values["build_path"] = build_path
        if compression_level is not None:
            self._values["compression_level"] = compression_level
        if environment is not None:
            self._values["environment"] = environment
        if is_placeholder is not None:
            self._values["is_placeholder"] = is_placeholder
        if nextjs_path is not None:
            self._values["nextjs_path"] = nextjs_path
        if next_js_path is not None:
            self._values["next_js_path"] = next_js_path
        if node_env is not None:
            self._values["node_env"] = node_env
        if open_next_path is not None:
            self._values["open_next_path"] = open_next_path
        if quiet is not None:
            self._values["quiet"] = quiet
        if sharp_layer_arn is not None:
            self._values["sharp_layer_arn"] = sharp_layer_arn
        if temp_build_dir is not None:
            self._values["temp_build_dir"] = temp_build_dir
        if lambda_options is not None:
            self._values["lambda_options"] = lambda_options

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''Optional value used to install NextJS node dependencies.

        It defaults to 'npx --yes open-next@latest build'
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_path(self) -> typing.Optional[builtins.str]:
        '''The directory to execute ``npm run build`` from.

        By default, it is ``nextjsPath``.
        Can be overridden, particularly useful for monorepos where ``build`` is expected to run
        at the root of the project.
        '''
        result = self._values.get("build_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression_level(self) -> typing.Optional[jsii.Number]:
        '''0 - no compression, fastest 9 - maximum compression, slowest.

        :default: 1
        '''
        result = self._values.get("compression_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom environment variables to pass to the NextJS build and runtime.'''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def is_placeholder(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.

        :deprecated: use ``openNextPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("is_placeholder")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def nextjs_path(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.

        :deprecated: use ``nextJsPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("nextjs_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_js_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("next_js_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_env(self) -> typing.Optional[builtins.str]:
        '''Optional value for NODE_ENV during build and runtime.'''
        result = self._values.get("node_env")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_next_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the OpenNext package named ``.open-next`` by default.

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("open_next_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quiet(self) -> typing.Optional[builtins.bool]:
        '''Less build output.'''
        result = self._values.get("quiet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sharp_layer_arn(self) -> typing.Optional[builtins.str]:
        '''Optional arn for the sharp lambda layer.

        If omitted, the layer will be created.
        '''
        result = self._values.get("sharp_layer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_build_dir(self) -> typing.Optional[builtins.str]:
        '''Directory to store temporary build files in.

        Defaults to os.tmpdir().
        '''
        result = self._values.get("temp_build_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''The S3 bucket holding application images.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def next_build(self) -> NextjsBuild:
        '''The ``NextjsBuild`` instance representing the built Nextjs application.'''
        result = self._values.get("next_build")
        assert result is not None, "Required property 'next_build' is missing"
        return typing.cast(NextjsBuild, result)

    @builtins.property
    def lambda_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions]:
        '''Override function properties.'''
        result = self._values.get("lambda_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageOptimizationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="open-next-cdk.NextjsAssetsDeploymentProps",
    jsii_struct_bases=[NextjsBaseProps],
    name_mapping={
        "build_command": "buildCommand",
        "build_path": "buildPath",
        "compression_level": "compressionLevel",
        "environment": "environment",
        "is_placeholder": "isPlaceholder",
        "nextjs_path": "nextjsPath",
        "next_js_path": "nextJsPath",
        "node_env": "nodeEnv",
        "open_next_path": "openNextPath",
        "quiet": "quiet",
        "sharp_layer_arn": "sharpLayerArn",
        "temp_build_dir": "tempBuildDir",
        "bucket": "bucket",
        "next_build": "nextBuild",
        "cache_policies": "cachePolicies",
        "distribution": "distribution",
        "ephemeral_storage_size": "ephemeralStorageSize",
        "memory_limit": "memoryLimit",
        "prune": "prune",
        "use_efs": "useEfs",
        "vpc": "vpc",
    },
)
class NextjsAssetsDeploymentProps(NextjsBaseProps):
    def __init__(
        self,
        *,
        build_command: typing.Optional[builtins.str] = None,
        build_path: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_placeholder: typing.Optional[builtins.bool] = None,
        nextjs_path: typing.Optional[builtins.str] = None,
        next_js_path: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        open_next_path: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
        sharp_layer_arn: typing.Optional[builtins.str] = None,
        temp_build_dir: typing.Optional[builtins.str] = None,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        next_build: NextjsBuild,
        cache_policies: typing.Optional[typing.Union[NextjsAssetsCachePolicyProps, typing.Dict[builtins.str, typing.Any]]] = None,
        distribution: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution] = None,
        ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
        prune: typing.Optional[builtins.bool] = None,
        use_efs: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param build_command: Optional value used to install NextJS node dependencies. It defaults to 'npx --yes open-next@latest build'
        :param build_path: The directory to execute ``npm run build`` from. By default, it is ``nextjsPath``. Can be overridden, particularly useful for monorepos where ``build`` is expected to run at the root of the project.
        :param compression_level: 0 - no compression, fastest 9 - maximum compression, slowest. Default: 1
        :param environment: Custom environment variables to pass to the NextJS build and runtime.
        :param is_placeholder: (deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.
        :param nextjs_path: (deprecated) Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.
        :param next_js_path: Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param node_env: Optional value for NODE_ENV during build and runtime.
        :param open_next_path: Relative path to the OpenNext package named ``.open-next`` by default. One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param quiet: Less build output.
        :param sharp_layer_arn: Optional arn for the sharp lambda layer. If omitted, the layer will be created.
        :param temp_build_dir: Directory to store temporary build files in. Defaults to os.tmpdir().
        :param bucket: Properties for the S3 bucket containing the NextJS assets.
        :param next_build: The ``NextjsBuild`` instance representing the built Nextjs application.
        :param cache_policies: Override the default S3 cache policies created internally.
        :param distribution: Distribution to invalidate when assets change.
        :param ephemeral_storage_size: ephemeralStorageSize for lambda function which been run by BucketDeployment.
        :param memory_limit: memoryLimit for lambda function which been run by BucketDeployment.
        :param prune: Set to true to delete old assets (defaults to false). Recommended to only set to true if you don't need the ability to roll back deployments.
        :param use_efs: In case of useEfs, vpc is required.
        :param vpc: In case of useEfs, vpc is required.
        '''
        if isinstance(cache_policies, dict):
            cache_policies = NextjsAssetsCachePolicyProps(**cache_policies)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae64d307733915cb668ea5f338f12bc80df41ff63e405ab971fc71674b0aa622)
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument build_path", value=build_path, expected_type=type_hints["build_path"])
            check_type(argname="argument compression_level", value=compression_level, expected_type=type_hints["compression_level"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument is_placeholder", value=is_placeholder, expected_type=type_hints["is_placeholder"])
            check_type(argname="argument nextjs_path", value=nextjs_path, expected_type=type_hints["nextjs_path"])
            check_type(argname="argument next_js_path", value=next_js_path, expected_type=type_hints["next_js_path"])
            check_type(argname="argument node_env", value=node_env, expected_type=type_hints["node_env"])
            check_type(argname="argument open_next_path", value=open_next_path, expected_type=type_hints["open_next_path"])
            check_type(argname="argument quiet", value=quiet, expected_type=type_hints["quiet"])
            check_type(argname="argument sharp_layer_arn", value=sharp_layer_arn, expected_type=type_hints["sharp_layer_arn"])
            check_type(argname="argument temp_build_dir", value=temp_build_dir, expected_type=type_hints["temp_build_dir"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument next_build", value=next_build, expected_type=type_hints["next_build"])
            check_type(argname="argument cache_policies", value=cache_policies, expected_type=type_hints["cache_policies"])
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
            check_type(argname="argument ephemeral_storage_size", value=ephemeral_storage_size, expected_type=type_hints["ephemeral_storage_size"])
            check_type(argname="argument memory_limit", value=memory_limit, expected_type=type_hints["memory_limit"])
            check_type(argname="argument prune", value=prune, expected_type=type_hints["prune"])
            check_type(argname="argument use_efs", value=use_efs, expected_type=type_hints["use_efs"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "next_build": next_build,
        }
        if build_command is not None:
            self._values["build_command"] = build_command
        if build_path is not None:
            self._values["build_path"] = build_path
        if compression_level is not None:
            self._values["compression_level"] = compression_level
        if environment is not None:
            self._values["environment"] = environment
        if is_placeholder is not None:
            self._values["is_placeholder"] = is_placeholder
        if nextjs_path is not None:
            self._values["nextjs_path"] = nextjs_path
        if next_js_path is not None:
            self._values["next_js_path"] = next_js_path
        if node_env is not None:
            self._values["node_env"] = node_env
        if open_next_path is not None:
            self._values["open_next_path"] = open_next_path
        if quiet is not None:
            self._values["quiet"] = quiet
        if sharp_layer_arn is not None:
            self._values["sharp_layer_arn"] = sharp_layer_arn
        if temp_build_dir is not None:
            self._values["temp_build_dir"] = temp_build_dir
        if cache_policies is not None:
            self._values["cache_policies"] = cache_policies
        if distribution is not None:
            self._values["distribution"] = distribution
        if ephemeral_storage_size is not None:
            self._values["ephemeral_storage_size"] = ephemeral_storage_size
        if memory_limit is not None:
            self._values["memory_limit"] = memory_limit
        if prune is not None:
            self._values["prune"] = prune
        if use_efs is not None:
            self._values["use_efs"] = use_efs
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''Optional value used to install NextJS node dependencies.

        It defaults to 'npx --yes open-next@latest build'
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_path(self) -> typing.Optional[builtins.str]:
        '''The directory to execute ``npm run build`` from.

        By default, it is ``nextjsPath``.
        Can be overridden, particularly useful for monorepos where ``build`` is expected to run
        at the root of the project.
        '''
        result = self._values.get("build_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression_level(self) -> typing.Optional[jsii.Number]:
        '''0 - no compression, fastest 9 - maximum compression, slowest.

        :default: 1
        '''
        result = self._values.get("compression_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom environment variables to pass to the NextJS build and runtime.'''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def is_placeholder(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.

        :deprecated: use ``openNextPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("is_placeholder")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def nextjs_path(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.

        :deprecated: use ``nextJsPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("nextjs_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_js_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("next_js_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_env(self) -> typing.Optional[builtins.str]:
        '''Optional value for NODE_ENV during build and runtime.'''
        result = self._values.get("node_env")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_next_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the OpenNext package named ``.open-next`` by default.

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("open_next_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quiet(self) -> typing.Optional[builtins.bool]:
        '''Less build output.'''
        result = self._values.get("quiet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sharp_layer_arn(self) -> typing.Optional[builtins.str]:
        '''Optional arn for the sharp lambda layer.

        If omitted, the layer will be created.
        '''
        result = self._values.get("sharp_layer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_build_dir(self) -> typing.Optional[builtins.str]:
        '''Directory to store temporary build files in.

        Defaults to os.tmpdir().
        '''
        result = self._values.get("temp_build_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''Properties for the S3 bucket containing the NextJS assets.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def next_build(self) -> NextjsBuild:
        '''The ``NextjsBuild`` instance representing the built Nextjs application.'''
        result = self._values.get("next_build")
        assert result is not None, "Required property 'next_build' is missing"
        return typing.cast(NextjsBuild, result)

    @builtins.property
    def cache_policies(self) -> typing.Optional[NextjsAssetsCachePolicyProps]:
        '''Override the default S3 cache policies created internally.'''
        result = self._values.get("cache_policies")
        return typing.cast(typing.Optional[NextjsAssetsCachePolicyProps], result)

    @builtins.property
    def distribution(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution]:
        '''Distribution to invalidate when assets change.'''
        result = self._values.get("distribution")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution], result)

    @builtins.property
    def ephemeral_storage_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''ephemeralStorageSize for lambda function which been run by BucketDeployment.'''
        result = self._values.get("ephemeral_storage_size")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        '''memoryLimit for lambda function which been run by BucketDeployment.'''
        result = self._values.get("memory_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prune(self) -> typing.Optional[builtins.bool]:
        '''Set to true to delete old assets (defaults to false).

        Recommended to only set to true if you don't need the ability to roll back deployments.
        '''
        result = self._values.get("prune")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def use_efs(self) -> typing.Optional[builtins.bool]:
        '''In case of useEfs, vpc is required.'''
        result = self._values.get("use_efs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''In case of useEfs, vpc is required.'''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsAssetsDeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="open-next-cdk.NextjsS3EnvRewriterProps",
    jsii_struct_bases=[NextjsBaseProps, RewriterParams],
    name_mapping={
        "build_command": "buildCommand",
        "build_path": "buildPath",
        "compression_level": "compressionLevel",
        "environment": "environment",
        "is_placeholder": "isPlaceholder",
        "nextjs_path": "nextjsPath",
        "next_js_path": "nextJsPath",
        "node_env": "nodeEnv",
        "open_next_path": "openNextPath",
        "quiet": "quiet",
        "sharp_layer_arn": "sharpLayerArn",
        "temp_build_dir": "tempBuildDir",
        "replacement_config": "replacementConfig",
        "s3_bucket": "s3Bucket",
        "s3keys": "s3keys",
        "cloudfront_distribution_id": "cloudfrontDistributionId",
        "debug": "debug",
    },
)
class NextjsS3EnvRewriterProps(NextjsBaseProps, RewriterParams):
    def __init__(
        self,
        *,
        build_command: typing.Optional[builtins.str] = None,
        build_path: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        is_placeholder: typing.Optional[builtins.bool] = None,
        nextjs_path: typing.Optional[builtins.str] = None,
        next_js_path: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        open_next_path: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
        sharp_layer_arn: typing.Optional[builtins.str] = None,
        temp_build_dir: typing.Optional[builtins.str] = None,
        replacement_config: typing.Union[RewriteReplacementsConfig, typing.Dict[builtins.str, typing.Any]],
        s3_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        s3keys: typing.Sequence[builtins.str],
        cloudfront_distribution_id: typing.Optional[builtins.str] = None,
        debug: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param build_command: Optional value used to install NextJS node dependencies. It defaults to 'npx --yes open-next@latest build'
        :param build_path: The directory to execute ``npm run build`` from. By default, it is ``nextjsPath``. Can be overridden, particularly useful for monorepos where ``build`` is expected to run at the root of the project.
        :param compression_level: 0 - no compression, fastest 9 - maximum compression, slowest. Default: 1
        :param environment: Custom environment variables to pass to the NextJS build and runtime.
        :param is_placeholder: (deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.
        :param nextjs_path: (deprecated) Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.
        :param next_js_path: Relative path to the directory where the NextJS project is located. Can be the root of your project (``.``) or a subdirectory (``packages/web``). One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param node_env: Optional value for NODE_ENV during build and runtime.
        :param open_next_path: Relative path to the OpenNext package named ``.open-next`` by default. One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        :param quiet: Less build output.
        :param sharp_layer_arn: Optional arn for the sharp lambda layer. If omitted, the layer will be created.
        :param temp_build_dir: Directory to store temporary build files in. Defaults to os.tmpdir().
        :param replacement_config: 
        :param s3_bucket: 
        :param s3keys: 
        :param cloudfront_distribution_id: 
        :param debug: 
        '''
        if isinstance(replacement_config, dict):
            replacement_config = RewriteReplacementsConfig(**replacement_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0323bdd0d73ebcdc84ea335a90b20eae8c790d19dda7c0e320c8bbb3d2212369)
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument build_path", value=build_path, expected_type=type_hints["build_path"])
            check_type(argname="argument compression_level", value=compression_level, expected_type=type_hints["compression_level"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument is_placeholder", value=is_placeholder, expected_type=type_hints["is_placeholder"])
            check_type(argname="argument nextjs_path", value=nextjs_path, expected_type=type_hints["nextjs_path"])
            check_type(argname="argument next_js_path", value=next_js_path, expected_type=type_hints["next_js_path"])
            check_type(argname="argument node_env", value=node_env, expected_type=type_hints["node_env"])
            check_type(argname="argument open_next_path", value=open_next_path, expected_type=type_hints["open_next_path"])
            check_type(argname="argument quiet", value=quiet, expected_type=type_hints["quiet"])
            check_type(argname="argument sharp_layer_arn", value=sharp_layer_arn, expected_type=type_hints["sharp_layer_arn"])
            check_type(argname="argument temp_build_dir", value=temp_build_dir, expected_type=type_hints["temp_build_dir"])
            check_type(argname="argument replacement_config", value=replacement_config, expected_type=type_hints["replacement_config"])
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument s3keys", value=s3keys, expected_type=type_hints["s3keys"])
            check_type(argname="argument cloudfront_distribution_id", value=cloudfront_distribution_id, expected_type=type_hints["cloudfront_distribution_id"])
            check_type(argname="argument debug", value=debug, expected_type=type_hints["debug"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "replacement_config": replacement_config,
            "s3_bucket": s3_bucket,
            "s3keys": s3keys,
        }
        if build_command is not None:
            self._values["build_command"] = build_command
        if build_path is not None:
            self._values["build_path"] = build_path
        if compression_level is not None:
            self._values["compression_level"] = compression_level
        if environment is not None:
            self._values["environment"] = environment
        if is_placeholder is not None:
            self._values["is_placeholder"] = is_placeholder
        if nextjs_path is not None:
            self._values["nextjs_path"] = nextjs_path
        if next_js_path is not None:
            self._values["next_js_path"] = next_js_path
        if node_env is not None:
            self._values["node_env"] = node_env
        if open_next_path is not None:
            self._values["open_next_path"] = open_next_path
        if quiet is not None:
            self._values["quiet"] = quiet
        if sharp_layer_arn is not None:
            self._values["sharp_layer_arn"] = sharp_layer_arn
        if temp_build_dir is not None:
            self._values["temp_build_dir"] = temp_build_dir
        if cloudfront_distribution_id is not None:
            self._values["cloudfront_distribution_id"] = cloudfront_distribution_id
        if debug is not None:
            self._values["debug"] = debug

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''Optional value used to install NextJS node dependencies.

        It defaults to 'npx --yes open-next@latest build'
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_path(self) -> typing.Optional[builtins.str]:
        '''The directory to execute ``npm run build`` from.

        By default, it is ``nextjsPath``.
        Can be overridden, particularly useful for monorepos where ``build`` is expected to run
        at the root of the project.
        '''
        result = self._values.get("build_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression_level(self) -> typing.Optional[jsii.Number]:
        '''0 - no compression, fastest 9 - maximum compression, slowest.

        :default: 1
        '''
        result = self._values.get("compression_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom environment variables to pass to the NextJS build and runtime.'''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def is_placeholder(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Used in conjunction with nextJsPath to skip building NextJS app and assume .open-next folder already exists. Useful when using ``next dev`` for local development.

        :deprecated: use ``openNextPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("is_placeholder")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def nextjs_path(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath``, ``nextJsPath`` or ``nextjsPath`` must be supplied.

        :deprecated: use ``nextJsPath`` instead

        :stability: deprecated
        '''
        result = self._values.get("nextjs_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_js_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the directory where the NextJS project is located.

        Can be the root of your project (``.``) or a subdirectory (``packages/web``).

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("next_js_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_env(self) -> typing.Optional[builtins.str]:
        '''Optional value for NODE_ENV during build and runtime.'''
        result = self._values.get("node_env")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_next_path(self) -> typing.Optional[builtins.str]:
        '''Relative path to the OpenNext package named ``.open-next`` by default.

        One of ``openNextPath`` or ``nextJsPath`` must be supplied.
        '''
        result = self._values.get("open_next_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quiet(self) -> typing.Optional[builtins.bool]:
        '''Less build output.'''
        result = self._values.get("quiet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sharp_layer_arn(self) -> typing.Optional[builtins.str]:
        '''Optional arn for the sharp lambda layer.

        If omitted, the layer will be created.
        '''
        result = self._values.get("sharp_layer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_build_dir(self) -> typing.Optional[builtins.str]:
        '''Directory to store temporary build files in.

        Defaults to os.tmpdir().
        '''
        result = self._values.get("temp_build_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replacement_config(self) -> RewriteReplacementsConfig:
        result = self._values.get("replacement_config")
        assert result is not None, "Required property 'replacement_config' is missing"
        return typing.cast(RewriteReplacementsConfig, result)

    @builtins.property
    def s3_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def s3keys(self) -> typing.List[builtins.str]:
        result = self._values.get("s3keys")
        assert result is not None, "Required property 's3keys' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cloudfront_distribution_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cloudfront_distribution_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def debug(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("debug")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsS3EnvRewriterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BaseSiteDomainProps",
    "BaseSiteEnvironmentOutputsInfo",
    "BaseSiteReplaceProps",
    "CreateArchiveArgs",
    "ImageOptimizationLambda",
    "ImageOptimizationProps",
    "NextJsAssetsDeployment",
    "NextJsLambda",
    "Nextjs",
    "NextjsAssetsCachePolicyProps",
    "NextjsAssetsDeploymentProps",
    "NextjsBaseProps",
    "NextjsBuild",
    "NextjsBuildProps",
    "NextjsCachePolicyProps",
    "NextjsDefaultsProps",
    "NextjsDistribution",
    "NextjsDistributionCdkProps",
    "NextjsDistributionProps",
    "NextjsDomainProps",
    "NextjsLambdaProps",
    "NextjsLayer",
    "NextjsLayerProps",
    "NextjsOriginRequestPolicyProps",
    "NextjsProps",
    "NextjsS3EnvRewriter",
    "NextjsS3EnvRewriterProps",
    "RewriteReplacementsConfig",
    "RewriterParams",
]

publication.publish()

def _typecheckingstub__019eb9cb658a919f238ec89c2ac4f8d4f430a39ae77b8e15a0af0e839efefa8f(
    *,
    domain_name: builtins.str,
    alternate_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    domain_alias: typing.Optional[builtins.str] = None,
    hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
    is_external_domain: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a37ab543538565e7eca2e38a6e7c09a4a90a2a5367294a1559439e7e1971a4b(
    *,
    environment_outputs: typing.Mapping[builtins.str, builtins.str],
    path: builtins.str,
    stack: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc26084934caab47ace3ffcee4e6b0cac75371bb903717a566b321e735a5830e(
    *,
    files: builtins.str,
    replace: builtins.str,
    search: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee680970a366f95bf6ef80132b6eadd2e646f8f195c4e8dfbfa95337d5878bf0(
    *,
    directory: builtins.str,
    zip_file_name: builtins.str,
    zip_out_dir: builtins.str,
    compression_level: typing.Optional[jsii.Number] = None,
    file_glob: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157f5efeb550e21797ac19dc1f9b4330b5c51b7bdb58c9e7b911cfb50c9195cb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    next_build: NextjsBuild,
    lambda_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_command: typing.Optional[builtins.str] = None,
    build_path: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_placeholder: typing.Optional[builtins.bool] = None,
    nextjs_path: typing.Optional[builtins.str] = None,
    next_js_path: typing.Optional[builtins.str] = None,
    node_env: typing.Optional[builtins.str] = None,
    open_next_path: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
    sharp_layer_arn: typing.Optional[builtins.str] = None,
    temp_build_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588b2f02789bdd1c109803091defa80aeaec7785450eaa47be42a9971c720cb4(
    value: _aws_cdk_aws_s3_ceddda9d.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6045d57fb31451fb936db3248c52f6b83aefddab050f147e709aae07a940f439(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    next_build: NextjsBuild,
    cache_policies: typing.Optional[typing.Union[NextjsAssetsCachePolicyProps, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    memory_limit: typing.Optional[jsii.Number] = None,
    prune: typing.Optional[builtins.bool] = None,
    use_efs: typing.Optional[builtins.bool] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    build_command: typing.Optional[builtins.str] = None,
    build_path: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_placeholder: typing.Optional[builtins.bool] = None,
    nextjs_path: typing.Optional[builtins.str] = None,
    next_js_path: typing.Optional[builtins.str] = None,
    node_env: typing.Optional[builtins.str] = None,
    open_next_path: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
    sharp_layer_arn: typing.Optional[builtins.str] = None,
    temp_build_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c6cec02d84c8bc3e73efd718be681e79029f97892a72e5bca357aa036a4f81(
    value: _aws_cdk_aws_s3_ceddda9d.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1327f99f641d04415d8421d141b6f78b0eee4bd2f8cbdae17d1e886c56fdebd(
    value: typing.List[_aws_cdk_aws_s3_deployment_ceddda9d.BucketDeployment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d32aed5501f7c71e063a4c5cf333b32b8c9996b9b5b4279619c90dc83c3320(
    value: NextjsAssetsDeploymentProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5cc7ae950eb1bae0bda3e0bd18762fa2dcd8c4ccf2c768de9e35455c00610ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66b1fadb3e68f42b191aa2a4aefa30763ca59ece898c809f8228a9c2621a651(
    value: typing.Optional[NextjsS3EnvRewriter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c85864266153cb3d4005ca79b503771e7b9925308a48822000a74f5e033e14(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    next_build: NextjsBuild,
    lambda_: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    build_command: typing.Optional[builtins.str] = None,
    build_path: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_placeholder: typing.Optional[builtins.bool] = None,
    nextjs_path: typing.Optional[builtins.str] = None,
    next_js_path: typing.Optional[builtins.str] = None,
    node_env: typing.Optional[builtins.str] = None,
    open_next_path: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
    sharp_layer_arn: typing.Optional[builtins.str] = None,
    temp_build_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c8396a4420e3be6327f0a446fbeed1d617d702af6b5e586d255aa297905b3f(
    replacement_params: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa71d4dacf5733f40404eadc2057462b59e9bf42dad339819d7a812526a14ebf(
    value: _aws_cdk_aws_lambda_ceddda9d.Function,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82994df33753e5860e831c81987bda0fc5c3272885fe48c387dde700c530c5fb(
    value: typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9535918ed268c2e0e473996077280651fd58778071f4e8b0956e46fc71e19aa0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    defaults: typing.Optional[typing.Union[NextjsDefaultsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_optimization_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    build_command: typing.Optional[builtins.str] = None,
    build_path: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_placeholder: typing.Optional[builtins.bool] = None,
    nextjs_path: typing.Optional[builtins.str] = None,
    next_js_path: typing.Optional[builtins.str] = None,
    node_env: typing.Optional[builtins.str] = None,
    open_next_path: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
    sharp_layer_arn: typing.Optional[builtins.str] = None,
    temp_build_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a96beea058283d44fc69a720bc3146dd7665681fdf587d8317b98f31848a54(
    value: NextJsAssetsDeployment,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66115b1083ac96ae90c36905d71a1899c5b2996a05bc48371059c5f0772a29f(
    value: NextjsDistribution,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d1482f66c73ff51ce110fad7c441e89de7c4233253f987165cc337cdd7e4dd(
    value: ImageOptimizationLambda,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79cf5e6d7eec23d62a041e6a112917a27fc15aced738d0167375b4036920ae3(
    value: _aws_cdk_aws_lambda_ceddda9d.FunctionUrl,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10cf35c72782073e027c09dd0f89e4828580bd26ee19b53f61fc82d1628d63c2(
    value: _aws_cdk_aws_lambda_ceddda9d.FunctionUrl,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f37641bca890433f71effb5852c463b6e8ed0687407757ac84e4ea541f2ef3f(
    value: NextjsBuild,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53482f9991762e4bf6015d390d17745121e2f9388a6aca4c38ea04c090958889(
    value: NextjsProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42ca1a45458c5f184ac29830e2c4f0f57574d4025ebc989c7876b17578d2090(
    value: NextJsLambda,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6273ad4e83f2dc262e098a33cae7c5b7c352a80269b88e1329f3893ad019c8(
    value: _aws_cdk_aws_s3_ceddda9d.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2f88c2afe3d23d88a89f83eccb3397f0da1c0f7b2b95c12828733706b87319(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de266f92ce9933a969eb89db4385680a75d24dd79fa1a114ae884255d2e9f14(
    value: typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b262b89d865ef0d9906001dc575f0c2d26b5595c39ca421bc05d0350e73d33(
    *,
    static_max_age_default: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    static_stale_while_revalidate_default: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ec93c51d94a84969d4927564d798c246740d1434e27b5b273de694bcb20eb7(
    *,
    build_command: typing.Optional[builtins.str] = None,
    build_path: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_placeholder: typing.Optional[builtins.bool] = None,
    nextjs_path: typing.Optional[builtins.str] = None,
    next_js_path: typing.Optional[builtins.str] = None,
    node_env: typing.Optional[builtins.str] = None,
    open_next_path: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
    sharp_layer_arn: typing.Optional[builtins.str] = None,
    temp_build_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9d80a1ea2ef48546f31aefe8a0be85957df79feb9c7df063a9bd3bbdb52d29(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    build_command: typing.Optional[builtins.str] = None,
    build_path: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_placeholder: typing.Optional[builtins.bool] = None,
    nextjs_path: typing.Optional[builtins.str] = None,
    next_js_path: typing.Optional[builtins.str] = None,
    node_env: typing.Optional[builtins.str] = None,
    open_next_path: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
    sharp_layer_arn: typing.Optional[builtins.str] = None,
    temp_build_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a912e3a54c42492f785a9d372ca82465f6ff9b69009e400d852c360b67f76f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ace1ca8dd1b78da960b5d20cce2b57b05dee340f64f297db89f59417ee6478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235fe242c6d21213443c40d48046f33d758998c7da50aa59cd543cabf16fa5f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f5d5dbc76a5b36128a18058a86db2c28f8d473a64027f62353357ab989fd97(
    value: NextjsBuildProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa960e2f5007cf0398b02a4d3d88cea2967cc0b60b1817da2432a756414ff24e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f76be60c8fe54d3eedb4892d9d0ad058323cadecd0198fd368c07f2d16541ce(
    *,
    build_command: typing.Optional[builtins.str] = None,
    build_path: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_placeholder: typing.Optional[builtins.bool] = None,
    nextjs_path: typing.Optional[builtins.str] = None,
    next_js_path: typing.Optional[builtins.str] = None,
    node_env: typing.Optional[builtins.str] = None,
    open_next_path: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
    sharp_layer_arn: typing.Optional[builtins.str] = None,
    temp_build_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5beab1443400ede62a629403d54e15d235c8d7e5e8675ca115a14d1897afe74a(
    *,
    image_cache_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy] = None,
    lambda_cache_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy] = None,
    static_cache_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy] = None,
    static_client_max_age_default: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3281f9f114cf2d3432895c9f007c24b74abbc116d63e7a103aa11263e265642(
    *,
    asset_deployment: typing.Any = None,
    distribution: typing.Any = None,
    lambda_: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96429686a12d62c6a68e5becfb0bb1fee7ad2eb8691d4394d55362a261b4c253(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_opt_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    next_build: NextjsBuild,
    server_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    static_assets_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    cache_policies: typing.Optional[typing.Union[NextjsCachePolicyProps, typing.Dict[builtins.str, typing.Any]]] = None,
    cdk: typing.Optional[typing.Union[NextjsDistributionCdkProps, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_domain: typing.Optional[typing.Union[builtins.str, typing.Union[NextjsDomainProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    function_url_auth_type: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionUrlAuthType] = None,
    origin_request_policies: typing.Optional[typing.Union[NextjsOriginRequestPolicyProps, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_prefix: typing.Optional[builtins.str] = None,
    stage_name: typing.Optional[builtins.str] = None,
    build_command: typing.Optional[builtins.str] = None,
    build_path: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_placeholder: typing.Optional[builtins.bool] = None,
    nextjs_path: typing.Optional[builtins.str] = None,
    next_js_path: typing.Optional[builtins.str] = None,
    node_env: typing.Optional[builtins.str] = None,
    open_next_path: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
    sharp_layer_arn: typing.Optional[builtins.str] = None,
    temp_build_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4f3e3041a6f9373eb4e476ca58b65574cd2fc90f10e0fe83eb833b55aa4c4b(
    value: _aws_cdk_aws_cloudfront_ceddda9d.OriginRequestPolicyProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6adf7f3d1cd4d7aa682ec6290c2383de65e020a5feb9c92694fa04db3bd04d27(
    value: _aws_cdk_aws_cloudfront_ceddda9d.CachePolicyProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc609a1f2cd4e3d6079cc5d3384f9c1b9c7a2b83d6b12b6f0f6598f78dfaec5(
    value: _aws_cdk_aws_cloudfront_ceddda9d.OriginRequestPolicyProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53820e7c1766a05033b5c7c3f60eac49d0ee4dac99da8aaaf8bcf4251a088708(
    value: _aws_cdk_aws_cloudfront_ceddda9d.CachePolicyProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394dfd623fd21e3cefb89b421c91ea0a1bff35a5b3ec33c4cd100e0a601cbd7a(
    value: _aws_cdk_aws_cloudfront_ceddda9d.OriginRequestPolicyProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5966ac5eec38e82772f0bc21221c45e008e0ef917275c9b23d95c0758b7d4eaa(
    value: _aws_cdk_aws_cloudfront_ceddda9d.CachePolicyProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2003bb843dee56635b51a213e2427a1fcc2c2a3ae2489c5b26a13cb1dd8f12(
    value: _aws_cdk_aws_cloudfront_ceddda9d.Distribution,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58db2de3e18d039ca31d58b4ea3e6374131689393d94e20487cb2a876c030565(
    value: NextjsDistributionProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f1468fcfbed7bd8a91f5d103f84be21de64720a4ffaf85d52d6c44f0de940d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84af5c3db1ff8f4257a5a8213acd077dfb03c8e3462adbabbe438b172dcaf2e0(
    value: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef90d5029061afa1511d648182b8db1a888e8a9ec071985f61b9162d9a23bf2(
    value: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ebd22500c4f1cf1308ccffff6700bea18f32e4ec0fb2bf6fbcf119f0ff1bdda(
    *,
    distribution: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.DistributionProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b78b297e19da3fbc794e6c49aae016184b97ec8bc8d7a0bde99ac5866d11dc(
    *,
    build_command: typing.Optional[builtins.str] = None,
    build_path: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_placeholder: typing.Optional[builtins.bool] = None,
    nextjs_path: typing.Optional[builtins.str] = None,
    next_js_path: typing.Optional[builtins.str] = None,
    node_env: typing.Optional[builtins.str] = None,
    open_next_path: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
    sharp_layer_arn: typing.Optional[builtins.str] = None,
    temp_build_dir: typing.Optional[builtins.str] = None,
    image_opt_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    next_build: NextjsBuild,
    server_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    static_assets_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    cache_policies: typing.Optional[typing.Union[NextjsCachePolicyProps, typing.Dict[builtins.str, typing.Any]]] = None,
    cdk: typing.Optional[typing.Union[NextjsDistributionCdkProps, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_domain: typing.Optional[typing.Union[builtins.str, typing.Union[NextjsDomainProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    function_url_auth_type: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionUrlAuthType] = None,
    origin_request_policies: typing.Optional[typing.Union[NextjsOriginRequestPolicyProps, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_prefix: typing.Optional[builtins.str] = None,
    stage_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2f0e8acb48dbe67528492a569aeedd131e85a109a90d1a0fb6b1ce7dc3d365(
    *,
    domain_name: builtins.str,
    alternate_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    domain_alias: typing.Optional[builtins.str] = None,
    hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
    is_external_domain: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b398354dc2cfe9832ff6a120234dbe8d3b199fc0b2d5d22bcf7dc901e36569d5(
    *,
    build_command: typing.Optional[builtins.str] = None,
    build_path: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_placeholder: typing.Optional[builtins.bool] = None,
    nextjs_path: typing.Optional[builtins.str] = None,
    next_js_path: typing.Optional[builtins.str] = None,
    node_env: typing.Optional[builtins.str] = None,
    open_next_path: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
    sharp_layer_arn: typing.Optional[builtins.str] = None,
    temp_build_dir: typing.Optional[builtins.str] = None,
    next_build: NextjsBuild,
    lambda_: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d1eedb1aeead6789283febfffae0b4de96a8e41458d224f4ffdedbffaf2c9b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b6529cd61a993ba5195a67f3a7a1ddfa195058990804f8623c4880b612ce474(
    *,
    fallback_origin_request_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy] = None,
    image_optimization_origin_request_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy] = None,
    lambda_origin_request_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014db87f37373e70d9930df2867cbc2bad2cafed8c75b1ffc138c1240a2fb0bf(
    *,
    build_command: typing.Optional[builtins.str] = None,
    build_path: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_placeholder: typing.Optional[builtins.bool] = None,
    nextjs_path: typing.Optional[builtins.str] = None,
    next_js_path: typing.Optional[builtins.str] = None,
    node_env: typing.Optional[builtins.str] = None,
    open_next_path: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
    sharp_layer_arn: typing.Optional[builtins.str] = None,
    temp_build_dir: typing.Optional[builtins.str] = None,
    defaults: typing.Optional[typing.Union[NextjsDefaultsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_optimization_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df1a18724360cf1749ec444d4ce6c18a8aa9328a161d3fa5a00db5c5c695ffb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    build_command: typing.Optional[builtins.str] = None,
    build_path: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_placeholder: typing.Optional[builtins.bool] = None,
    nextjs_path: typing.Optional[builtins.str] = None,
    next_js_path: typing.Optional[builtins.str] = None,
    node_env: typing.Optional[builtins.str] = None,
    open_next_path: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
    sharp_layer_arn: typing.Optional[builtins.str] = None,
    temp_build_dir: typing.Optional[builtins.str] = None,
    replacement_config: typing.Union[RewriteReplacementsConfig, typing.Dict[builtins.str, typing.Any]],
    s3_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    s3keys: typing.Sequence[builtins.str],
    cloudfront_distribution_id: typing.Optional[builtins.str] = None,
    debug: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c5f8577d14ba37a10e5749b77bcd6b33b7f45799e6087b1a7caa5c0127d7f8(
    value: typing.Optional[_constructs_77d1e7e8.Construct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa704f388c7acf1d06e8f3f9dd9607914e4e88881ed5b95b0ffa74c3589de118(
    *,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    json_s3_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    json_s3_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff83d6924e35bccbe4afc1591f0143870d4b7531b5aeea0eccd14ab8c37c7bf(
    *,
    replacement_config: typing.Union[RewriteReplacementsConfig, typing.Dict[builtins.str, typing.Any]],
    s3_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    s3keys: typing.Sequence[builtins.str],
    cloudfront_distribution_id: typing.Optional[builtins.str] = None,
    debug: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710ec40c82cf50feb374c3f2e6241ae54a2573c4abba6b30508027a8581722a1(
    *,
    build_command: typing.Optional[builtins.str] = None,
    build_path: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_placeholder: typing.Optional[builtins.bool] = None,
    nextjs_path: typing.Optional[builtins.str] = None,
    next_js_path: typing.Optional[builtins.str] = None,
    node_env: typing.Optional[builtins.str] = None,
    open_next_path: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
    sharp_layer_arn: typing.Optional[builtins.str] = None,
    temp_build_dir: typing.Optional[builtins.str] = None,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    next_build: NextjsBuild,
    lambda_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae64d307733915cb668ea5f338f12bc80df41ff63e405ab971fc71674b0aa622(
    *,
    build_command: typing.Optional[builtins.str] = None,
    build_path: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_placeholder: typing.Optional[builtins.bool] = None,
    nextjs_path: typing.Optional[builtins.str] = None,
    next_js_path: typing.Optional[builtins.str] = None,
    node_env: typing.Optional[builtins.str] = None,
    open_next_path: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
    sharp_layer_arn: typing.Optional[builtins.str] = None,
    temp_build_dir: typing.Optional[builtins.str] = None,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    next_build: NextjsBuild,
    cache_policies: typing.Optional[typing.Union[NextjsAssetsCachePolicyProps, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    memory_limit: typing.Optional[jsii.Number] = None,
    prune: typing.Optional[builtins.bool] = None,
    use_efs: typing.Optional[builtins.bool] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0323bdd0d73ebcdc84ea335a90b20eae8c790d19dda7c0e320c8bbb3d2212369(
    *,
    build_command: typing.Optional[builtins.str] = None,
    build_path: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    is_placeholder: typing.Optional[builtins.bool] = None,
    nextjs_path: typing.Optional[builtins.str] = None,
    next_js_path: typing.Optional[builtins.str] = None,
    node_env: typing.Optional[builtins.str] = None,
    open_next_path: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
    sharp_layer_arn: typing.Optional[builtins.str] = None,
    temp_build_dir: typing.Optional[builtins.str] = None,
    replacement_config: typing.Union[RewriteReplacementsConfig, typing.Dict[builtins.str, typing.Any]],
    s3_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    s3keys: typing.Sequence[builtins.str],
    cloudfront_distribution_id: typing.Optional[builtins.str] = None,
    debug: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
