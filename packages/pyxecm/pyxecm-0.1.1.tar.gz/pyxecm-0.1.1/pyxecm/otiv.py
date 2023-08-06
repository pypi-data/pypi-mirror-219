"""
OTIV Module to keep Intelligent Viewing specific data
such as connection parameters, license information ...

Class: OTIV
Methods:

__init__ : class initializer
config : returns config data set
"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2023, OpenText"
__credits__ = ["Kai-Philip Gatzweiler"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import os
import logging

logger = logging.getLogger("pyxecm")


class OTIV(object):
    """Used to manage stettings for OpenText Intelligent Viewing."""

    _config = None

    def __init__(
        self,
        resource_name: str,
        product_name: str,
        product_description: str,
        license_file: str,
        default_license: str = "FULLTIME_USERS_REGULAR",
    ):
        """Initialize the OTIV class for Intelligent Viewing

        Args:
            resource_name (string): OTDS resource name
            product_name (string): OTDS product name for licensing
            license_file (string): path to license file
            default_license (string, optional): Defaults to "FULLTIME_USERS_REGULAR".
        """

        # Initialize otcsConfig as an empty dictionary
        otcsConfig = {}

        otcsConfig["resource"] = resource_name
        otcsConfig["product"] = product_name
        otcsConfig["description"] = product_description
        otcsConfig["license_file"] = license_file
        otcsConfig["license"] = default_license

        self._config = otcsConfig

    # end method definition

    def config(self):
        return self._config

    # end method definition
