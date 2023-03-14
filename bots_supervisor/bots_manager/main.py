import grpc
import bots_pb2
import bots_pb2_grpc
import logging
import os

from kubernetes import client, config

logger = logging.getLogger()

    #config.load_kube_config('kubeconfig',persist_config=True)

logger.debug("----1")
aConfiguration = client.Configuration()
aConfiguration.host = os.getenv("KUBERNETES_HOST")
print(f"Kubernetes_host: {aConfiguration.host}")


aConfiguration.verify_ssl = False
# aConfiguration.api_key = kube_api_key

# v1 = client.ApiClient(aConfiguration)


# Do calls
# api_response = v1.list_namespaced_pod('default')



# cv1 = client.CoreV1Api(v1)
# print(dir(cv1))
# k8s_apps_v1 = client.AppsV1Api(v1)
# print(dir(k8s_apps_v1))


def create_new_bot(bot_id: str):
    deployment_code = _make_deployment_code(bot_id)
    with client.ApiClient(aConfiguration) as api_client:
        api_instance = client.AppsV1Api(api_client)
        print("---------------")
        print(api_instance.list_daemon_set_for_all_namespaces())
        print("---------------")
        resp = api_instance.create_namespaced_deployment(
            body=deployment_code,
            namespace="default"
        )
        print(resp)


def call_to_bot(bot_id: str, parameter: str) -> str:
    create_new_bot(bot_id)
    for x in range(3):
        print(f"Trying #{x}")



def _make_deployment_code(bot_id) -> str:
    dep = """
    {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {
        "name": "{{bot_id}}"
    },
    "spec": {
        "selector": {
        "matchLabels": {
            "app": "{{bot_id}}"
        }
        },
        "replicas": 1,
        "template": {
        "metadata": {
            "labels": {
            "app": "{{bot_id}}"
            }
        },
        "spec": {
            "containers": [
            {
                "name": "hello-python",
                "image": "{{bot_id}}:latest",
                "imagePullPolicy": "Never",
                "ports": [
                    {
                        "containerPort": 50000
                    }
                ],
                "env":[
                    "IMAGE_NAME": "{{bot_id}}",
                    "GRPC_PORT": 50000
                ]
            }
            ]
        }
        }
    }
    }
    """
    return dep.replace("{{bot_id}}", bot_id)





