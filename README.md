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
src: Contains the application code in JAVA17, SpringBoot framework is used.

Please note that our preferred language is Python.
Python.

Part 1: Infrastructure and IaC
Identify the infrastructure necessary to ingest, store and expose data: Use the Pub/Sub scheme: Pubsub scheme is used, for this 3 enpoints are exposed.

POST: https://post-request-dot-watchful-pier-422221-q7.uc.r.appspot.com/ (Create a theme)
PUT: https://post-request-dot-watchful-pier-422221-q7.uc.r.appspot.com/ (Update a theme)
GET: https://post-request-dot-watchful-pier-422221-q7.uc.r.appspot.com/{id} (Get messages from a topic)

b. Database for storage focused on data analytics.
A Database is used in GCP under the Sql Cloud service, name **database_latam**, Mysql 8 engine.
c. HTTP endpoint to serve part of the stored data.

POST: https://post-request-dot-watchful-pier-422221-q7.uc.r.appspot.com/ (Create a theme)
PUT: https://post-request-dot-watchful-pier-422221-q7.uc.r.appspot.com/ (Update a theme)
GET: https://post-request-dot-watchful-pier-422221-q7.uc.r.appspot.com/{id} (Get messages from a topic)
Deploy infrastructure using Terraform in the way that best suits you. Include Terraform source code.
Terraform is used to deploy the database, the only infrastructure component that we would be using.

main.tf
provider.tf

Part 2: Applications and CI/CD flow
HTTP API: Set up an HTTP endpoint with logic that reads data from the database and exposes it when receiving a GET request.

Invocation Method:
https://post-request-dot-watchful-pier-422221-q7.uc.r.appspot.com/

CI-CD deployment method:
 .github/workflows/deploy.yml