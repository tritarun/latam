# latam
this repo is for Latam DevSecOps/SRE Technical Challenge

Advance instructions
Use a public git repository to solve the challenge
https://github.com/tritarun/latam

Use a master branch and a develop branch when solving the problem
Gitflow is used using the master branch (main), develop (base for features) and the feature branches for the different developments.

All the files used to resolve the challenge must be in the repository.
.github/worflow: Contains the CI/CD.
Iac: Contains the terraforms for the deployment of the infrastructure.


Please note that language used is Python.


Part 1:Infraestructura e IaC
Identify the infrastructure necessary to ingest, store and expose data: Use the Pub/Sub scheme: Pubsub scheme is used, for this 3 enpoints are exposed.


POST: https://post-request-dot-watchful-pier-422221-q7.uc.r.appspot.com/api/data (Create a theme)
PUT: https://post-request-dot-watchful-pier-422221-q7.uc.r.appspot.com/api/data (Update a theme)
GET: https://post-request-dot-watchful-pier-422221-q7.uc.r.appspot.com/api/data/<id> (Get messages from a topic)

b. Database for storage focused on data analytics.
A Database is used in GCP under the Sql Cloud service, name **latam-database**, Mysql 8 engine.
c. HTTP endpoint to serve part of the stored data.

POST: https://post-request-dot-watchful-pier-422221-q7.uc.r.appspot.com/api/data (Create a theme)
PUT: https://post-request-dot-watchful-pier-422221-q7.uc.r.appspot.com/api/data (Update a theme)
GET: https://post-request-dot-watchful-pier-422221-q7.uc.r.appspot.comapi/data/<id> (Get messages from a topic)
Deploy infrastructure using Terraform in the way that best suits you. Include Terraform source code.
Terraform is used to deploy the database, the only infrastructure component that we would be using.

main.tf
provider.tf

Part 2: Aplicaciones y flujo CI/CD
HTTP API: Set up an HTTP endpoint with logic that reads data from the database and exposes it when receiving a GET request.

Invocation Method:
https://post-request-dot-watchful-pier-422221-q7.uc.r.appspot.com/api/data

CI-CD deployment method:
 .github/workflows/deploy.yml

Results:
POST

{
  "nombre": "Your Tema Name- Valpo"
}

GET

curl https://post-request-dot-watchful-pier-422221-q7.uc.r.appspot.com     
{"data":[[1,"Your Tema Name"],[2,"Your Tema Name"],[3,"Your Tema Name- Valpo"]]}

![GET Response](/images/Get_Response.png)

It includes an architecture diagram with the infrastructure from point 1.1 and its interaction with the services/applications that demonstrates the end-to-end process from ingestion to consumption by the HTTP API.

Serverless technology used: App Engine GCP

![GET Response](/images/Architecture_Latam_Challange.jpg)

Part 3: Pruebas de Integración y Puntos Críticos de Calidad


Part 4: Métricas y Monitoreo

1.Propose 3 metrics (in addition to the basic CPU/RAM/DISK USAGE) critical to understanding the health and performance of the end-to-end system

network
sys load
filesystem

2.Propose a visualization tool and describe verbatim what metrics it would show, and how this information would allow us to understand the health of the system to make strategic decisions

Grafana stands out as an open source platform used in data analysis and extraction of information and metrics. Grafana, like other platforms, shows us several metrics, but we will focus on the 3 basic ones:

CPU
RAM
disk usage

These metrics allow us to identify the amount of use that our system has on the machine that is running. By exceeding the established limits and being informed by alerts, we can perform vertical escalations or auto-scaling (add more resources) or horizontal (add more machines). , all this to complement the original and thus not allow our application to crash due to overload.

3.It broadly describes what the implementation of this tool in the cloud would be like and how it would collect system metrics.

It can be easily installed in a Kubernetes cluster through its yaml.

The Grafana operator imports Grafana resources that are created during application installation. The GrafanaDashboard scans the resources in all namespaces and now the resources are visible. Dashboards are organized into folders that correspond to namespaces. Expand a folder to view dashboards.

4.Describe how the visualization will change if we scale the solution to 50 similar systems and what other metrics or forms of visualization this scaling allows us to unlock.

The visualization will be more complicated, which is why the technical resource intended to monitor it will be essential. Metrics:

GroupMinSize: The minimum size of the Auto Scaling group.
GroupMaxSize: The maximum size of the Auto Scaling group.
GroupStandbyInstances: The number of instances that have the Standby state. Instances with this state are still running but are not in service.
GroupTerminatingInstances: The number of instances being terminated. This metric does not include instances that are in service or pending.

5.Comment on what difficulties or limitations could arise at the level of observability of the systems if the scalability problem is not correctly addressed.

We may have difficulties or limitations in establishing the amount of resources that are being created for the use of our applications.

Part 5: Alertas y SRE (Opcional)

1.Specifically define what rules or thresholds you would use for the proposed metrics, so that alerts are triggered to the team when system performance declines. Argue.

GroupMinSize: If the number of machines is less than the GroupMinSize, trigger an alert.
GroupMaxSize: If the number of machines is greater than the GroupMaxSize, trigger an alert.
GroupStandbyInstances: If the number exceeds 10%, trigger an alert.
GroupStandbyInstances: As soon as one is finished, trigger an alert.
GroupMinSize, due to application response time issues, this number cannot be lower.
GroupMaxSize, due to cloud costs, this number cannot be higher.
GroupStandbyInstances, if we have more than 10% that are running and are not in service, it may worsen the system's response times.
GroupStandbyInstances, as soon as a machine is finished we must know which one it was and why it is in this state.

2.Defines SLI metrics for system services and an SLO for each of the SLIs. Argue why you chose those SLIs/SLOs and why you discarded other metrics to use them within the definition of SLIs.

SLI metrics
totalServiceFilter : A metric that counts the total number of events. SLI: 99.95%.
badServiceFilter : In a metric that counts “bad” events. SLI: 99.95%.

These metrics are important for the business, to be clear about the number of events that occur in our system and the number of incorrect events, this allows improvements to be made in both the software and the equipment.