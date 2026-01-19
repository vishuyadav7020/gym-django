Deployment test /n
second
\\
\\
docker run command for without cloudflare tunnel and mongodb running in conatiner :- docker run -d --name \\django_app_test -p 8001:8000 --env-file .env.local vishu7020/gym-django:local\\

change the direcoty of env to for server :- /var/www/gym-django/.env\\
change the direcoty of env to for local :- remain same \\


\\\
Stackfit.in running succesfully\\
cloudflare tunnel id in settings
docker down\\
docker pull\\
docker up -d\\
 mongodb ruuning on conatiner mongo 7 \\
 command to access mongosh :- docker exec -it mongo_db mongosh\\


\
kubernaties secret file command create on .env.kuber file\
If later you:\

Change .env.kuber\

Add new variables\

You must re-create the secret (Kubernetes does NOT auto-update secrets):\

kubectl delete secret web-env -n testing
kubectl create secret generic web-env \
  --from-env-file=/var/www/gym-django/.env.kuber \
  -n testing
kubectl rollout restart deployment web -n testing
