from typing import List, Any

from botocore.exceptions import ClientError

from boto3 import session

__author__ = "Dheeraj Banodha"
__version__ = '0.2.6'

import logging

from aws_recommendation.cloudwatch import cloudwatch
from aws_recommendation.dynamodb import dynamodb
from aws_recommendation.ebs import ebs
from aws_recommendation.ec2 import ec2
from aws_recommendation.elb import elb
from aws_recommendation.kms import kms
from aws_recommendation.rds import rds
from aws_recommendation.redshift import redshift
from aws_recommendation.s3 import s3
from aws_recommendation.utils import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class aws_client(utils, cloudwatch, s3, rds, ec2, dynamodb, ebs, elb, kms, redshift):
    def __init__(self, **kwargs):
        if 'aws_access_key_id' in kwargs.keys() and 'aws_secret_access_key' in kwargs.keys():
            self.session = session.Session(
                aws_access_key_id=kwargs['aws_access_key_id'],
                aws_secret_access_key=kwargs['aws_secret_access_key'],
            )
        elif 'profile_name' in kwargs.keys():
            self.session = session.Session(profile_name=kwargs['profile_name'])

    from .cost_estimations import estimated_savings

    # Merge the recommendations and return the list
    def get_recommendations(self) -> list:
        recommendations: list[Any] = []
        regions = self.get_regions()

        ec2_instances = self.list_instances(regions)

        recommendations += self.get_s3_recommendations()
        recommendations += self.get_cw_recommendations(regions=regions)
        recommendations += self.get_rds_recommendations(regions=regions)
        recommendations += self.get_ec2_recommendations(regions=regions, ec2_instances=ec2_instances)
        recommendations += self.get_dynamodb_recommendations(regions=regions)
        recommendations += self.estimated_savings(regions=regions, ec2_instances=ec2_instances)
        recommendations += self.get_ebs_recommendations(regions=regions)
        recommendations += self.get_elb_recommendations(regions)
        recommendations += self.get_kms_recommendations(regions)
        recommendations += self.get_redshift_recommendations(regions)

        return recommendations




