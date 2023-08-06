import logging

from botocore.exceptions import ClientError

from aws_recommendation.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class redshift:
    def get_redshift_recommendations(self, regions=None):
        """
        :param regions:
        :return:
        """
        logger.info(" ---Inside redshift :: get_redshift_recommendations()--- ")

        if regions is None:
            regions = self.get_regions()

        return self.under_utilized_redshift_cluster(regions)

    # Generated recommendation for under utilized redshift cluster
    def under_utilized_redshift_cluster(self, regions) -> list:
        """
        :param regions:
        :param self:
        :return:
        """
        logger.info(" ---Inside redshift :: under_utilized_redshift_cluster()")

        recommendation = []

        for region in regions:
            try:
                client = self.session.client('redshift', region_name=region)
                clusters = self.list_redshift_clusters(client)

                for cluster in clusters:
                    cpu_datapoints = self.get_metrics_stats(
                        region=region,
                        namespace='AWS/Redshift',
                        dimensions=[{'Name': 'ClusterIdentifier', 'Value': cluster['ClusterIdentifier']}],
                        metric_name='CPUUtilization',
                        period=3600,
                        stats=["Average"]
                    )
                    flag = True
                    for datapoint in cpu_datapoints['Datapoints']:
                        if datapoint['Average'] > 60:
                            flag = False
                            break

                    if flag:
                        read_datapoints = self.get_metrics_stats(
                            region=region,
                            namespace='AWS/Redshift',
                            dimensions=[{'Name': 'ClusterIdentifier', 'Value': cluster['ClusterIdentifier']}],
                            metric_name='ReadIOPS',
                            period=3600,
                            stats=["Sum"]
                        )
                        readOps_sum = 0
                        for datapoint in read_datapoints['Datapoints']:
                            readOps_sum = readOps_sum +  datapoint['Sum']

                        if readOps_sum > 100:
                            flag = False

                    if flag:
                        write_datapoints = self.get_metrics_stats(
                            region=region,
                            namespace='AWS/Redshift',
                            dimensions=[{'Name': 'ClusterIdentifier', 'Value': cluster['ClusterIdentifier']}],
                            metric_name='WriteIOPS',
                            period=3600,
                            stats=["Sum"]
                        )
                        writeOps_sum = 0
                        for datapoint in write_datapoints['Datapoints']:
                            writeOps_sum = writeOps_sum + datapoint['Sum']

                        if writeOps_sum > 100:
                            flag = False

                    if flag:
                        try:
                            tags = cluster['Tags']
                        except KeyError:
                            tags = None
                        temp = {
                            'Service Name': 'Redshift',
                            'Id': cluster['ClusterIdentifier'],
                            'Recommendation': 'Consider shutting down the cluster and taking a final snapshot, or downsizing the cluster',
                            'Description': 'TChecks your Amazon Redshift configuration for clusters that appear to be underutilized',
                            'Metadata': {
                                'Region': region,
                                'Node Type': cluster['NodeType'],
                                'Tags': tags,
                            },
                            'Recommendation Reason': {
                                'Average CPU Datapoints(7 days)': [float('{:.2f}'.format(x['Average'])) for x in cpu_datapoints['Datapoints']],
                                'Total ReadOps': readOps_sum,
                                'Total WriteOps': writeOps_sum
                            },
                            'Risk': 'High',
                            'Savings': None,
                            'Source': 'Klera',
                            'Category': 'Cost Optimization'
                        }
                        recommendation.append(temp)

            except ClientError as e:
                if e.response['Error']['Code'] == 'AccessDenied' or e.response['Error']['Code'] == 'AccessDeniedException':
                    logger.info('---------Redshift read access denied----------')
                    temp = {
                        'Service Name': 'Redshift',
                        'Id': 'Access Denied',
                        'Recommendation': 'Access Denied',
                        'Description': 'Access Denied',
                        'Metadata': {
                            'Access Denied'
                        },
                        'Recommendation Reason': {
                            'Access Denied'
                        },
                        'Risk': 'High',
                        'Savings': None,
                        'Source': 'Klera',
                        'Category': 'Cost Optimization'
                    }
                    recommendation.append(temp)
                    return recommendation
                logger.error("Something went wrong with the region {}: {}".format(region, e))

        return recommendation