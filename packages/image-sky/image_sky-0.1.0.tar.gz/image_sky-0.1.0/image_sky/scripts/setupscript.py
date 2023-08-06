#
# Copyright 2018 PyWren Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import getpass
import random
import re
import time

import boto3
import click
import oss2

import image_sky.wrenconfig
from image_sky.fun_client import fun_client
from image_sky.scripts import pywrencli


def get_username():
    return getpass.getuser()

def click_validate_prompt(message, default, validate_func,
                          fail_msg="", max_attempts=5):
    """
    Click wrapper that repeats prompt until acceptable answer
    """
    attempt_num = 0
    while True:
        res = click.prompt(message, default)
        if validate_func(res):
            return res
        else:
            attempt_num += 1
            if attempt_num >= max_attempts:
                raise Exception("Too many invalid answers")
            if fail_msg != "":
                click.echo(fail_msg.format(res))


def check_aws_region_valid(regions):
    #return aws_region_str in get_lambda_regions()
    return True

def check_service_name(service_name):
    return True


def check_user_id(user_id):
    return True


# def check_service_name_valid(service_name, access_key_id, access_key_secret):
#     client = fun_client.create_client(access_key_id, access_key_secret)
#     fun_client.get_service(client, service_name)
#     return True


def check_overwrite_function(filename):
    filename = os.path.expanduser(filename)
    if os.path.exists(filename):
        return click.confirm("{} already exists, would you like to overwrite?".format(filename))
    return True

def check_bucket_exists(s3bucket, accessKeyID, accessKeySecret, endpoint):
    """
    This is the recommended boto3 way to check for bucket
    existence:
    http://boto3.readthedocs.io/en/latest/guide/migrations3.html
    """
    auth = oss2.Auth(accessKeyID, accessKeySecret)
    bucket = oss2.Bucket(auth, endpoint, s3bucket)
    exists = True
    try:
        bucket.get_bucket_info()
    except oss2.exceptions.NoSuchBucket as e:
        error_code = e.status
        if error_code == 404:
            exists = False
    except Exception as e:
        raise e
    return exists

def create_unique_bucket_name():
    bucket_name = "{}-image_sky-{}".format(get_username().lower(),
                                        random.randint(0, 999))
    return bucket_name

def check_valid_bucket_name(bucket_name):
    # Validates bucketname
    # Based on http://info.easydynamics.com/blog/aws-s3-bucket-name-validation-regex
    # https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html
    bucket_regex = re.compile(r"""^([a-z]|(\d(?!\d{0,2}\.\d{1,3}\.\d{1,3}\.\d{1,3})))
                                   ([a-z\d]|(\.(?!(\.|-)))|(-(?!\.))){1,61}[a-z\d\.]$""", re.X)
    if re.match(bucket_regex, bucket_name):
        return True
    return False

def validate_s3_prefix(prefix): # pylint: disable=unused-argument
    # FIXME
    return True

def validate_lambda_function_name(function_name): # pylint: disable=unused-argument
    # FIXME
    return True

def validate_lambda_role_name(role_name): # pylint: disable=unused-argument
    # FIXME
    return True

@click.command()
@click.option('--dryrun', default=False, is_flag=True, type=bool,
              help='create config file but take no actions')
@click.option('--suffix', default="", type=str,
              help="suffix to use for all automatically-generated named entities, " + \
                   "useful for helping with IAM roles, and automated testing")
@click.pass_context
def interactive_setup(ctx, dryrun, suffix):


    def ds(key):
        """
        Debug suffix for defaults. For automated testing,
        automatically adds a suffix to each default
        """
        return "{}{}".format(key, suffix)


    click.echo("This is the PyWren interactive setup script")
    #first we will try and make sure AWS is set up

    # account_id = ctx.invoke(pywrencli.get_aws_account_id, False)
    # click.echo("Your AWS configuration appears to be set up, and your account ID is {}".format(
    #     account_id))

    click.echo("This interactive script will set up your initial PyWren configuration.")
    click.echo("If this is the first time you are using PyWren then accepting the defaults " + \
               "should be fine.")

    # first, what is your default AWS region?
    aws_region = click_validate_prompt(
        "What is your default aws region?",
        default=image_sky.wrenconfig.AWS_REGION_DEFAULT,
        validate_func=check_aws_region_valid,
        #fail_msg="{} not a valid aws region. valid regions are " + " ".join(get_lambda_regions())
    )
    # # FIXME make sure this is a valid region
    #aws_region = "cn-beijing"

    accessKeyID, accessKeySecret, endpoint = ctx.invoke(pywrencli.get_aws_account_id)

    user_id = click_validate_prompt(
        "What is your user_id?",
        default=image_sky.wrenconfig.USER_ID,
        validate_func=check_user_id,
        # fail_msg="{} not a valid aws region. valid regions are " + " ".join(get_lambda_regions())
    )


    service_name = click_validate_prompt(
        "What is your service_name?",
        default=image_sky.wrenconfig.SERVICE_NAME,
        validate_func=check_service_name,
        #fail_msg="{} not a valid aws region. valid regions are " + " ".join(get_lambda_regions())
    )

    # if not check_service_name_valid(service_name, accessKeyID, accessKeySecret):
    #     print(service_name + " not a valid service_name ")
    #     raise Exception(service_name + " not a valid service_name ")

    # if config file exists, ask before overwriting
    config_filename = click_validate_prompt(
        "Location for config file: ",
        default=image_sky.wrenconfig.get_default_home_filename(),
        validate_func=check_overwrite_function)
    config_filename = os.path.expanduser(config_filename)

    s3_bucket = click_validate_prompt(
        "PyWren requires an s3 bucket to store intermediate data. " + \
            "What s3 bucket would you like to use?",
        default=create_unique_bucket_name(),
        validate_func=check_valid_bucket_name)
    create_bucket = False
    if not check_bucket_exists(s3_bucket, accessKeyID, accessKeySecret, endpoint):
        create_bucket = click.confirm(
            "Bucket does not currently exist, would you like to create it?", default=True)

    click.echo("PyWren prefixes every object it puts in S3 with a particular prefix.")
    bucket_pywren_prefix = click_validate_prompt(
        "PyWren s3 prefix: ",
        default=image_sky.wrenconfig.AWS_S3_PREFIX_DEFAULT,
        validate_func=validate_s3_prefix)

    lambda_config_advanced = click.confirm(
        "Would you like to configure advanced PyWren properties?", default=False)
    lambda_role = ds(image_sky.wrenconfig.AWS_LAMBDA_ROLE_DEFAULT)
    function_name = ds(image_sky.wrenconfig.AWS_LAMBDA_FUNCTION_NAME_DEFAULT)

    if lambda_config_advanced:
        lambda_role = click_validate_prompt(
            "Each lambda function runs as a particular"
            "IAM role. What is the name of the role you"
            "would like created for your lambda",
            default=lambda_role,
            validate_func=validate_lambda_role_name)
        function_name = click_validate_prompt(
            "Each lambda function has a particular function name."
            "What is your function name?",
            default=function_name,
            validate_func=validate_lambda_function_name)
    click.echo("PyWren standalone mode uses dedicated AWS instances to run PyWren tasks. " + \
               "This is more flexible, but more expensive with fewer simultaneous workers.")
    # use_standalone = click.confirm("Would you like to enable PyWren standalone mode?")

    click.echo("Creating config {}".format(config_filename))
    ctx.obj = {"config_filename" : config_filename}
    ctx.invoke(pywrencli.create_config,
               aws_region=aws_region,
               service_name=service_name,
               bucket_name=s3_bucket,
               lambda_role=lambda_role,
               function_name=function_name,
               bucket_prefix=bucket_pywren_prefix,
               accessKeyID=accessKeyID,
               accessKeySecret=accessKeySecret,
               endpoint=endpoint,
               user_id=user_id,
               force=True)
    if dryrun:
        click.echo("dryrun is set, not manipulating cloud state.")
        return

    if create_bucket:
        click.echo("Creating bucket {}.".format(s3_bucket))
        ctx.invoke(pywrencli.create_bucket)
    # click.echo("Creating role.")
    # ctx.invoke(pywrencli.create_role)
    click.echo("Deploying lambda.")
    ctx.invoke(pywrencli.deploy_lambda)

    # if use_standalone:
    #     click.echo("Setting up standalone mode.")
    #     ctx.invoke(pywrencli.create_queue)
    #     ctx.invoke(pywrencli.create_ec2_ssh_key)
    #     ctx.invoke(pywrencli.create_instance_profile)
    click.echo("Pausing for 10 sec for changes to propagate.")
    time.sleep(10)
    ctx.invoke(pywrencli.test_function)

if __name__ == '__main__':
    interactive_setup() # pylint: disable=no-value-for-parameter
