from google.cloud import storage
from io import BytesIO


def upload_to_gcs(content: bytes, bucket_name: str, blob_name: str) -> str:
    """
    Uploads in-memory content to a Google Cloud Storage bucket.

    Args:
        content: The content to upload, as bytes.
        bucket_name: The name of the GCS bucket.
        blob_name: The desired name of the object (blob) in the bucket.

    Returns:
        The GCS URI of the uploaded file (e.g., "gs://bucket-name/blob-name").
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Use BytesIO to treat the byte content like a file
    content_stream = BytesIO(content)

    print(f"Uploading to gs://{bucket_name}/{blob_name}...")
    blob.upload_from_file(content_stream, content_type="audio/mpeg")
    print("Upload successful.")

    return f"gs://{bucket_name}/{blob_name}"