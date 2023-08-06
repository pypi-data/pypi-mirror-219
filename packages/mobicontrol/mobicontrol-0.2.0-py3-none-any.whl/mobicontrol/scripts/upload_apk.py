from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import json

LF = "\r\n"
BOUNDARY = "mc_boundary"


def get_package_upload_data(token: str, file: bytes, filename) -> MIMEMultipart:
    message = get_apk_upload_data(token, file, filename)

    metadata = MIMEBase("application", "vnd.android.application.metadata+json")
    metadata.set_payload(json.dumps({"DeviceFamily": "AndroidPlus"}))
    del metadata["mime-version"]
    message.attach(metadata)

    return message


def get_apk_upload_data(token: str, file: bytes, filename) -> MIMEMultipart:
    message = MIMEMultipart("related", charset="utf-8", boundary=BOUNDARY)

    message.add_header("Authorization", f"Bearer {token}")
    message.add_header("Accept", "application/json")
    message.add_header("Content-Disposition", f"attachment; filename={filename}")

    binary_file = MIMEBase("application", "vnd.android.application")
    binary_file["Content-Type-Encoding"] = "base64"
    binary_file["Content-Disposition"] = f'attachment; filename="{filename}"'
    binary_file.set_payload(file)
    del binary_file["mime-version"]

    message.attach(binary_file)

    return message
