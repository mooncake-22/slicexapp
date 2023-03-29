## 
```bash=
cd src/protobuf
python3 -m grpc_tools.protoc -I=. --python_out=. --pyi_out=. --grpc_python_out=. rc.proto
```

```bash=
curl -v -X DELETE "http://192.168.8.167:32080/a1mediator/a1-p/policytypes/22222"   -H "accept: application/json" -H "Content-Type: application/json"
curl -v -X PUT "http://192.168.8.167:32080/a1mediator/a1-p/policytypes/22222"   -H "accept: application/json" -H "Content-Type: application/json"   -d @./policytype.json
curl -v -X GET "http://192.168.8.167:32080/a1mediator/a1-p/policytypes/22222/policies/173a7699-abc7-4575-b56a-65d3b7e58ca9/status"   -H "accept: application/json" -H "Content-Type: application/json"
```

```bash=
cd slice-py/
sudo docker build -t mooncake22/slicexapp:0.0.1 .
```


```bash=
 export NODE_PORT=$(kubectl get --namespace ricinfra -o jsonpath="{.spec.ports[0].nodePort}" services r4-chartmuseum-chartmuseum)
 export NODE_IP=$(kubectl get nodes --namespace ricinfra -o jsonpath="{.items[0].status.addresses[0].address}")
 export CHART_REPO_URL=http://$NODE_IP:$NODE_PORT/charts
 ```