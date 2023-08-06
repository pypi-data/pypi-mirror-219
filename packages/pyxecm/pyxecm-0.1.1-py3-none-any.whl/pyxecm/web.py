"""
Module to implement functions to execute Web Requests

Class: HTTP
Methods:

__init__ : class initializer
checkHostReachable: checks if a server / host is reachable
httpRequest: make a HTTP request to a defined URL / endpoint (e.g. a Web Hook)

"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2023, OpenText"
__credits__ = ["Kai-Philip Gatzweiler"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import requests
import os
import logging
import socket

logger = logging.getLogger("pyxecm")

requestHeaders = {"Content-Type": "application/x-www-form-urlencoded"}


class HTTP(object):
    """Used to automate stettings in OpenText Archive Center."""

    _config = None

    def __init__(self):
        """Initialize the HTTP object

        Args:
        """

    def checkHostReachable(self, hostname: str, port: int = 80) -> bool:
        """Check if a server / web address is reachable

        Args:
            hostname (string): endpoint hostname
            port (integer): endpoint port
        Results:
            boolean: True is reachable, False otherwise
        """

        logger.info(
            "Test if host -> {} is reachable on port -> {} ...".format(hostname, port)
        )
        try:
            socket.getaddrinfo(hostname, port)
        except socket.gaierror as e:
            logger.warning(
                "Address-related error - cannot reach host -> {}; error -> {}".format(
                    hostname, e
                )
            )
            return False
        except socket.error as e:
            logger.warning(
                "Connection error - cannot reach host -> {}; error -> {}".format(
                    hostname, e
                )
            )
            return False
        else:
            logger.info("Host is reachable at -> {}:{}".format(hostname, port))
            return True

    # end method definition

    def httpRequest(
        self, url: str, method: str = "POST", payload: dict = {}, headers: dict = {}
    ):
        if not headers:
            headers = requestHeaders

        logger.info(
            "Make HTTP Request to URL -> {} using -> {} method with payload -> {}".format(
                url, method, payload
            )
        )

        httpRequestResponse = requests.request(
            method=method, url=url, data=payload, headers=headers
        )

        if not httpRequestResponse.ok:
            logger.error(
                "HTTP request -> {} to url -> {} failed; error -> {}".format(
                    method, httpRequestResponse.text
                )
            )

        return httpRequestResponse

    # end method definition
