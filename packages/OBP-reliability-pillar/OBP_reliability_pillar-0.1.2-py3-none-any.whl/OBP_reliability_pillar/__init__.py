from boto3 import session

from OBP_reliability_pillar.cloudwatch import cloudwatch
from OBP_reliability_pillar.dynamodb import dynamodb
from OBP_reliability_pillar.elastic_beanstalk import elastic_beanstalk
from OBP_reliability_pillar.elastic_load_balancer import elb
from OBP_reliability_pillar.rds import rds
from OBP_reliability_pillar.ec2 import ec2
from OBP_reliability_pillar.redshift import redshift
from OBP_reliability_pillar.s3 import s3
# from OBP_reliability_pillar.security_hub import security_hub
from OBP_reliability_pillar.auto_scaling import auto_scaling
from OBP_reliability_pillar.lambdafn import lambdafn
from OBP_reliability_pillar.guard_duty import guard_duty
from OBP_reliability_pillar.elastic_search import elastic_search

__version__ = '0.1.2'
__author__ = 'Dheeraj Banodha'

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class aws_client(elb, dynamodb, cloudwatch, rds, guard_duty, elastic_search,
                 ec2, s3, elastic_beanstalk, redshift, auto_scaling, lambdafn):
    def __init__(self, **kwargs):
        """

        @param str aws_access_key_id: AWS Access Key ID
        @param str aws_secret_access_key: AWS Secret Access Key
        """

        if 'aws_access_key_id' in kwargs.keys() and 'aws_secret_access_key' in kwargs.keys():
            self.session = session.Session(
                aws_access_key_id=kwargs['aws_access_key_id'],
                aws_secret_access_key=kwargs['aws_secret_access_key'],
            )
        elif 'profile_name' in kwargs.keys():
            self.session = session.Session(profile_name=kwargs['profile_name'])

        elb.__init__(elb, self.session)
        dynamodb.__init__(dynamodb, self.session)
        cloudwatch.__init__(cloudwatch, self.session)
        rds.__init__(rds, self.session)
        ec2.__init__(ec2, self.session)
        s3.__init__(s3, self.session)
        elastic_beanstalk.__init__(elastic_beanstalk, self.session)
        redshift.__init__(redshift, self.session)
        # security_hub.__init__(security_hub, self.session)
        auto_scaling.__init__(auto_scaling, self.session)
        lambdafn.__init__(lambdafn, self.session)
        guard_duty.__init__(guard_duty, self.session)
        elastic_search.__init__(elastic_search, self.session)

    # consolidate compliance.py details
    def get_compliance(self) -> list:
        """
        :return list: consolidated list  of compliance.py checks
        """

        regions = self.get_regions()

        compliance = []
        compliance.extend(self.dynamodb_compliance(regions))
        compliance.extend(self.elb_compliance(regions))
        compliance.extend(self.cloudwatch_compliance(regions))
        compliance.extend(self.rds_compliance(regions))
        compliance.extend(self.ec2_compliance(regions))
        compliance.extend(self.s3_compliance())
        compliance.extend(self.elastic_beanstalk_compliance(regions))
        compliance.extend(self.redshift_compliance(regions))
        compliance.extend(self.auto_scaling_compliance(regions))
        # compliance.extend(self.security_hub_enabled())
        compliance.extend(self.lambda_compliance(regions))
        compliance.extend(self.guard_duty_compliance())
        compliance.extend(self.elastic_search_compliance(regions))

        return compliance

    def get_regions(self):
        logger.info(" ---Inside utils :: get_regions()--- ")
        """Summary

        Returns:
            TYPE: Description
        """

        client = self.session.client('ec2', region_name='us-east-1')
        region_response = {}
        # try:
        region_response = client.describe_regions()
        # except botocore.exceptions.ClientError as error:
        #     if error.response['Error']['Code'] == 'AuthFailure':
        #         logger.error(f" AccessKey credentails not found here: {error}")
        #         return {
        #             'Result': 'Auth Failure',
        #             'failReason': 'Auth Failure',
        #             'Offenders': [],
        #             'ScoredControl': False,
        #             'Description': 'Auth Failure',
        #             'ControlId': 'Auth Failure'
        #         }
        # except botocore.exceptions.NoCredentialsError as e:
        #     logger.error(f" Unable to locate credentials: {e} ")
        #     return {
        #         'Result': 'Auth Failure',
        #         'failReason': 'Auth Failure',
        #         'Offenders': [],
        #         'ScoredControl': False,
        #         'Description': 'Auth Failure',
        #         'ControlId': 'Auth Failure'
        #     }

        logger.debug(region_response)
        regions = [region['RegionName'] for region in region_response['Regions']]
        return regions
