
## Helm chart

This image comes with its own helm chart. The chart versions are aligned with the releases of the image. Charts are hosted
through this repository.

To install the image, simply do the following:

```shell script
helm repo add bokysan https://bokysan.github.io/docker-postfix/
helm upgrade --install --set persistence.enabled=false --set config.general.ALLOWED_SENDER_DOMAINS=example.com mail bokysan/mail
```

Chart configuration is as follows:

| Property | Default value | Description |
|----------|---------------|-------------|
| `replicaCount` | `1` | How many replicas to start |
| `image.repository` | `boky/postfix` | This docker image repository |
| `image.tag` | *empty* | Docker image tag, by default uses Chart's `AppVersion` |
| `image.pullPolicy` | `IfNotPresent` | [Pull policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for the image |
| `imagePullSecrets` | `[]` | Pull secrets, if neccessary |
| `nameOverride` | `""` | Override the helm chart name |
| `fullnameOverride` | `""` | Override the helm full deployment name |
| `serviceAccount.create` | `true` | Specifies whether a service account should be created |
| `serviceAccount.annotations` | `{}` | Annotations to add to the service account |
| `serviceAccount.name` | `""` | The name of the service account to use. If not set and create is true, a name is generated using the fullname template |
| `service.type` | `ClusterIP` | How is the server exposed |
| `service.port` | `587` | SMTP submission port |
| `service.labels` | `{}` | Additional service labels |
| `service.annotations` | `{}` | Additional service annotations |
| `service.spec` | `{}` | Additional service specifications |
| `service.nodePort` | *empty* | Use a specific `nodePort` |
| `service.nodeIP` | *empty* | Use a specific `nodeIP` |
| `resources` | `{}` | [Pod resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) |
| `autoscaling.enabled` | `false` | Set to `true` to enable [Horisontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) |
| `autoscaling.minReplicas` | `1` | Minimum number of replicas |
| `autoscaling.maxReplicas` | `100` | Maximum number of replicas |
| `autoscaling.targetCPUUtilizationPercentage` | `80` | When to scale up |
| `autoscaling.targetMemoryUtilizationPercentage` | `""` | When to scale up |
| `autoscaling.labels` | `{}` | Additional HPA labels |
| `autoscaling.annotations` | `{}` | Additional HPA annotations |
| `nodeSelector` | `{}` | Standard Kubernetes stuff |
| `tolerations` | `[]` | Standard Kubernetes stuff |
| `affinity` | `{}` | Standard Kubernetes stuff |
| `certs.create` | `{}` | Auto generate TLS certificates for Postfix |
| `extraVolumes` | `[]` | Append any extra volumes to the pod |
| `extraVolumeMounts` | `[]` | Append any extra volume mounts to the postfix container |
| `extraInitContainers` | `[]` | Execute any extra init containers on startup |
| `extraEnv` | `[]` | Add any extra environment variables to the container |
| `extraContainers` | `[]` | Add extra containers |
| `deployment.labels` | `{}` | Additional labels for the statefulset |
| `deployment.annotations` | `{}` | Additional annotations for the statefulset |
| `pod.securityContext` | `{}` | Pods's [security context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) |
| `pod.labels` | `{}` | Additional labels for the pod |
| `pod.annotations` | `{}` | Additional annotations for the pod |
| `container.postfixsecurityContext` | `{}` | Containers's [security context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) |
| `config.general` | `{}` | Key-value list of general configuration options, e.g. `TZ: "Europe/London"` |
| `config.postfix` | `{}` | Key-value list of general postfix options, e.g. `myhostname: "demo"` |
| `config.opendkim` | `{}` | Key-value list of general OpenDKIM options, e.g. `RequireSafeKeys: "yes"` |
| `secret` | `{}` | Key-value list of environment variables to be shared with Postfix / OpenDKIM as secrets |
| `mountSecret.enabled` | `false` | Create a folder with contents of the secret in the pod's container |
| `mountSecret.path` | `/var/lib/secret` | Where to mount secret data |
| `mountSecret.data` | `{}` | Key-value list of files to be mount into the container |
| `persistence.enabled` | `true` | Persist Postfix's queue on disk |
| `persistence.accessModes` | `[ 'ReadWriteOnce' ]` | Access mode |
| `persistence.existingClaim` | `""` | Provide an existing `PersistentVolumeClaim`, the value is evaluated as a template. |
| `persistence.size` | `1Gi` | Storage size |
| `persistence.storageClass` | `""` | Storage class |
| `recreateOnRedeploy` | `true` | Restart Pods on every helm deployment, to prevent issues with stale configuration(s). |
