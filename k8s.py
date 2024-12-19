import sys
import datetime
import argparse
from kubernetes import client, config
from kubernetes.client.rest import ApiException

# Getting Arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Kubernetes Pod Log Analyzer")
    parser.add_argument("--namespace", help="Namespace of the pod", required=True)
    parser.add_argument("--label-selector", help="Label selector of the pod", required=True)
    parser.add_argument("--restart-threshold", type=int, help="Restart Threshold For Warnings", required=True)
    parser.add_argument("--output-file", help="Path to save the logs", required=True)
    return parser.parse_args()

# Defining a log Format
def log_message(message, outputfile):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(outputfile, "a") as f:
        f.write(f"{timestamp} - {message}\n")

def main():
    args = parse_arguments()
    namespace = args.namespace
    label_selector = args.label_selector
    restart_threshold = args.restart_threshold
    output_file = args.output_file

    # Load Kubernetes Configuration
    try:
        config.load_kube_config()
    except Exception as e:
        print(f"Error: Unable to load Kubernetes configuration: {e}")
        sys.exit(1)

    v1 = client.CoreV1Api()

    try:
        pods = v1.list_namespaced_pod(namespace, label_selector=label_selector).items
    except ApiException as e:
        print(f"Error Fetching pods: {e}")
        sys.exit(1)

    if not pods:
        log_message(f"No pods found in namespace '{namespace}' with the label selector '{label_selector}'", output_file)
        return

    error_keywords = ["Error", "Failed", "Crashloopback"]

    for pod in pods:
        pod_name = pod.metadata.name
        for container_status in pod.status.container_statuses or []:
            container_name = container_status.name
            restart_count = container_status.restart_count

            # Log if restart count exceeds threshold
            if restart_count >= restart_threshold:
                log_message(f"Pod {pod_name}, Container: {container_name} - Restarts: {restart_count} has exceeded the restart threshold of {restart_threshold}", output_file)

            try:
                # Get the logs for the container in the pod
                logs = v1.read_namespaced_pod_log(
                    namespace=namespace,
                    name=pod_name,
                    container=container_name,
                    timestamps=True
                )
            except ApiException as e:
                log_message(f"Error fetching logs for Pod: {pod_name}, Container: {container_name} - {e}", output_file)
                continue

            # Split logs into lines and process each line
            log_lines = logs.splitlines()
            for line in log_lines:
                log_message(f"Pod: {pod_name}, Container: {container_name} - {line}", output_file)

                # Flag errors in logs
                if any(keyword in line for keyword in error_keywords):
                    log_message(f"Flagged: {line}", output_file)

if __name__ == "__main__":
    main()
