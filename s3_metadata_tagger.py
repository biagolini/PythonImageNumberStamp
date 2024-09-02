# Import libraries
import boto3
from urllib.parse import urlparse
# Import configs
import config as cf

# Adds or updates metadata for all objects in a specified S3 prefix
def add_metadata_to_s3_objects(bucket_name, bucket_path, user_defined_metadata, system_defined_metadata=None):
    # Initialize the S3 client
    s3_client = boto3.client('s3')

    # List all objects within the specified prefix
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=bucket_path)
    
    if 'Contents' not in response:
        print("No objects found in the specified path.")
        return
    
    # Iterate over each object in the path
    for obj in response['Contents']:
        object_key = obj['Key']

        # Skip directory-like objects
        if object_key.endswith('/'):
            print(f"Skipping directory-like object {object_key}")
            continue
        
        # Get the current metadata
        head_object = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        current_metadata = head_object['Metadata']

        # Update the metadata with new values
        new_metadata = current_metadata.copy()
        new_metadata.update(user_defined_metadata)

        # Set system-defined metadata if provided
        extra_args = {'MetadataDirective': 'REPLACE', 'Metadata': new_metadata}
        if system_defined_metadata:
            # Ensure the keys are using the correct names
            if 'Cache-Control' in system_defined_metadata:
                extra_args['CacheControl'] = system_defined_metadata['Cache-Control']
        
        # Copy the object to itself with the new metadata
        s3_client.copy_object(
            Bucket=bucket_name,
            CopySource={'Bucket': bucket_name, 'Key': object_key},
            Key=object_key,
            **extra_args
        )
        
        print(f"Updated metadata for {object_key}")

# Call the function with the imported configuration
add_metadata_to_s3_objects(cf.bucket_name, cf.bucket_path, cf.user_defined_metadata, cf.system_defined_metadata)
