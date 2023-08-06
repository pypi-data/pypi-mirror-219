"""
OTAC Module to implement functions to apply Archive Center settings

Class: OTAC
Methods:

__init__ : class initializer
config : returns config data set
execCommand: exec a command on Archive Center

"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2023, OpenText"
__credits__ = ["Kai-Philip Gatzweiler"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import requests
import os
import logging
import base64

from suds.client import Client

logger = logging.getLogger("pyxecm")

requestHeaders = {"Content-Type": "application/x-www-form-urlencoded"}


class OTAC:
    """Used to automate stettings in OpenText Archive Center."""

    _config = None
    _soap_token: str = ""

    def __init__(
        self,
        protocol: str,
        hostname: str,
        port: int,
        ds_username: str,
        ds_password: str,
        admin_username: str,
        admin_password: str,
    ):
        """Initialize the OTAC object

        Args:
            protocol (string): Either http or https.
            hostname (string): The hostname of the Archive Center  to communicate with.
            port (integer): The port number used to talk to the Archive Center .
            ds_username (string): The admin user name of Archive Center (dsadmin).
            ds_password (string): The admin password of Archive Center (dsadmin).
            admin_username (string): The admin user name of Archive Center (otadmin@otds.admin).
            admin_password (string): The admin password of Archive Center (otadmin@otds.admin).
        """

        otacConfig = {}

        if hostname:
            otacConfig["hostname"] = hostname
        else:
            otacConfig["hostname"] = ""

        if protocol:
            otacConfig["protocol"] = protocol
        else:
            otacConfig["protocol"] = "http"

        if port:
            otacConfig["port"] = port
        else:
            otacConfig["port"] = 80

        if ds_username:
            otacConfig["ds_username"] = ds_username
        else:
            otacConfig["ds_username"] = "dsadmin"

        if ds_password:
            otacConfig["ds_password"] = ds_password
        else:
            otacConfig["ds_password"] = ""

        if admin_username:
            otacConfig["admin_username"] = admin_username
        else:
            otacConfig["admin_username"] = "admin"

        if admin_password:
            otacConfig["admin_password"] = admin_password
        else:
            otacConfig["admin_password"] = ""

        otacBaseUrl = protocol + "://" + otacConfig["hostname"]
        if str(port) not in ["80", "443"]:
            otacBaseUrl += ":{}".format(port)
        otacExecUrl = otacBaseUrl + "/archive/admin/exec"
        otacConfig["execUrl"] = otacExecUrl
        otacConfig["baseUrl"] = otacBaseUrl

        self._config = otacConfig

    def config(self):
        return self._config

    def hostname(self):
        return self.config()["hostname"]

    def setHostname(self, hostname: str):
        self.config()["hostname"] = hostname

    def setCredentials(
        self,
        ds_username: str = "",
        ds_password: str = "",
        admin_username: str = "",
        admin_password: str = "",
    ):
        if ds_username:
            self.config()["ds_username"] = ds_username
        else:
            self.config()["ds_username"] = "dsadmin"

        if ds_password:
            self.config()["ds_password"] = ds_password
        else:
            self.config()["ds_password"] = ""

        if admin_username:
            self.config()["admin_username"] = admin_username
        else:
            self.config()["admin_username"] = "admin"

        if admin_password:
            self.config()["admin_password"] = admin_password
        else:
            self.config()["admin_password"] = ""

    def baseUrl(self):
        return self.config()["baseUrl"]

    def execUrl(self):
        return self.config()["execUrl"]

    def _soapLogin(self):
        """Authenticate via SOAP with admin User

        Args:
            None
        Returns:
            string: soap_token
        """

        url = self.baseUrl() + "/archive/services/Authentication?wsdl"
        client = Client(url)
        self._soap_token = client.service.Authenticate(
            username=self.config()["admin_username"],
            password=self.config()["admin_password"],
        )

        return self._soap_token

    # end method definition

    def execCommand(self, command: str):
        """Execute a command on Archive Center

        Args:
            command (string): command to execute
        Returns:
            _type_: _description_
        """

        payload = {
            "command": command,
            "user": self.config()["ds_username"],
            "passwd": self.config()["ds_password"],
        }

        request_url = self.execUrl()
        logger.info(
            "Execute command -> {} on Archive Center (user -> {}); calling -> {}".format(
                command, payload["user"], request_url
            )
        )
        response = requests.post(request_url, data=payload, headers=requestHeaders)
        if not response.ok:
            logger.error(
                "Failed to execute command -> {} on Archive Center; error -> {}".format(
                    command, response.text.replace("\n", " ")
                )
            )

        return response

    # end method definition

    def putCert(
        self,
        auth_id: str,
        logical_archive: str,
        cert_path: str,
        permissions: str = "rcud",
    ):
        """Put Certificate on Archive Center

        Args:
            auth_id (string): ID of Certification
            logical_archive (string): Archive ID
            certPath (string): local path to certificate (base64)
            permissions (string, optional): Permissions. Defaults to "rcud" (read-create-update-delete).
        Returns:
            response or None if the request fails
        """

        # Check if the photo file exists
        if not os.path.isfile(cert_path):
            logger.error("Certificate file -> {} not found!".format(cert_path))
            return None

        with open(cert_path, "r") as file:
            cert_content = file.read().strip()

        # Check that we have the pem certificate file - this is what OTAC expects. If the file content is
        # base64 encoded we will decode it
        if "BEGIN CERTIFICATE" in cert_content:
            logger.info("Certificate file -> {} is not base64 encoded".format(cert_path))
        elif "BEGIN CERTIFICATE" in base64.b64decode(
            cert_content, validate=True
        ).decode("utf-8"):
            logger.info("Certificate file -> {} is base64 encoded".format(cert_path))
            cert_content = base64.b64decode(cert_content, validate=True).decode("utf-8")
        else:
            logger.error(
                "Cerfificate file -> {} is not in the right format".format(cert_path)
            )
            return None

        request_url = (
            self.baseUrl()
            + "/archive?putCert&pVersion=0046&authId="
            + auth_id
            + "&contRep="
            + logical_archive
            + "&permissions="
            + permissions
        )
        logger.info(
            "Putting certificate -> {} on Archive -> {}; calling -> {}".format(
                cert_path, logical_archive, request_url
            )
        )
        response = requests.put(request_url, data=cert_content, headers=requestHeaders)

        if not response.ok:
            message = response.text.split(
                '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN'
            )[0]
            logger.error(
                "Failed to put certificate -> {} on Archive -> {}; error -> {}".format(
                    cert_path, logical_archive, message
                )
            )

        return response

    # end method definition

    def enableCert(self, auth_id: str, logical_archive: str, enable: bool = True):
        """Enable Certitificate

        Args:
            auth_id (string): Client ID
            logical_archive (string): Archive ID
            enable (boolean, optional): Enable or Disable certificate. Defaults to True.
        Returns:
            response or None if request fails.
        """

        if self._soap_token == "":
            self._soapLogin()

        if enable == True:
            enabled: int = 1
        else:
            enabled: int = 0

        url = self.baseUrl() + "/ot-admin/services/ArchiveAdministration?wsdl"
        client = Client(url)

        token_header = client.factory.create("ns0:OTAuthentication")
        token_header.AuthenticationToken = self._soap_token
        client.set_options(soapheaders=token_header)

        try:
            response = client.service.invokeCommand(
                command="SetCertificateFlags",
                parameters=[
                    {"key": "CERT_TYPE", "data": "@{}".format(logical_archive)},
                    {"key": "CERT_NAME", "data": auth_id},
                    {"key": "CERT_FLAGS", "data": enabled},
                ],
            )
            return response

        except Exception as e:
            logger.error(
                "Failed to execute SetCertificateFlags for Client -> {} on Archive -> {}; error -> {}".format(
                    auth_id, logical_archive, e
                )
            )
            return None


# end method definition
