from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.onprem.tracing import Jaeger
from diagrams.k8s.network import SVC
from diagrams.custom import Custom
from diagrams.k8s.controlplane import API

with Diagram(name="Option-2: Do not expose Jaeger UI", show=False,filename="adr-0029-option2"):
    user = User("Jaeger user")

    with Cluster("ck8s workload cluster"):
       jaeger_ui = [Custom("Jaeger UI", "./adr-0029-Jaeger-UI.png")]
       kube_api = API("API server")
       svc = SVC("jaeger-query")
       user >> Edge(label="1. kubectl port-forward service/jaeger-operator-jaeger-query",color="darkgreen",fontsize="15") >> kube_api
       kube_api >> Edge(label="2. API server creates a tunnel to service",color="darkgreen",fontsize="15") >> svc
       svc >> Edge(label="3. http://localhost:16686",color="black",fontsize="15") >> jaeger_ui
