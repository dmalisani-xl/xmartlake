import threading
import grpc
import bots_pb2
import bots_pb2_grpc
import time

from kubernetes import client, config

NAMESPACE = "xmartlake"
CONTAINER_PORT = 50000

config.load_incluster_config()

k8s_client = client.CoreV1Api()
k8s_apps_v1 = client.AppsV1Api()

# # Use the client object to list pods in the "xmartlake" namespace
pods = k8s_client.list_namespaced_pod(namespace=NAMESPACE)


def list_pods():
    pods = k8s_client.list_namespaced_pod(namespace=NAMESPACE)
    for i in pods.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


def send_when_ready(bot_id: str, parameter: str) -> str:
    # Wait until the pod is in the 'Running' state
    print(f"Waiting for bot {bot_id}")
    pod_name = f'{bot_id}-'
    breaker_count = 0
    pod = None
    while True:
        pods = k8s_client.list_namespaced_pod(namespace=NAMESPACE, label_selector=f'app={bot_id}')
        if len(pods.items) > 0:
            pod = pods.items[0]
            if pod.status.phase == 'Running':
                print("Bot was started")
                break
        time.sleep(1)
        breaker_count += 1
        if breaker_count > 3:
            raise RuntimeError(f"{pod_name} is not ready")
        

    # Wait until the gRPC service is ready
    channel = grpc.insecure_channel(f'{pod.status.pod_ip}:{CONTAINER_PORT}')
    stub = bots_pb2_grpc.TurnCallerStub(channel)
    ping_count = 0
    response = None
    while True:
        try:
            response = stub.ping(bots_pb2.EmptyMessage())
            print("PING-----------")
            print(response)
            if response.ack == 'pong':
                print("The POD is ready to receive GRPC")
                break
                
        except Exception as e:
            print(f"Waiting... {e}")
        list_pods()
        time.sleep(1)
        ping_count += 1
        print(f"Retrying. {ping_count}")
        if ping_count > 3:
            raise RuntimeError(f"{pod_name} is not ready")

    try:
        call_parameter = bots_pb2.TurnMessage(parameter=parameter)
        print(call_parameter)
        response = stub.play(call_parameter)
        print(response)
    except Exception as e:
        print(e)
        raise RuntimeError(e)
    return response.response


def create_new_bot(bot_id: str):
    deployment = make_deployment(bot_id)
    print("------ Creating deployment ------")
    _ = k8s_apps_v1.create_namespaced_deployment(body=deployment, namespace=NAMESPACE)
    list_pods()


def delete_bot_deployment(bot_id: str):
    # Delete the deployment
    deployment_name = f'deployment-{bot_id}'
    # delete_replica_sets(deployment_name)

    print("------ Destroying deployment ------")
    k8s_apps_v1.delete_namespaced_deployment(
        name=deployment_name,
        namespace=NAMESPACE,
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=0
        )
    )

    # Wait until the deployment is deleted
    while True:
        try:
            k8s_apps_v1.read_namespaced_deployment(name=deployment_name, namespace=NAMESPACE)
        except client.exceptions.ApiException as e:
            if e.status == 404:
                break
        time.sleep(1)


def delete_replica_sets(deployment_name: str):
    label_selector = f'app={deployment_name}'
    replicasets = k8s_apps_v1.list_namespaced_replica_set(namespace=NAMESPACE, label_selector=label_selector)
    for replicaset in replicasets.items:
        replicaset_name = replicaset.metadata.name
        print(f"Deleting replicaset {replicaset_name}")
        k8s_apps_v1.delete_namespaced_replica_set(
            name=replicaset_name,
            namespace=NAMESPACE,
            body=client.V1DeleteOptions(
                propagation_policy='Orphan',
                grace_period_seconds=0
            )
        )
def call_to_bot(bot_id: str, parameter: str) -> str:
    try:
        create_new_bot(bot_id)
        response = send_when_ready(bot_id, parameter)
    except RuntimeError:
        print("Pod is not working")
        response = "XXX"

    delete_thread = threading.Thread(target=delete_bot_deployment, args=(bot_id,))
    delete_thread.start()
    print(f"Returning response: {response}")
    return response


def make_deployment(bot_id: str) -> client.V1Deployment:
  

  # Create a Kubernetes API client
  api_client = client.ApiClient()

  # Define the deployment's metadata
  metadata = client.V1ObjectMeta(name=f'deployment-{bot_id}')
  envs = [
      client.V1EnvVar(name="IMAGE_NAME", value=f"{bot_id}"),
      client.V1EnvVar(name="GRPC_PORT", value=f"{CONTAINER_PORT}")
  ]
  # Define the deployment's container spec
  container_spec = client.V1Container(
      name=bot_id,
      image=f'{bot_id}:latest',
      image_pull_policy="Never",
      ports=[client.V1ContainerPort(container_port=CONTAINER_PORT)],
      env=envs
  )

  # Define the deployment spec
  spec = client.V1DeploymentSpec(
      replicas=1,
      selector=client.V1LabelSelector(match_labels={'app': bot_id}),
      template=client.V1PodTemplateSpec(
          metadata=client.V1ObjectMeta(labels={'app': bot_id}),
          spec=client.V1PodSpec(containers=[container_spec])
      )
  )

  # Create the deployment object
  deployment = client.V1Deployment(
      api_version='apps/v1',
      kind='Deployment',
      metadata=metadata,
      spec=spec
  )
  return deployment