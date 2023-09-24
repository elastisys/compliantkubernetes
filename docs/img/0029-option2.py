from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.onprem.tracing import Jaeger
from diagrams.k8s.network import SVC
from diagrams.custom import Custom
from diagrams.k8s.controlplane import API

with Diagram(name="Option-2: Do not expose Jaeger UI", show=False):
    user = User("Jaeger user")

    with Cluster("ck8s workload cluster"):
       custom = [Custom("Jaeger UI", "./0029-Jaeger-UI.png")]
       api = API("API server")
       svc = SVC("jaeger-query")
       user >> Edge(label="1. kubectl port-forward service/jaeger-operator-jaeger-query",color="darkgreen",fontsize="15") >> api
       api >> Edge(label="2. API server creates a tunnel to service",color="darkgreen",fontsize="15") >> svc
       svc >> Edge(label="3. http://localhost:16686",color="black",fontsize="15") >> custom
