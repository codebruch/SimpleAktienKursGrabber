docker build --pull --rm -f "Dockerfile" -t grabber:latest "."
PIMAGE=$(docker images --filter="reference=grabber:latest" --quiet)
docker tag $PIMAGE registry.registry.lan/grabber:release
docker push registry.registry.lan/grabber:release
#kubectl rollout restart -n default deployment grabber
