"""
Kubernetes Module to implement functions to read / write Kubernetes objects
such as Pods, Stateful Sets, Config Maps, ...

https://github.com/kubernetes-client/python 
https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md
https://github.com/kubernetes-client/python/tree/master/examples

Class: K8s
Methods:

__init__ : class initializer
getCoreV1Api: Get Kubernetes API object for Core APIs
getAppsV1Api: Get Kubernetes API object for Applications (e.g. Stateful Sets)
getNetworkingV1Api: Get Kubernetes API object for Networking (e.g. Ingress)
getNamespace: Get the Kubernetes namespace the K8s object is configured for

getPod: Get a Kubernetes Pod based on its name
listPods: Get a list of Kubernetes pods based on field and label selectors
execPodCommand: Execute a list of commands in a Kubernetes Pod
execPodCommendInteractive: Write commands to stdin and wait for response
deletePod: Delete a running pod (e.g. to make Kubernetes restart it)

getConfigMap: Get a Kubernetes Config Map based on its name
listConfigMaps: Get a list of Kubernetes Config Maps based on field and label selectors
findConfigMap: Find a Kubernetes Config Map based on its name
replaceConfigMap: Replace the data body of a Kubernetes Config Map

getStatefulSet: Gets a Kubernetes Stateful Set based on its name
getStatefulSetScale: Gets the number of replicas for a Kubernetes Stateful Set
patchStatefulSet: Updates the specification of a Kubernetes Stateful Set
scaleStatefulSet: Changes number of replicas for a Kubernetes Stateful Set

getService: Get a Kubernetes Service based on its name
listServices: Get a list of Kubernetes Services based on field and label selectors
patchService: Update the specification of a Kubernetes Service

getIngress: Get a Kubernetes Ingress based on its name
patchIngress: Update the specification of a Kubernetes Ingress
updateIngressBackendServices: Replace the backend service and port for an ingress host

"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2023, OpenText"
__credits__ = ["Kai-Philip Gatzweiler"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import os
import logging
import time
from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.exceptions import ApiException

# Configure Kubernetes API authentication to use pod serviceAccount
# config.load_incluster_config()

logger = logging.getLogger("pyxecm")

class K8s(object):
    """Used to automate stettings in Kubernetes."""

    _core_v1_api = None
    _apps_v1_api = None
    _networking_v1_api = None
    _namespace = None

    def __init__(self, inCluster: bool = True, namespace: str = ""):
        """Initialize the Kubernetes object."""

        # Configure Kubernetes API authentication to use pod serviceAccount
        if inCluster:
            config.load_incluster_config()
        else:
            config.load_kube_config()

        self._core_v1_api = client.CoreV1Api()
        self._apps_v1_api = client.AppsV1Api()
        self._networking_v1_api = client.NetworkingV1Api()
        if namespace:
            self._namespace = namespace
        else:
            # Read current namespace
            with open(
                "/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r"
            ) as f:
                self._namespace = f.read()

    def getCoreV1Api(self):
        return self._core_v1_api

    def getAppsV1Api(self):
        return self._apps_v1_api

    def getNetworkingV1Api(self):
        return self._networking_v1_api

    def getNamespace(self):
        return self._namespace

    def getPod(self, pod_name: str):
        """Get a pod in the configured namespace (the namespace is defined in the class constructor).
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#read_namespaced_pod
        Args:
            pod_name (string): name of the Kubernetes pod in the current namespace
        Returns:
            V1Pod (object) or None if the call fails.
            - api_version='v1',
            - kind='Pod',
            - metadata=V1ObjectMeta(...),
            - spec=V1PodSpec(...),
            - status=V1PodStatus(...)
        """

        try:
            response = self.getCoreV1Api().read_namespaced_pod(
                name=pod_name, namespace=self.getNamespace()
            )
        except ApiException as e:
            logger.error(
                "Failed to get Pod -> {}; error -> {}".format(pod_name, str(e))
            )
            return None

        return response

    # end method definition

    def listPods(self, field_selector: str = "", label_selector: str = ""):
        """List all Kubernetes pods in a given namespace. The list can be further restricted
            by specifying a field or label selector.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#list_namespaced_pod
        Args:
            field_selector (string): filter result based on fields
            label_selector (string): filter result based on labels
        Returns:
            V1PodList (object) or None if the call fails
            Properties can be accessed with the "." notation (this is an object not a dict!):
            - api_version: The Kubernetes API version.
            - items: A list of V1Pod objects, each representing a pod. You can access the fields of a
                    V1Pod object using dot notation, for example, pod.metadata.name to access the name of the pod
            - kind: The Kubernetes object kind, which is always "PodList".
            - metadata: Additional metadata about the pod list, such as the resource version.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1PodList.md
        """

        try:
            response = self.getCoreV1Api().list_namespaced_pod(
                field_selector=field_selector,
                label_selector=label_selector,
                namespace=self.getNamespace(),
            )
        except ApiException as e:
            logger.error(
                "Failed to list Pods with field_selector -> {} and label_selector -> {}; error -> {}".format(
                    field_selector, label_selector, str(e)
                )
            )
            return None

        return response

    # end method definition

    def waitPodCondition(self, pod_name: str, condition_name: str):
        """Wait for the pod to reach a defined condition (e.g. "Ready").
        Args:
            pod_name (string): name of the Kubernetes pod in the current namespace
            condition_name (string): name of the condition, e.g. "Ready"
        Returns:
            True once the pod reaches the condition - otherwise wait forever
        """

        ready = False
        while not ready:
            try:
                pod_status = self.getCoreV1Api().read_namespaced_pod_status(
                    pod_name, self.getNamespace()
                )

                # Check if the pod has reached the defined condition:
                for cond in pod_status.status.conditions:
                    if cond.type == condition_name and cond.status == "True":
                        logger.info(
                            "Pod -> {} is in state -> {}!".format(
                                pod_name, condition_name
                            )
                        )
                        ready = True
                        break
                else:
                    logger.info(
                        "Pod -> {} is not yet in state -> {}. Waiting...".format(
                            pod_name, condition_name
                        )
                    )
                    time.sleep(30)
                    continue

            except ApiException as e:
                logger.error(
                    "Failed to wait for pod -> {}; error -> {}".format(pod_name, str(e))
                )

    # end method definition

    def execPodCommand(self, pod_name: str, command: list):
        """Execute a command inside a Kubernetes Pod (similar to kubectl exec on command line).
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#connect_get_namespaced_pod_exec
        Args:
            pod_name (string): name of the Kubernetes pod in the current namespace
            command (list): list of command and its parameters, e.g. ["/bin/bash", "-c", "pwd"]
                            The "-c" is required to make the shell executing the command.
        Returns:
            Response of the command or None if the call fails
        """

        pod = self.getPod(pod_name)
        if not pod:
            logger.error("Pod -> {} does not exist".format(pod_name))

        logger.info("Execute command -> {} in pod -> {}".format(command, pod_name))

        try:
            response = stream(
                self.getCoreV1Api().connect_get_namespaced_pod_exec,
                pod_name,
                self.getNamespace(),
                command=command,
                stderr=True,
                stdin=False,
                stdout=True,
                tty=False,
            )
        except ApiException as e:
            logger.error(
                "Failed to execute command -> {} in pod -> {}; error -> {}".format(
                    command, pod_name, str(e)
                )
            )
            return None

        return response

    # end method definition

    # Some commands like the OTAC spawner need to run interactive - otherwise the command "hangs"
    def execPodCommandInteractive(
        self,
        pod_name: str,
        commands: list,
        timeout: int = 30,
        write_stderr_to_error_log: bool = True,
    ):
        """Execute a command inside a Kubernetes pod (similar to kubectl exec on command line).
            Other than execPodCommand() method above this is an interactive execution using
            stdin and reading the output from stdout and stderr. This is required for longer
            running commands. It is currently used for restarting the spawner of Archive Center.
            The output of the command is pushed into the logging.
        Args:
            pod_name (string): name of the Kubernetes pod in the current namespace
            commands (list): list of command and its parameters, e.g. ["/bin/bash", "/etc/init.d/spawner restart"]
                             Here we should NOT have a "-c" parameter!
            timeout (integer): timeout duration that is waited for any response.
                               Each time a resonse is found in stdout or stderr we wait another timeout duration
                               to make sure we get the full output of the command.
            write_stderr_to_error_log (boolean): flag to control if output in stderr should be written to info or error log stream.
                                                 Default is write to error log (True)
        Returns:
            Response of the command (string) or None if the call fails
        """

        pod = self.getPod(pod_name)
        if not pod:
            logger.error("Pod -> {} does not exist".format(pod_name))

        if not commands:
            return None

        # Get first command - this should be the shell:
        command = commands.pop(0)

        try:
            response = stream(
                self.getCoreV1Api().connect_get_namespaced_pod_exec,
                pod_name,
                self.getNamespace(),
                command=command,
                stderr=True,
                stdin=True,  # This is important!
                stdout=True,
                tty=False,
                _preload_content=False,  # This is important!
            )
        except ApiException as e:
            logger.error(
                "Failed to execute command -> {} in pod -> {}; error -> {}".format(
                    command, pod_name, str(e)
                )
            )
            return None

        while response.is_open():
            got_response = False
            response.update(timeout=timeout)
            if response.peek_stdout():
                logger.info(response.read_stdout().replace("\n", " "))
                got_response = True
            if response.peek_stderr():
                if write_stderr_to_error_log:
                    logger.error(response.read_stderr().replace("\n", " "))
                else:
                    logger.info(response.read_stderr().replace("\n", " "))
                got_response = True
            if commands:
                command = commands.pop(0)
                logger.info(
                    "Execute command -> {} in pod -> {}".format(command, pod_name)
                )
                response.write_stdin(command + "\n")
            else:
                # We continue as long as we get some response during timeout period
                if not got_response:
                    break

        response.close()

        return response

    # end method definition

    def deletePod(self, pod_name: str):
        """Delete a pod in the configured namespace (the namespace is defined in the class constructor).
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#delete_namespaced_pod
        Args:
            pod_name (string): name of the Kubernetes pod in the current namespace
        Return:
            V1Status (object) or None if the call fails.
            - api_version: The Kubernetes API version.
            - kind: The Kubernetes object kind, which is always "Status".
            - metadata: Additional metadata about the status object, such as the resource version.
            - status: The status of the operation, which is either "Success" or an error status.
            - message: A human-readable message explaining the status.
            - reason: A short string that describes the reason for the status.
            - code: An HTTP status code that corresponds to the status.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Status.md
        """

        pod = self.getPod(pod_name)
        if not pod:
            logger.error("Pod -> {} does not exist".format(pod_name))

        try:
            response = self.getCoreV1Api().delete_namespaced_pod(
                pod_name, namespace=self.getNamespace()
            )
        except ApiException as e:
            logger.error(
                "Failed to delete Pod -> {}; error -> {}".format(pod_name, str(e))
            )
            return None

        return response

    # end method definition

    def getConfigMap(self, config_map_name: str):
        """Get a config map in the configured namespace (the namespace is defined in the class constructor).
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#read_namespaced_config_map
        Args:
            config_map_name (string): name of the Kubernetes config map in the current namespace
        Returns:
            V1ConfigMap (object) that includes these fields:
            - api_version: The Kubernetes API version.
            - metadata: A V1ObjectMeta object representing metadata about the V1ConfigMap object,
                        such as its name, labels, and annotations.
            - data: A dictionary containing the non-binary data stored in the ConfigMap,
                    where the keys represent the keys of the data items and the values represent
                    the values of the data items.
            - binary_data: A dictionary containing the binary data stored in the ConfigMap,
                           where the keys represent the keys of the binary data items and the values
                           represent the values of the binary data items. Binary data is encoded as base64
                           strings in the dictionary values.
        """

        try:
            response = self.getCoreV1Api().read_namespaced_config_map(
                name=config_map_name, namespace=self.getNamespace()
            )
        except ApiException as e:
            logger.error("Failed to get Config Map -> {}; error -> {}".format(str(e)))
            return None

        return response

    # end method definition

    def listConfigMaps(self, field_selector: str = "", label_selector: str = ""):
        """List all Kubernetes Config Maps in the current namespace.
            The list can be filtered by providing field selectors and label selectors.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#list_namespaced_config_map
        Args:
            field_selector (string): filter result based on fields
            label_selector (string): filter result based on labels
        Returns:
            V1ConfigMapList (object) or None if the call fails
            Properties can be accessed with the "." notation (this is an object not a dict!):
            - api_version: The Kubernetes API version.
            - items: A list of V1ConfigMap objects, each representing a config map. You can access the fields of a
                     V1Pod object using dot notation, for example, cm.metadata.name to access the name of the config map
            - kind: The Kubernetes object kind, which is always "ConfigMapList".
            - metadata: Additional metadata about the config map list, such as the resource version.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1ConfigMapList.md
        """

        try:
            response = self.getCoreV1Api().list_namespaced_config_map(
                field_selector=field_selector,
                label_selector=label_selector,
                namespace=self.getNamespace(),
            )
        except ApiException as e:
            logger.error(
                "Failed to list Config Maps with field_selector -> {} and label_selector -> {}; error -> {}".format(
                    field_selector, label_selector, str(e)
                )
            )
            return None

        return response

    # end method definition

    def findConfigMap(self, config_map_name: str):
        """Find a Kubernetes Config Map based on its name.
           This is just a wrapper method for listConfigMaps()
           that uses the name as a field selector.

        Args:
            config_map_name (string): name of the Config Map
        Returns:
            object: V1ConfigMapList (object) or None if the call fails
        """

        try:
            response = self.listConfigMaps(
                field_selector="metadata.name={}".format(config_map_name)
            )
        except ApiException as e:
            logger.error(
                "Failed to find Config Map -> {}; error -> {}".format(
                    config_map_name, str(e)
                )
            )
            return None

        return response

    # end method definition

    def replaceConfigMap(self, config_map_name: str, config_map_data: dict):
        """Replace a Config Map with a new specification.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#replace_namespaced_config_map

        Args:
            config_map_name (string): name of the Kubernetes Config Map
            config_map_data (dictionary): new specification of the Config Map
        Returns:
            V1ConfigMap (object) or None if the call fails.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1ConfigMap.md
        """

        try:
            response = self.getCoreV1Api().replace_namespaced_config_map(
                name=config_map_name,
                namespace=self.getNamespace(),
                body=client.V1ConfigMap(
                    metadata=client.V1ObjectMeta(
                        name=config_map_name,
                    ),
                    data=config_map_data,
                ),
            )
        except ApiException as e:
            logger.error(
                "Failed to replace Config Map -> {}; error -> {}".format(
                    config_map_name, str(e)
                )
            )
            return None

        return response

    # end method definition

    def getStatefulSet(self, sts_name: str):
        """Get a Kubernetes Stateful Set based on its name.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/AppsV1Api.md#read_namespaced_stateful_set

        Args:
            sts_name (string): name of the Kubernetes stateful set
        Returns:
            V1StatefulSet (object) or None if the call fails.
            See : https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1StatefulSet.md
        """

        try:
            response = self.getAppsV1Api().read_namespaced_stateful_set(
                name=sts_name, namespace=self.getNamespace()
            )
        except ApiException as e:
            logger.error(
                "Failed to get Stateful Set -> {}; error -> {}".format(sts_name, str(e))
            )
            return None

        return response

    # end method definition

    def getStatefulSetScale(self, sts_name: str):
        """Get the number of replicas for a Kubernetes Stateful Set.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/AppsV1Api.md#read_namespaced_stateful_set_scale

        Args:
            sts_name (string): name of the Kubernetes Stateful Set
        Returns:
            V1Scale (object) or None if the call fails.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Scale.md
        """

        try:
            response = self.getAppsV1Api().read_namespaced_stateful_set_scale(
                name=sts_name, namespace=self.getNamespace()
            )
        except ApiException as e:
            logger.error(
                "Failed to get scaling (replicas) of Stateful Set -> {}; error -> {}".format(
                    sts_name, str(e)
                )
            )
            return None

        return response

    # end method definition

    def patchStatefulSet(self, sts_name: str, sts_body: dict):
        """Patch a Stateful set with new values.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/AppsV1Api.md#patch_namespaced_stateful_set

        Args:
            sts_name (string): name of the Kubernetes stateful set in the current namespace
            sts_body (string): patch string
        Returns:
            V1StatefulSet (object) or None if the call fails.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1StatefulSet.md
        """

        try:
            response = self.getAppsV1Api().patch_namespaced_stateful_set(
                name=sts_name, namespace=self.getNamespace(), body=sts_body
            )
        except ApiException as e:
            logger.error(
                "Failed to patch Stateful Set -> {} with -> {}; error -> {}".format(
                    sts_name, sts_body, str(e)
                )
            )
            return None

        return response

    # end method definition

    def scaleStatefulSet(self, sts_name: str, scale: int):
        """Scale a stateful set to a specific number of replicas. It uses the class method patchStatefulSet() above.

        Args:
            sts_name (string): name of the Kubernetes stateful set in the current namespace
        Returns:
            V1StatefulSet (object) or None if the call fails.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1StatefulSet.md
        """

        try:
            response = self.patchStatefulSet(
                sts_name, sts_body={"spec": {"replicas": scale}}
            )
        except ApiException as e:
            logger.error(
                "Failed to scale Stateful Set -> {} to -> {} replicas; error -> {}".format(
                    sts_name, scale, str(e)
                )
            )
            return None

        return response

    # end method definition

    def getService(self, service_name: str):
        """Get a Kubernetes Service with a defined name in the current namespace

        Args:
            service_name (string): name of the Kubernetes Service in the current namespace
        Returns:
            V1Service (object) or None if the call fails
            This is NOT a dict but an object - the you have to use the "." syntax to access to returned elements.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Service.md
        """

        try:
            response = self.getCoreV1Api().read_namespaced_service(
                name=service_name, namespace=self.getNamespace()
            )
        except ApiException as e:
            logger.error(
                "Failed to get Service -> {}; error -> {}".format(service_name, str(e))
            )
            return None

        return response

    # end method definition

    def listServices(self, field_selector: str = "", label_selector: str = ""):
        """List all Kubernetes Service in the current namespace.
            The list can be filtered by providing field selectors and label selectors.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#list_namespaced_service

        Args:
            field_selector (string): filter result based on fields
            label_selector (string): filter result based on labels
        Returns:
            V1ServiceList (object) or None if the call fails
            Properties can be accessed with the "." notation (this is an object not a dict!):
            - api_version: The Kubernetes API version.
            - items: A list of V1Service objects, each representing a service. You can access the fields of a
                     V1Service object using dot notation, for example, service.metadata.name to access the name of the service
            - kind: The Kubernetes object kind, which is always "ServiceList".
            - metadata: Additional metadata about the pod list, such as the resource version.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1ServiceList.md
        """

        try:
            response = self.getCoreV1Api().list_namespaced_service(
                field_selector=field_selector,
                label_selector=label_selector,
                namespace=self.getNamespace(),
            )
        except ApiException as e:
            logger.error(
                "Failed to list Services with field_selector -> {} and label_selector -> {}; error -> {}".format(
                    field_selector, label_selector, str(e)
                )
            )
            return None

        return response

    # end method definition

    def patchService(self, service_name: str, service_body: dict):
        """Patches a Kubernetes Service with an updated spec

        Args:
            service_name (string): name of the Kubernetes Ingress in the current namespace
            service_body (dict): new / updated Service body spec (will be merged with existing values)
        Returns:
            V1Service object or None if the call fails
            This is NOT a dict but an object - you have to use the "." syntax to access to returned elements
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Service.md
        """

        try:
            response = self.getCoreV1Api().patch_namespaced_service(
                name=service_name, namespace=self.getNamespace(), body=service_body
            )
        except ApiException as e:
            logger.error(
                "Failed to patch Service -> {} with -> {}; error -> {}".format(
                    service_name, service_body, str(e)
                )
            )
            return None

        return response

    # end method definition

    def getIngress(self, ingress_name: str):
        """Get a Kubernetes Ingress with a defined name in the current namespace

        Args:
            ingress_name (string): name of the Kubernetes Ingress in the current namespace
        Returns:
            V1Ingress object or None if the call fails
            This is NOT a dict but an object - the you have to use the "." syntax to access to returned elements.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Ingress.md
        """

        try:
            response = self.getNetworkingV1Api().read_namespaced_ingress(
                name=ingress_name, namespace=self.getNamespace()
            )
        except ApiException as e:
            logger.error(
                "Failed to get Ingress -> {}; error -> {}".format(ingress_name, str(e))
            )
            return None

        return response

    # end method definition

    def patchIngress(self, ingress_name: str, ingress_body: dict):
        """Patch a Kubernetes Ingress with a updated spec.
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/NetworkingV1Api.md#patch_namespaced_ingress

        Args:
            ingress_name (string): name of the Kubernetes Ingress in the current namespace
            ingress_body (dict): new / updated ingress body spec (will be merged with existing values)
        Returns:
            V1Ingress object or None if the call fails
            This is NOT a dict but an object - you have to use the "." syntax to access to returned elements
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Ingress.md
        """

        try:
            response = self.getNetworkingV1Api().patch_namespaced_ingress(
                name=ingress_name,
                namespace=self.getNamespace(),
                body=ingress_body,
            )
        except ApiException as e:
            logger.error(
                "Failed to patch Ingress -> {} with -> {}; error -> {}".format(
                    ingress_name, ingress_body, str(e)
                )
            )
            return None

        return response

    # end method definition

    def updateIngressBackendServices(
        self, ingress_name: str, hostname: str, service_name: str, service_port: int
    ):
        """Updates a backend service and port of an Kubernetes Ingress

        "spec": {
            "rules": [
                {
                    "host": host,
                    "http": {
                        "paths": [
                            {
                                "path": "/",
                                "pathType": "Prefix",
                                "backend": {
                                    "service": {
                                        "name": <service_name>,
                                        "port": {
                                            "name": None,
                                            "number": <service_port>,
                                        },
                                    },
                                },
                            }
                        ]
                    },
                }
            ]
        }

        Args:
            ingress_name (string): name of the Kubernetes Ingress in the current namespace
            hostname (string): hostname that should get an updated backend service / port
            service_name (string): new backend service name
            service_port (integer): new backend service port
        Returns:
            V1Ingress Object or None if the call fails
            This is NOT a dict but an object - you have to use the "." syntax to access to returned elements
            See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Ingress.md
        """

        ingress = self.getIngress(ingress_name)
        if not ingress:
            return None

        host = ""
        rules = ingress.spec.rules
        rule_index = 0
        for rule in rules:
            if hostname in rule.host:
                host = rule.host
                path = rule.http.paths[0]
                backend = path.backend
                service = backend.service

                logger.info(
                    "Replace backend service -> {} ({}) with new backend service -> {} ({})".format(
                        service.name, service.port.number, service_name, service_port
                    )
                )

                service.name = service_name
                service.port.number = service_port
                break
            else:
                rule_index += 1

        if not host:
            logger.error("Cannot find host -> {}.")
            return None

        body = [
            {
                "op": "replace",
                "path": "/spec/rules/{}/http/paths/0/backend/service/name".format(
                    rule_index
                ),
                "value": service_name,
            },
            {
                "op": "replace",
                "path": "/spec/rules/{}/http/paths/0/backend/service/port/number".format(
                    rule_index
                ),
                "value": service_port,
            },
        ]

        return self.patchIngress(ingress_name, body)

    # end method definition
