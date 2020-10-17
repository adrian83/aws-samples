import boto3
import sys

maxVersions = 30

versionsLabel = "Versions"
versionIdLabel = "VersionId"
nextVersionIdMarkerLabel = "NextVersionIdMarker"


bucket = sys.argv[1]
obj = sys.argv[2]

print("Removing object {0} from bucket {1}".format(obj, bucket))

client = boto3.client('s3')

nextVersionIdMarker = None

while True:

    response = client.list_object_versions( \
        Bucket=bucket, MaxKeys=5, KeyMarker=obj, Prefix=obj, VersionIdMarker=nextVersionIdMarker) \
        if nextVersionIdMarker else client.list_object_versions(Bucket=bucket, MaxKeys=5, Prefix=obj)

    if versionsLabel not in response:
        print("No {} in response. Exiting...".format(versionsLabel))
        sys.exit(0)

    versions = response[versionsLabel]

    for version in versions:
        version = version[versionIdLabel]
        delResp = client.delete_object(Bucket=bucket, Key=obj, VersionId=version)
        print("Object {0} with version {1} from bucket {2} removed".format(obj, version, bucket))


    if nextVersionIdMarkerLabel not in response:
        print("No more versions to fetch. Exiting...")
        sys.exit(0)

    nextVersionIdMarker = response[nextVersionIdMarkerLabel]