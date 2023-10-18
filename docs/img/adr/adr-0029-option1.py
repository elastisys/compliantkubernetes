from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.auth import Oauth2Proxy
from diagrams.onprem.identity import Dex
from diagrams.onprem.tracing import Jaeger
from diagrams.k8s.network import SVC
from diagrams.custom import Custom


with Diagram(name="Option-1: Expose Jaeger UI via ingress in wc cluster and use Oauth2-proxy for request authentication", show=False,direction="LR",filename="adr-0029-option1"):
    user = User("Jaeger user")
    dex = Dex("Dex")

    with Cluster("ck8s workload cluster"):
       svc = SVC("jaeger-query")
       jaeger_ui = [Custom("", "./adr-0029-Jaeger-UI.png")]
       svc >> Edge(label="5. Jaeger UI",color="darkgreen") >> jaeger_ui

       with Cluster("Authorization workflows"):
         ingress = Nginx("Ingress Controller")
         oauth2Proxy = Oauth2Proxy("Oauth2Proxy")
         ingress >> Edge(label="2. Authentication request",color="darkorange") >> oauth2Proxy
         oauth2Proxy >> Edge(label="Authenticated via OAuth2Proxy",color="darkorange",style="dashed") >> ingress
         oauth2Proxy >> Edge(label="",color="darkorange") >> dex
         dex >> Edge(label="3. Dex Authentication",color="darkorange",style="dashed") >> oauth2Proxy


       ingress >> Edge(label="4. Allowed request",color="darkorange") >> svc
       user >> Edge(label="1. https://jaeger.abc-ck8s.com",color="darkgreen") >> ingress
