from kubernetes import client, config
config.load_kube_config()

v1 = client.CoreV1Api()

def create_new_bot():
    ...


def call_to_bot(bot_id: str) -> str:
    ...


def _make_deployment_code(bot_id) -> str:

    dep = """
    {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {
        "name": "hello-python-dep"
    },
    "spec": {
        "selector": {
        "matchLabels": {
            "app": "hello-python-app"
        }
        },
        "replicas": 1,
        "template": {
        "metadata": {
            "labels": {
            "app": "hello-python-app"
            }
        },
        "spec": {
            "containers": [
            {
                "name": "hello-python",
                "image": "daniel:latest",
                "imagePullPolicy": "Never",
                "ports": [
                {
                    "containerPort": 5000
                }
                ]
            }
            ]
        }
        }
    }
    }
    """
k8s_apps_v1 = client.AppsV1Api()

resp = k8s_apps_v1.create_namespaced_deployment(body=dep, namespace="default")

