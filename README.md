# Radius Authentication using REST API Call
In this lab environments, we will configure a radius server which will authenticate user not by himself but making API call to a server. Based on the response from API server radius will authenticate or not that user. Use case scenario might be that If we have user list database in our application backend then we can leverage this to verify user and authenticate. Because of AAA server capabilities, we can also extend this to manage authorization and account related operation but here we will only work on remote user authentication.

# Requirements:
  **VM1: Radius Server (192.168.56.104/24)**\
  **VM2: API Server (192.168.56.106/24)**
  
# Scenario:
Network Access Server (NAS) is a device that provides an access point to the network for remote users connecting using SLIP, PPP, or any other remote access protocol. The NAS transmits the information provided in the connection request from the remote user to the RADIUS server. Here wireless controller act as NAS server. Then RADIUS server checks this information against the user and returns to the NAS an authentication, authorization or denial for the remote user connection. \
The RADIUS server **(192.168.56.104)** checks user information against the entry for the remote user in various methods. It can use local or remote mysql database, LDAP, Active Directory etc. But in this scenario radius server will not authenticate remote user by himself but relay this information to a server **(192.168.56.106)** via REST API call. Then the API server will verify the user credential and give response to the radius server. On the basis of API response from the server radius will allow or deny the user accordingly.

![](images/topo-1.png)

# Environment Setup:
We will use Ubuntu 22.04.2 LTS for lab setup. FreeRADIUS is a modular, high performance free RADIUS application which is absolutely free. We will use it as radius server deployment. It will be deployed under an Ubuntu VM for which the IP address is **192.168.56.104** . Also, for emulating API server functionality, we will use Python and Flask module. That will be configured on another VM with IP address of **192.168.56.104** .

# API Server Configuration:
For API server functionality we will use a python script where Flask is used to for emulation API endpoint where radius will communicate through API call with user credentials. Then Server will verify this credentials with its own internal mechanism. it can verify user with backend user database query. Here, we will hardcode only one user information into script for simplicity. I think it will fulfill the purpose of this experiment. We will create a python script called **erp.py** .

### erp.py

```
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    # Hardcoded authentication logic
    if username == 'user1' and password == 'pass1':
        authenticated = "ok"
        response = {'authenticated': authenticated}
        return jsonify(response)

    else:
        return Response(
        "Authentication Not Allowed!",
        status=400,
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

```
It is a simple script that will listen on 5000 port while running. It accepts API request on URI **/authenticate** . When Radius will receive user authentication request from wireless controller, it will send that user information as JSON data onto API end point. Then API server will verify this information. If user information is correct then it will response HTTP 200 means allow. Otherwise it will deny by sending HTTP 400 response. Based on reply from API server, radius will allow or deny the user request.

### Running API Script:

execute erp.py

```bash
  python3 erp.py
```
![](images/api-1.png)

Now, we will keep this script running and configure radius server.

# API Server Configurstion:
In radius server VM, we will install and configure FreeRADIUS software. For this we need to install some packages. 

### Install FreeRADIUS:

To install FreeRADIUS, run the following command:

```bash
  apt install freeradius freeradius-rest freeradius-utils
```
### Configure FreeRADIUS:

We need to edit several files to configure:
