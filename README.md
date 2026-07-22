
# Project Title

A personal app that transforms your phone into the center of an automated financial hub. For those who hate the traditional budgeting apps, and writing all your expenses by hand.


## Tech Stack

**Server:** Python, FastAPI, PostgreSQL, Docker

**Client:** MacroDroid (for development), Flutter (intended for the final app)



## Architecture

1. Dockerized microservices:
- Parser: Implements a webhook to receive and the notifications generated in the client, ans the processes to extract information (like transaction amount or if it is outcome/income) from raw text.
- Core: Implements a CRUD interface for both Accounts and Transactions, persisting them in strict relational formats using PostgreSQL.

2. Client (for development):
- [MacroDroid](https://www.macrodroid.com/) (external app) allows you to create automations in your phone. Used during development to test data gathering and flow.

So the system generates the data on the phone, sends requests using MacroDroid for automation to the Parser service and it communicates through an internal Docker network with Core service for data persistance.
## Prerequisites
-Git  
-Python 3.14+  
-Docker  
## Installation
1. Clone the repo locally
```bash
git clone https://github.com/alonso-git/FoxVault
```

2. Create the Docker network
```bash
sudo docker network create foxvault_network
```

3. Compose the containers (run this inside the main directory of the project):
```bash
cd Core
sudo docker compose up -d
cd ../Parser
sudo docker compose up -d
```

4. Verify the status:
```bash
sudo docker logs core-service
sudo docker logs parser-serrvice
```

5. Install MacroDroid in your phone (if you got an iPhone, search for a similar app)
- **Open the app and click "Add Macro"**
- **Trigger**
- Click the "+" symbol on the "Triggers" card
- Click the section "Device Events"
- Select "Notification" and "Notificacion Received" on the pop up. Click "OK"
- In the "Applications" section (on op) click the square button and choose a bank app (I know this can sound unsafe, so you can choose another non-sensitive app and try the system before)
- Click "Ok" and "OK" again. Trigger is set
- **Action**
- Click the "+" symbol on the "Actions" tab
- Click the section "Web Interactions"
- Select "HTTP Request"
- Select "POST" in the "Request method"
- For the URL, you will need to know where your app is running. An option is [Cloudlflare Tunnels](https://try.cloudflare.com/) which you can try quickly, or set up a local network. We use a permanent, public [Cloudflare Access Tunnel](https://www.cloudflare.com/sase/products/access/). After your host URL, append the Transaction Ingester Endpoint URL listed below.
- Switch to the "Content Body" tab and paste the following in the field "Text":
```json
{
"origin_app": "{not_app_name}",
"origin_device":"{device_manufacturer} {device_model}",
"title":"{not_title}",
"body":"{notification}",
"timestamp":"{year}-{month_digit}-{dayofmonth}T{hour_0}:{minute}:{second}"
}
```
- Click the checkmark "✓" button. Action is set

- **Name and save**
- Give it a name in the top text field
- Click the three dot menu and then "Save changes". Macro is set
## Endpoints

- Transaction Ingester Endpoint:
```bash
{host_url}/api/v1/payments/webhook/
```
## Repo Structure

Two main directories live in the repo: "Core" and "Parser"

Each one is an independent FastAPI project, with its own Docker configuration and they need (if you are going to make changes/develop the project) individual venv.

Setting up the repo for local development is straightforward:

1. Navigate to the main directory (eg. FoxVault)
2. Navigate to each service's directory, create the venv and install the dependencies. Do not forget to deactivate the venv when you are going to switch between developing one service to the other (it is not usual, but you could get interpreter errors, they are annoying)
```bash
cd Core
python -m venv venv
# or
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

cd ../Parser
# Repeat the process
```