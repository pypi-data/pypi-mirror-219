"""
OTPD Module to implement functions to read / write PowerDocs objects

Class: OTPD
Methods:

__init__ : class initializer
config : returns config data set
importDatabase: imports the PowerDocs database from a zip file
applySetting: apply a setting to a PowerDocs tenant

"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2023, OpenText"
__credits__ = ["Kai-Philip Gatzweiler"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import json
import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import logging

logger = logging.getLogger("pyxecm")

requestHeaders = {
    "accept": "application/json;charset=utf-8",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
}


class OTPD:
    """Used to automate stettings in OpenText Extended ECM PowerDocs."""

    _config = None
    _jsessionid = None

    def __init__(
        self, protocol: str, hostname: str, port: int, username: str, password: str
    ):
        """Initialize the OTPD object

        Args:
            protocol (string): Either http or https.
            hostname (string): The hostname of the PowerDocs Server Manager to communicate with.
            port (integer): The port number used to talk to the PowerDocs Server Manager.
            username (string): The admin user name of PowerDocs Server Manager.
            password (string): The admin password of PowerDocs Server Manager.
        """

        otpdConfig = {}

        if hostname:
            otpdConfig["hostname"] = hostname
        else:
            otpdConfig["hostname"] = ""

        if protocol:
            otpdConfig["protocol"] = protocol
        else:
            otpdConfig["protocol"] = "http"

        if port:
            otpdConfig["port"] = port
        else:
            otpdConfig["port"] = 80

        if username:
            otpdConfig["username"] = username
        else:
            otpdConfig["username"] = "admin"

        if password:
            otpdConfig["password"] = password
        else:
            otpdConfig["password"] = ""

        otpdBaseUrl = protocol + "://" + otpdConfig["hostname"]
        if str(port) not in ["80", "443"]:
            otpdBaseUrl += ":{}".format(port)
        otpdBaseUrl += "/ServerManager"
        otpdConfig["baseUrl"] = otpdBaseUrl

        otpdRestUrl = otpdBaseUrl + "/api"
        otpdConfig["restUrl"] = otpdRestUrl

        otpdConfig["settingsUrl"] = otpdRestUrl + "/v1/settings"

        otpdConfig["importDatabaseUrl"] = otpdBaseUrl + "/servlet/import"

        self._config = otpdConfig

    def config(self):
        return self._config

    def credentials(self):
        return {
            "username": self.config()["username"],
            "password": self.config()["password"],
        }

    def hostname(self):
        return self.config()["hostname"]

    def setHostname(self, hostname: str):
        self.config()["hostname"] = hostname

    def setCredentials(self, username: str = "", password: str = ""):
        if username:
            self.config()["username"] = username
        else:
            self.config()["username"] = "admin"

        if password:
            self.config()["password"] = password
        else:
            self.config()["password"] = ""

    def baseUrl(self):
        return self.config()["baseUrl"]

    def restUrl(self):
        return self.config()["restUrl"]

    def parseRequestResponse(
        self,
        response_object: object,
        additional_error_message: str = "",
        show_error: bool = True,
    ) -> dict:
        """Converts the request response to a Python dict in a safe way
           that also handles exceptions.

        Args:
            response_object (object): this is reponse object delivered by the request call
            additional_error_message (string): print a custom error message
            show_error (boolean): if True log an error, if False log a warning

        Return: a python dict object or null in case of an error
        """

        if not response_object:
            return None

        try:
            dict_object = json.loads(response_object.text)
        except json.JSONDecodeError as e:
            if additional_error_message:
                message = "Cannot decode response as JSon. {}; error -> {}".format(
                    additional_error_message, e
                )
            else:
                message = "Cannot decode response as JSon; error -> {}".format(e)
            if show_error:
                logger.error(message)
            else:
                logger.warning(message)
            return None
        else:
            return dict_object

    # end method definition

    def importDatabase(self, filename: str):
        """Import PowerDocs database backup from a zip file"""

        file = filename.split("/")[-1]
        file_tup = (file, open(filename, "rb"), "application/zip")

        # fields attribute is set according to the other party's interface description
        m = MultipartEncoder(fields={"name": file, "zipfile": file_tup})

        requestUrl = self.config()["otpdImportDatabaseUrl"]

        logger.info(
            "Importing Database backup -> {}, in to ServerManager on-> {}".format(
                filename, requestUrl
            )
        )
        resourceResponse = requests.post(
            requestUrl, data=m, headers={"content-type": m.content_type}, timeout=60
        )

        if resourceResponse.ok:
            return resourceResponse
        else:
            logger.error(
                "Failed to Import Database backup -> {} in to -> {}; error => {}".format(
                    filename, requestUrl, resourceResponse.text
                )
            )
            return None

    # end method definition

    # This method is currently not used and not working...
    def authenticate(self, revalidate: bool = False):
        # Already authenticated and session still valid?
        if self._jsessionid and not revalidate:
            return self._jsessionid

        auth_url = (
            self.baseUrl()
            + "/j_security_check?j_username="
            + self.config()["username"]
            + "&j_password="
            + self.config()["password"]
        )
        payLoad = {}
        payLoad["settingname"] = "LocalOtdsUrl"
        payLoad["settingvalue"] = "http://otds/otdsws"

        requestUrl = self.config()["settingsUrl"]

        ##Fetching session id will be three step process
        # Step1: intiate a dummy request to tomcat
        # Step2: fetch session id from the response, and hit j_security_check with proper authentication
        # Step3: get session id from the response, add to self. It can be used for other transactions
        session = requests.Session()
        response = session.put(requestUrl, json=payLoad)
        logger.info("Initiating dummy rest call to Tomcat to get initial session id")
        logger.info(response.text)
        if response.ok:
            logger.info("Url to authenticate Tomcat for Session id -> " + auth_url)
            sessionResponse = session.post(auth_url)
            if sessionResponse.ok:
                logger.info("Response for -> {}, {} ".format(auth_url, sessionResponse))
                session_dict = session.cookies.get_dict()
                logger.info(
                    "Session id to perform Rest api calls to Tomcat -> "
                    + session_dict["JSESSIONID"]
                )
                self._jsessionid = session_dict["JSESSIONID"]
                requestHeaders["Cookie"] = "JSESSIONID=" + self._jsessionid
            else:
                logger.info(
                    "Fetching session id from -> {} failed with j_security_check. Response -> {}".format(
                        auth_url, sessionResponse.text
                    )
                )
        else:
            logger.info(
                "Fetching session id from -> {} failed. Response => {}".format(
                    requestUrl, response.text
                )
            )

    # end method definition

    def applySetting(
        self, setting_name: str, setting_value: str, tenant_name: str = ""
    ) -> dict:
        """Appy a setting to the PowerDocs Server Manager

        Args:
            setting_name (string): name of the setting
            setting_value (string): new value of the setting
            tenant_name (string): name of the PowerDocs tenant - this is optional as some settings are not tenant-specific!
        Return:
            dictionary: Request response or None if the REST call fails.
        """

        settingsPutBody = {
            "settingname": setting_name,
            "settingvalue": setting_value,
        }

        if tenant_name:
            settingsPutBody["tenantName"] = tenant_name

        requestUrl = self.config()["settingsUrl"]

        logger.info(
            "Update setting -> {} with value -> {}; calling -> {}".format(
                setting_name, setting_value, requestUrl
            )
        )

        retries = 0
        while True:
            settingResponse = requests.put(
                requestUrl,
                json=settingsPutBody,
                headers=requestHeaders,
                auth=HTTPBasicAuth(
                    self.config()["username"], self.config()["password"]
                ),
                verify=False,  # for localhost deployments this will fail otherwise
            )
            if settingResponse.ok:
                return self.parseRequestResponse(settingResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif settingResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to update setting -> {}; error -> {}".format(
                        setting_name, settingResponse.text
                    )
                )
                return None

    # end method definition
