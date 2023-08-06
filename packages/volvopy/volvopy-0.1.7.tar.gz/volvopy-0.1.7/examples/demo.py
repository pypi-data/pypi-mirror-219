#!/usr/bin/env python3

import json
import pprint
import syslog

import mausy5043_common.funfile as mf
import requests
import volvopy  # noqa

pp2 = pprint.PrettyPrinter(sort_dicts=False, indent=1, depth=2)
DEBUG = True
MYAPP = volvopy.MYAPP
MYID = "demo"



def main():
    """Demonstrate use of the Volvo APIs"""

    print(f"Calling: {call_url}\n")
    accept = "application/json"
    headers = {
        "Content-type": "application/json",
        "Accept": f"{accept}",
        "authorization": f"Bearer {api_token}",
        "vcc-api-key": api_primary_key,
    }

    response = requests.get(call_url, headers=headers, timeout=10)
    if DEBUG:
        mf.syslog_trace(f"Response Status Code: {response.status_code}", False, DEBUG)
        for key in response.headers:
            mf.syslog_trace(f"   {key} :: {response.headers[key]}", False, DEBUG)
        mf.syslog_trace("***** ***** *****\n", False, DEBUG)

    if response.status_code == 400:
        raise Exception("Bad Request - Request contains an unaccepted input")
    elif response.status_code == 401:
        raise Exception("Unauthorized or TOKEN expired")
    elif response.status_code == 403:
        raise Exception("Resource forbidden")
    elif response.status_code == 404:
        raise Exception("Not found")
    elif response.status_code == 500:
        raise Exception("Internal Server Error")

    result = json.loads(response.content)
    if DEBUG:
        mf.syslog_trace(f"Result data: ", False, DEBUG)
        for key in result:
            if key == "data":
                for data_key in result[key]:
                    mf.syslog_trace(
                        f"      {data_key} :: {result[key][data_key]}", False, DEBUG
                    )
            else:
                mf.syslog_trace(f"   {key} :: {result[key]}", False, DEBUG)


if __name__ == "__main__":
    main()
