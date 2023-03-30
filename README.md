>[name=Yueh-Huan Chung][time=Wed, Mar 29, 2023 7:33 AM]

## Develop
### Protocol Buffer

**Compile protocol buffer from protoc to python:**
```bash=
cd src/protobuf
python3 -m grpc_tools.protoc -I=. --python_out=. --pyi_out=. --grpc_python_out=. rc.proto
```

### Re-build the Docker Image
```bash=
sudo docker build -t mooncake22/slicexapp:0.0.1 .
```

## Use
**Intro**
Currently, we have tested slicexapp with OSC F release Near-RT RIC platform and successfully integrated with OSC F Release Non-RT RIC.

Do remember to install dmscli tool from [appmgr](https://gerrit.o-ran-sc.org/r/gitweb?p=ric-plt%2Fappmgr.git;a=summary) first.

### Step 1: Setup Environment & Build Docker Image
- Export chart ENV for dmscli
```bash=
sudo export NODE_PORT=$(kubectl get --namespace ricinfra -o jsonpath="{.spec.ports[0].nodePort}" services r4-chartmuseum-chartmuseum)
sudo export NODE_IP=$(kubectl get nodes --namespace ricinfra -o jsonpath="{.items[0].status.addresses[0].address}")
sudo export CHART_REPO_URL=http://$NODE_IP:$NODE_PORT/charts
```

- Build docker image
```bash=
sudo docker build -t mooncake22/slicexapp:0.0.1 .
```

### Step 2: Onboard slicexapp descriptor
```bash=
cd config
dms_cli onboard config-file.json schema.json
```

### Step 3: Deploy slicexapp on the RIC platform
```bash=
dms_cli install slicexapp 0.0.1 ricxapp
```

### Step 4: Create A1 PolicyType Definition
```bash=
curl -v -X PUT "http://<RICPLT_IP>:32080/a1mediator/a1-p/policytypes/22222"   -H "accept: application/json" -H "Content-Type: application/json"   -d @./policytype.json
```

```bash=
curl -v -X GET "http://192.168.8.167:32080/a1mediator/a1-p/policytypes/22222/policies/173a7699-abc7-4575-b56a-65d3b7e58ca9/status"   -H "accept: application/json" -H "Content-Type: application/json"
```

### Step 5: Create A1 Policy
- Create Policy Instance through Non-RT RIC control panel
- Observe the behavior of the slicexapp


### Step 6: Delete A1 PolicyType Definition
```bash=
curl -v -X DELETE "http://<RICPLT_IP>:32080/a1mediator/a1-p/policytypes/22222"   -H "accept: application/json" -H "Content-Type: application/json"
```

### Step 7: Undeploy slicexapp on the RIC platform
```bash=
dms_cli uninstall slicexapp ricxapp
```