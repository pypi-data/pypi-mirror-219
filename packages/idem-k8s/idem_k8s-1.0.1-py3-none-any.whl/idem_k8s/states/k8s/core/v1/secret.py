"""State module for managing Kubernetes Secret."""
import base64
import copy
from typing import Any
from typing import Dict

from dict_tools import differ

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    metadata: Dict,
    type: str,
    data: Dict = None,
    immutable: bool = False,
    string_data: Dict = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Create a Secret

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        data(dict, Optional): Data contains the secret data. Each key must consist of alphanumeric characters, '-', '_' or
            '.'. The serialized form of the secret data is a base64 encoded string, representing the
            arbitrary (possibly non-string) data value here. Described in
            https://tools.ietf.org/html/rfc4648#section-4.
        immutable(bool, Optional): Immutable, if set to true, ensures that data stored in the Secret cannot be updated (only object
            metadata can be modified). If not set to true, the field can be modified at any time. Defaulted
            to nil.
        metadata(dict): Standard object's metadata.
            More info: `Kubernetes reference <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.>`_
        string_data(dict, Optional): stringData allows specifying non-binary secret data in string form. It is provided as a write-
            only input field for convenience. All keys and values are merged into the data field on write,
            overwriting any existing values. The stringData field is never output when reading from the API.
        type(str): Used to facilitate programmatic handling of secret data.
            More info: `Secret Types <https://kubernetes.io/docs/concepts/configuration/secret/#secret-types.>`_

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              k8s.core.v1.secret.present:
                - name: idem-test-secret
                - data:
                    username: YWRtaW4=
                    password: MWYyZDFlMmU2N2Rm
                - metadata:
                   name: idem-test-secret
                   namespace: default
                   annotations:
                    kubernetes.io/service-account.name: test-account
                - type: Opaque

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    # Get namespace
    namespace = metadata.get("namespace") if "namespace" in metadata else "default"
    metadata["namespace"] = namespace

    # Check for existing secret by name in namespace
    before = None
    if resource_id:
        secret = await hub.exec.k8s.client.CoreV1Api.read_namespaced_secret(
            ctx, name=resource_id, namespace=namespace
        )
        if not secret["result"]:
            result["comment"] = secret["comment"]
            result["result"] = secret["result"]
            return result
        before = secret["ret"]

    # Update current state
    current_state = hub.tool.k8s.core.v1.secret_utils.convert_raw_secret_to_present(
        secret=before
    )
    result["old_state"] = current_state

    if string_data:
        data = data if data else {}
        for key, value in string_data.items():
            data[key] = base64.b64encode(value.encode()).decode()

    # Handle no change behaviour
    desired_state = {
        "resource_id": resource_id,
        "metadata": metadata,
        "type": type,
        "data": data,
        "immutable": immutable,
    }

    desired_state = hub.tool.k8s.state_utils.merge_arguments(
        desire_state=desired_state, current_state=result["old_state"]
    )

    is_change_detected = before is None or bool(
        differ.deep_diff(old=result["old_state"] or {}, new=desired_state)
    )
    if not is_change_detected:
        result["comment"] = hub.tool.k8s.comment_utils.already_exists_comment(
            resource_type="k8s.core.v1.secret", name=name
        )
        result["new_state"] = copy.deepcopy(result["old_state"])
        return result

    # Handle test behaviour
    if ctx.get("test", False):
        result["new_state"] = hub.tool.k8s.test_state_utils.generate_test_state(
            enforced_state=current_state,
            desired_state=desired_state,
        )
        result["comment"] = (
            hub.tool.k8s.comment_utils.would_update_comment(
                resource_type="k8s.core.v1.secret", name=name
            )
            if before
            else hub.tool.k8s.comment_utils.would_create_comment(
                resource_type="k8s.core.v1.secret", name=name
            )
        )
        return result

    # Handle actual resource create or update
    body = hub.tool.k8s.marshaller.unmarshal(
        desired_state=desired_state, k8s_model_name="V1Secret"
    )
    if before:
        ret = await hub.exec.k8s.client.CoreV1Api.replace_namespaced_secret(
            ctx, name=resource_id, namespace=namespace, body=body
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.update_comment(
            resource_type="k8s.core.v1.secret", name=name
        )
    else:
        ret = await hub.exec.k8s.client.CoreV1Api.create_namespaced_secret(
            ctx, namespace=namespace, body=body
        )
        resource_id = body.metadata.name
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.create_comment(
            resource_type="k8s.core.v1.secret", name=name
        )

    # Fetch the updated resource and update new_state
    secret = await hub.exec.k8s.client.CoreV1Api.read_namespaced_secret(
        ctx, name=resource_id, namespace=namespace
    )
    if not secret["result"]:
        result["comment"] = result["comment"] + secret["comment"]
        result["result"] = secret["result"]
        return result
    after = secret["ret"]
    result[
        "new_state"
    ] = hub.tool.k8s.core.v1.secret_utils.convert_raw_secret_to_present(secret=after)
    return result


async def absent(
    hub,
    ctx,
    name: str,
    metadata: Dict = dict(namespace="default"),
    resource_id: str = None,
) -> Dict[str, Any]:
    """Delete a Secret

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        metadata(dict, Optional): Standard object's metadata.
            Defaults to metadata with 'default' namespace, in case of value not provided in absent state.
            More info: `Kubernetes reference <https://git.k8s.io/community/contributors/devel/sig-
            architecture/api-conventions.md#metadata.>`_

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              k8s.core.v1.secret.absent:
                - name: value
                - metadata: value

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    namespace = metadata.get("namespace") if "namespace" in metadata else "default"

    before = None
    if resource_id:
        secret = await hub.exec.k8s.client.CoreV1Api.read_namespaced_secret(
            ctx, name=resource_id, namespace=namespace
        )
        if secret and secret["result"]:
            before = secret["ret"]
            result[
                "old_state"
            ] = hub.tool.k8s.core.v1.secret_utils.convert_raw_secret_to_present(
                secret=before
            )

    if not before:
        result["comment"] = hub.tool.k8s.comment_utils.already_absent_comment(
            resource_type="k8s.core.v1.secret", name=name
        )
    elif ctx.get("test", False):
        result["comment"] = hub.tool.k8s.comment_utils.would_delete_comment(
            resource_type="k8s.core.v1.secret", name=name
        )
    else:
        ret = await hub.exec.k8s.client.CoreV1Api.delete_namespaced_secret(
            ctx, name=resource_id, namespace=namespace
        )
        if not ret["result"]:
            result["result"] = ret["result"]
            result["comment"] = ret["comment"]
            return result

        result["comment"] = hub.tool.k8s.comment_utils.delete_comment(
            resource_type="k8s.core.v1.secret", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    List or watch objects of kind Secret.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe k8s.core.v1.secret

    """
    ret = await hub.exec.k8s.client.CoreV1Api.list_secret_for_all_namespaces(
        ctx,
    )
    if not ret["result"]:
        hub.log.debug(f"Could not describe secret {ret['comment']}")
        return {}

    result = {}
    for secret in ret["ret"].items:
        secret_resource = (
            hub.tool.k8s.core.v1.secret_utils.convert_raw_secret_to_present(
                secret=secret
            )
        )
        result[secret.metadata.name] = {
            "k8s.core.v1.secret.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in secret_resource.items()
            ]
        }
    return result
