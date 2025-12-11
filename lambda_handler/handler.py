import json
import os
import boto3

s3 = boto3.client('s3')

file_rules = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Documents': ['.pdf', '.docx', '.txt'],
    'Videos': ['.mp4', '.mov'],
}

def lambda_handler(event, context):
    # 1. Extract bucket + key from S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key     = event['Records'][0]['s3']['object']['key']

    # 2. Skip files already in categorized folders
    if any(key.startswith(f + '/') for f in file_rules.keys()):
        print(f"Skipping {key}, already in correct folder.")
        return

    # 3. Get extension and determine destination
    file_extension = os.path.splitext(key)[1].lower()
    destination_folder = "Others"

    for category, extensions in file_rules.items():
        if file_extension in extensions:
            destination_folder = category
            break

    # 4. Build new path
    new_key = f"{destination_folder}/{os.path.basename(key)}"

    # 5. Move file (copy + delete)
    try:
        s3.copy_object(
            Bucket=bucket,
            CopySource={'Bucket': bucket, 'Key': key},
            Key=new_key
        )
        s3.delete_object(Bucket=bucket, Key=key)
        print(f"SUCCESS: Moved {key} -> {new_key}")

    except Exception as e:
        print(f"ERROR processing {key}: {str(e)}")
        raise e

    return {
        'statusCode': 200,
        'body': json.dumps(f"File organization complete: {new_key}")
    }

