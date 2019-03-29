A Flask app using for the football-data.org API.

The variable football matches hold a JSON-formatted response to our GET request.

we are using it to find out the statistics of matches  and shows the home team and wins or not.

1.Set the application for the new cluster
```
gcloud config set compute/zone europe-west2-b
export PROJECT_ID="$(gcloud config get-value project -q)"
```

2.create a Kubernetes cluster
```
gcloud container clusters create cassandra --num-nodes=3 --machine-type "n1-standard-2"
```

3.A Kubernetes service defines multiple sets of pods, allowing full systems to be deployed with one script.For this we will be using three files. 
```
wget -O cassandra-peer-service.yml http://tinyurl.com/yyxnephy
wget -O cassandra-service.yml http://tinyurl.com/y65czz8e
wget -O cassandra-replication-controller.yml http://tinyurl.com/y2crfsl8
```

4.now run our three components
```
kubectl create -f cassandra-peer-service.yml
kubectl create -f cassandra-service.yml
kubectl create -f cassandra-replication-controller.yml
```

5.Check that the single container is running correctly
```
kubectl get pods -l name=cassandra
```

6.and if so we can can scale up our number of nodes via our replication-controller:
```
kubectl scale rc cassandra --replicas=3
```

7.run cqlsh inside the container
```
kubectl exec -it <service name> cqlsh
```

8.build our keyspace
```
CREATE KEYSPACE crime WITH REPLICATION ={'home_team' : 'away_team', 'result' : 2};
```

9.Create the table for our service
```
CREATE TABLE ftball.stats(home_team,away_team,home_goals,away_goals,result,season)
```

10. then create our requirements.txt
```
pip
Flask
cassandra−driver
```

11.the Dockerfile
```
FROM python:3.7-alpine
WORKDIR /myapp
COPY . /myapp
RUN pip install -U -r requirements.txt
EXPOSE 8080
CMD ["python", "appx.py"]
```

12. build our image
```
docker build -t gcr.io/${PROJECT_ID}/ftball:v1 .
```

13.Push it to the Google Repository
```
docker push gcr.io/${PROJECT_ID}/ftball:v1
```

14.Run it as a service
```
kubectl run ftball-app --image=gcr.io/${PROJECT_ID}/ftball-app:v1 --port 8080
```

15.exposing the deploment to get an external IP
```
kubectl expose deployment ftball-app --type=LoadBalancer --port 80 --target-port 8080
```

16.get the external IP
```
kubectl get services
```

17.use the IP to visit the first web
```
[CURRENT_IP]/ftball/<TEAM NAME>
```

```
