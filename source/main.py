import boto3

ec2 = boto3.client('ec2')
route53 = boto3.client('route53')

def lambda_handler(event, context):

    instance_id = event['detail']['instance-id']
    state = event['detail']['state']

    # get from ec2 tag
    instance = ec2.describe_instances(InstanceIds=[instance_id])
    try:
        tags = instance['Reservations'][0]['Instances'][0]['Tags']
    except:
        tags = []

    public_dns_name = None
    public_host_name = None
    private_dns_name = None
    private_host_name = None
    zone_id = None
    private_zone_id = None

    for tag in tags:
        if tag['Key'] == 'PublicDNS':
            public_dns_name = tag['Value']
        elif tag['Key'] == 'PublicHost':
            public_host_name = tag['Value']
        elif tag['Key'] == 'PrivateDNS':
            private_dns_name = tag['Value']
        elif tag['Key'] == 'PrivateHost':
            private_host_name = tag['Value']

    if public_dns_name:
        zone_id = get_zone_id(public_dns_name,False)

    if private_dns_name:
        private_zone_id = get_zone_id(private_dns_name,True)

    if state == 'running':
        # Get instance attributes
        try:
            private_ip = instance['Reservations'][0]['Instances'][0]['PrivateIpAddress']
            public_ip = instance['Reservations'][0]['Instances'][0]['PublicIpAddress']
        except BaseException as e:
            print('Instance has no private or public IP:', e)
        if zone_id:
            create_resource_record(zone_id,public_host_name,public_dns_name,'A',public_ip)
        if private_zone_id:
            create_resource_record(private_zone_id,private_host_name,private_dns_name,'A',private_ip)
    elif state == 'terminated':
        if zone_id:
            delete_resource_record(zone_id,public_host_name,public_dns_name,'A')
        if private_zone_id:
            delete_resource_record(private_zone_id,private_host_name,private_dns_name,'A')


"""
This function returns the zone id for the zone name that's passed into the function.
"""
def get_zone_id(zone_name,privatezone):
    if zone_name[-1] != '.':
        zone_name = zone_name + '.'
    hosted_zones = route53.list_hosted_zones()
    x = list(filter(lambda record: record['Name'] == zone_name and record['Config']['PrivateZone'] is privatezone, hosted_zones['HostedZones']))
    try:
        zone_id_long = x[0]['Id']
        zone_id = str.split(str(zone_id_long),'/')[2]
        return zone_id
    except:
        return None

"""
This function creates resource records in the hosted zone passed by the calling function.
"""
def create_resource_record(zone_id, host_name, hosted_zone_name, type, value):
    print('Updating %s record %s in zone %s ' % (type, host_name, hosted_zone_name))
    if host_name[-1] != '.':
        host_name = host_name + '.'
    route53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            "Comment": "Updated by Lambda DDNS",
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": host_name + hosted_zone_name,
                        "Type": type,
                        "TTL": 60,
                        "ResourceRecords": [
                            {
                                "Value": value
                            },
                        ]
                    }
                },
            ]
        }
    )

"""
This function deletes resource records from the hosted zone passed by the calling function.
"""
def delete_resource_record(zone_id, host_name, hosted_zone_name, type):
    print('Deleting %s record %s in zone %s' % (type, host_name, hosted_zone_name))
    if host_name[-1] != '.':
        host_name = host_name + '.'
    r = route53.list_resource_record_sets(
            HostedZoneId=zone_id,
            StartRecordName=host_name + hosted_zone_name + '.',
            StartRecordType=type,
            MaxItems='1'
        )
    for sp_key,sp_val in r.items():
        if sp_key == 'ResourceRecordSets':
            value = sp_val[0]['ResourceRecords'][0]['Value']

    route53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            "Comment": "Updated by Lambda DDNS",
            "Changes": [
                {
                    "Action": "DELETE",
                    "ResourceRecordSet": {
                        "Name": host_name + hosted_zone_name,
                        "Type": type,
                        "TTL": 60,
                        "ResourceRecords": [
                            {
                                "Value": value
                            },
                        ]
                    }
                },
            ]
        }
    )
