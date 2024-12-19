# Kubernetes Pod Log Analyzer

This repository contains a Python script for analyzing Kubernetes pod logs. It helps in extracting log data from specific pods based on labels, checks for container restarts, flags error messages, and saves the results in a log file.

## Features

- Fetches logs of pods within a specified namespace using a label selector.
- Monitors restart counts and flags containers exceeding the restart threshold.
- Searches logs for error messages or failure-related keywords such as "Error", "Failed", or "Crashloopback".
- Logs findings (restart counts and flagged errors) into a specified output file.

## Prerequisites

Before running the script, ensure the following:

- Python 3.6 or later.
- **A running Kubernetes cluster**. You can use any of the following options:
  - **Minikube**: A local Kubernetes cluster setup tool.
  - **Kubeadm**: A tool for managing a Kubernetes cluster, typically used for setting up production environments.
  
  If you don't have a Kubernetes cluster running, you can set up Minikube or Kubeadm. Minikube is a great option for a local cluster for testing purposes.

  - **Minikube setup**: [Install Minikube](https://minikube.sigs.k8s.io/docs/)
  - **Kubeadm setup**: [Install Kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)

- Kubernetes cluster access and kubeconfig file set up (`~/.kube/config`).
- Required Python libraries: `kubernetes`.

You can install the required Python libraries using `pip`:

```bash
pip install kubernetes
```

## Usage

The script can be run from the command line with the following syntax:

```bash
python kubernetes_log_analyzer.py --namespace <namespace> --label-selector <label-selector> --restart-threshold <restart-threshold> --output-file <output-file-path>
```

### Arguments

- `--namespace`: The Kubernetes namespace of the pods to analyze. (Required)
- `--label-selector`: The label selector to filter pods. (Required)
- `--restart-threshold`: The threshold for restarts at which a warning will be logged. (Required)
- `--output-file`: The file path where logs and analysis results will be stored. (Required)

### Example

```bash
python kubernetes_log_analyzer.py --namespace my-namespace --label-selector app=my-app --restart-threshold 5 --output-file /path/to/output.log
```

This will analyze all pods in the `my-namespace` namespace with the label `app=my-app`, check for pods that have restarted more than 5 times, and save the results in `/path/to/output.log`.

## Code Explanation

### 1. **parse_arguments()**
   - This function uses `argparse` to handle command-line arguments, ensuring that the required parameters are provided for the script to run.

### 2. **log_message()**
   - A helper function to format log messages with timestamps and write them to the output file.

### 3. **main()**
   - The main function that:
     1. Loads the Kubernetes configuration.
     2. Fetches all pods in the specified namespace with the provided label selector.
     3. Checks if any container in the pods has exceeded the restart threshold.
     4. Retrieves logs for each container and flags any lines containing error keywords.
     5. Writes the log data and any flagged errors to the specified output file.

### 4. **Error Handling**
   - Handles potential errors gracefully, such as issues with fetching pod data or logs, by logging error messages in the output file.

## Example Output

### Log Entries for Restart Warnings

```plaintext
2024-12-19 12:34:56 - Pod my-pod, Container: my-container - Restarts: 6 has exceeded the restart threshold of 5
```

### Log Entries for Error Flags

```plaintext
2024-12-19 12:35:01 - Pod: my-pod, Container: my-container - Error: Connection refused
2024-12-19 12:35:05 - Flagged: Error: Connection refused
```

