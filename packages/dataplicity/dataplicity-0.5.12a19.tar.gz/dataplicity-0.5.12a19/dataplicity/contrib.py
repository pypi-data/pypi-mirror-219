import urllib3
import json
import logging

from collections import namedtuple

Response = namedtuple('Response', ['data', 'status_code', 'ok'])

log = logging.getLogger(__name__)
http = urllib3.PoolManager()


def requests_post_json(url, data, headers=None):
    if not headers:
        headers = {'Content-Type': 'application/json'}
    log.debug("Sending POST to %s / %s", url, data)

    response = http.request(
        'POST',
        url,
        body=json.dumps(data),
        headers=headers,
    )

    log.debug("Response [status: %s] data: %s", response.status, response.data)

    try:
        json_data = json.loads(response.data.decode('utf-8'))
    except:
        json_data = response.data

    return Response(
        data=json_data,
        status_code=response.status,
        ok=str(response.status)[0] == '2'
    )


def requests_get_json(url, headers):
    if not headers:
        headers = {'Content-Type': 'application/json'}
    response = http.request(
        'GET',
        url,
        headers=headers,
    )
    try:
        data = json.loads(response.data.decode('utf-8'))
    except:  # TODO: exception more restrictive
        data = response.data

    return Response(
        data=data,
        status_code=response.status,
        ok=str(response.status)[0] == "2"
    )

