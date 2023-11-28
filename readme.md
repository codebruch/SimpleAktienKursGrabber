[alex@nuc2 app]$  source ./bin/activate

(app) [alex@nuc2 app]$  python3 -m pip install selenium

 sudo docker build --pull --rm -f "Dockerfile" -t grabber:latest "."
 
 [root@nuc2 serverstatic]# PIMAGE=$(docker images --filter="reference=grabber:latest" --quiet)
docker tag $PIMAGE  registry.registry.lan/grabber:release
docker push  registry.registry.lan/grabber:release


  kubectl apply -f Deployment.yaml
 
