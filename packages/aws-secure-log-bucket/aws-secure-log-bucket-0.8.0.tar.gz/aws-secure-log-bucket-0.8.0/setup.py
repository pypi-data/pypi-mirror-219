import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-secure-log-bucket",
    "version": "0.8.0",
    "description": "secure multiple transition phases in a single lifecycle policy bucket.",
    "license": "Apache-2.0",
    "url": "https://github.com/yicr/aws-secure-log-bucket.git",
    "long_description_content_type": "text/markdown",
    "author": "yicr<yicr@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/yicr/aws-secure-log-bucket.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_secure_log_bucket",
        "aws_secure_log_bucket._jsii"
    ],
    "package_data": {
        "aws_secure_log_bucket._jsii": [
            "aws-secure-log-bucket@0.8.0.jsii.tgz"
        ],
        "aws_secure_log_bucket": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.61.0, <3.0.0",
        "aws-secure-bucket>=0.7.1, <0.8.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.84.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
