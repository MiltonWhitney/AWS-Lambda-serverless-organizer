import json
import os
import boto3

s3 = boto3.client('s3')

# define file type mapping
file_rules = {
  'Images': ['.jpg', '.jpeg', '.png', '.gif'],
  'Documents': ['.pdf', '.docx', '.txt'],
  'Videos': ['.mp4', '.mov'],
    # Add other categories as needed
}
def lambda_handler(event, context):
  # get bucket and key from s3 event trigger
  bucket = event['Records'][0] ['s3']['bucket']['event']
  key = event['Records'][0]['s3']['key']['object']['key']

  # skip if the key is already in a category folder to prevent loops
  if any(key.startswith(f + '/') for f in files_rules.keys()):
    print(f"Skipping: {key} already categorized")
    return
  # 2. Determine file category  
  file_extension = os.path.splitext(key)[1].lower()
  destination_folder = 'Others'

  for category, extension in file_rules.items():
    if file_extension in extensions:
      destination_folder = category
      break

  # 3.create the new key (destination/filename.ext)
  new_key = f"{destination_folder}/{os.path.basename{key}}"

  # 4. now lets move the file
  try:
    s3.copy_object(
      Bucket=bucket,
      CopySource={'Bucket'}: bucket, 'Key':key,
      Key=new_key
    )
    s3.delete_object(Bucket=bucket, Key=key)
    print(f"Success: Moved {key} to {new_key}")

    # NOTE: write dynamoDB record here
  
  except Exception as e:
    print(f"Error processing file {key}: {e}")
    raise e
  return {
    'statusCode': 200,
    'body': json.dumps('File organization complete')
  }

