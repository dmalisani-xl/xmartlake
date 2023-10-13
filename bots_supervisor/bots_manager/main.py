import threading
import grpc
import bots_pb2
import bots_pb2_grpc
import time

from uuid import uuid4

from kubernetes import client, config
from kubernetes.client.rest import ApiException


NAMESPACE = "xmartlake"
CONTAINER_PORT = 50000

try:
    # Try to load in-cluster config
    config.load_incluster_config()
except config.config_exception.ConfigException:
    # Fallback to kubeconfig when outside of the cluster
    config.load_kube_config()

k8s_client = client.CoreV1Api()
k8s_apps_v1 = client.AppsV1Api()

# # Use the client object to list pods in the "xmartlake" namespace
pods = k8s_client.list_namespaced_pod(namespace=NAMESPACE)


def get_pod_name_ip(bot_id: str):
    pods = k8s_client.list_namespaced_pod(namespace=NAMESPACE, label_selector=f'app={bot_id}')
    return (pods.items[0].metadata.name, pods.items[0].status.pod_ip) if (len(pods.items) and getattr(pods.items[0], "status")) else None, None


def send_when_ready(bot_id: str, parameter: str) -> str:
    # Wait until the pod is in the 'Running' state
    print(f"Waiting for bot {bot_id}")
    breaker_count = 0

    # Wait until the gRPC service is ready
    while True:
        if pod_is_running(bot_id):
            print("Pod is running")
            break
        print("Waiting for pod")
        time.sleep(1)
        breaker_count += 1
        if breaker_count > 3:
            raise RuntimeError(f"{pod_name} is not ready")
        
    pod_name, pod_ip = get_pod_name_ip(bot_id)
    print(f"Name: {pod_name}  ID: {bot_id}  IP: {pod_ip}")
    if not pod_ip:
        raise Exception("Pod not found")
    channel = grpc.insecure_channel(f'{pod_ip}:{CONTAINER_PORT}')
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
    return pod_name, response.response



def create_new_deployment(bot_id: str):

    deployment = make_deployment(bot_id)
    print("------ Creating deployment ------")
    dep = None
    for attempt in (1, 2):
        try:
            dep = k8s_apps_v1.create_namespaced_deployment(body=deployment, namespace=NAMESPACE, async_req=False)
            print("--- Deployment created ---")
            break
        except ApiException as e:

            print(f"--- Error on attempt {attempt}")
            
            print(repr(e))
            if attempt < 2:
                time.sleep(10)
            else:
                raise
    return dep

def delete_bot_deployment(deployment_name: str):
    # Delete the deployment

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

def delete_pod(deployment_name: str):
    # Delete the deployment
    print(f"Deleting pod {deployment_name}")
    k8s_client.delete_namespaced_pod(name=deployment_name, namespace=NAMESPACE)



def reset_pod(bot_id: str):
    print("Deleting pod")
    bot_name, _ = get_pod_name_ip(bot_id)
    try:
        print(f"Down {bot_name}")
        k8s_client.patch_namespaced_deployment_scale(
            name=bot_name,
            namespace=NAMESPACE,
            body={"spec": {"replicas": 0}}
        )
        time.sleep(2)
        print(f"Up {bot_name}")
        k8s_client.patch_namespaced_deployment_scale(
            name=bot_name,
            namespace=NAMESPACE,
            body={"spec": {"replicas": 1}}
        )

    except Exception as e:
        print(e)


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

def restart_pod(bot_id):
  pod_name, _ = get_pod_name_ip(bot_id)
  try:
    pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=NAMESPACE)
  except ApiException as e:
    if e.status == 404:
      print('Pod not found: {}'.format(pod_name))
      return False
    else:
      raise

  # Create a new pod object with the same spec as the existing pod.
  k8s_client.create_namespaced_pod(namespace=NAMESPACE)
  new_pod = k8s_client.client.V1Pod(
      metadata=pod.metadata,
      spec=pod.spec)

  # Update the restart count of the new pod.
  new_pod.metadata.annotations['kubectl.kubernetes.io/restart'] = str(pod.metadata.annotations['kubectl.kubernetes.io/restart'] + 1)

  # Patch the existing pod with the new pod object.
  k8s_apps_v1.patch_namespaced_pod(name=pod_name, namespace=NAMESPACE, body=new_pod)

  return True



def pod_is_running(bot_id):
    pods = k8s_client.list_namespaced_pod(namespace=NAMESPACE, label_selector=f'app={bot_id}')
    if len(pods.items) > 0:
        pod = pods.items[0]
        if pod.status.phase == 'Running':
            return True
    return False


def get_deploment_name(bot_id):
    deployment_name = None
    deployments = k8s_apps_v1.list_namespaced_deployment(namespace=NAMESPACE, label_selector=f'app={bot_id}')
    for deployment in deployments.items:
        deployment_name = deployment.metadata.name
    return deployment_name


def call_to_bot(bot_id: str, parameter: str) -> str:
    dep_name = get_deploment_name(bot_id)
    if not dep_name:
        dep = create_new_deployment(bot_id)
        dep_name = dep.metadata.name
        print(f"//Deployment created: {dep_name} for bot: {bot_id}")
    else:
        print(f"Found deployment: {dep_name} for {bot_id}")
    
    try:
        response = send_when_ready(bot_id, parameter)

    except RuntimeError:
        print(f"Pod {bot_id} is not working")
        response = "XXX"

    # delete_thread = threading.Thread(target=delete_pod, args=(dep_name,))
    # delete_thread.start()
    delete_pod(bot_id)
    print(f"Returning response: {response}")
    return response


def make_deployment(bot_id: str) -> client.V1Deployment:
  

  # Create a Kubernetes API client
  api_client = client.ApiClient()

  # Define the deployment's metadata
  bot_name = f"bot-{str(uuid4())}"
  metadata = client.V1ObjectMeta(name=bot_name, labels={'bot-id': bot_id})
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
