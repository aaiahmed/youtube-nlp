"""
Provides a youtube client.
"""

import os
import googleapiclient.discovery
import googleapiclient.errors

from utils.config import get_config

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

conf = get_config()
api_service_name = conf['youtube']['api_service_name']
api_version = conf['youtube']['api_version']
api_key = os.getenv("GOOGLE_API_KEY")


def get_client():
    """Returns a youtube client. """

    return googleapiclient.discovery.build(
        serviceName=api_service_name,
        version=api_version,
        developerKey=api_key)


def main():
    get_client()


if __name__ == "__main__":
    main()
