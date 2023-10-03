from diagrams import Diagram, Cluster, Edge, Node
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.auth import Oauth2Proxy
from diagrams.onprem.identity import Dex
from diagrams.onprem.tracing import Jaeger
from diagrams.k8s.network import SVC
from diagrams.custom import Custom

with Diagram(
        name="Option-3:  Expose Jaeger UI, but completely behind oauth2-proxy. Use config domain, groups, IP allowlisting and request logging for protecting it",
        filename="adr-0029-option3.png",
        show=False):
    user = User("Jaeger user")
    dex = Dex("Dex")


    with Cluster("ck8s workload cluster"):
       custom = [Custom("", "./0029-Jaeger-UI.png")]
       labels = ("IP allowlist managed at Ingress")
       custom2 = Node(labels,
            style="note", width="3", labelloc="t")
       custom3 = [Custom("", "./0029-note2.png")]
       svc = SVC("jaeger-query")

       svc >> Edge(label="5. Jaeger UI",color="black",fontsize="12") >> custom


       with Cluster("Authorization workflows"):
         ingress = Nginx("Ingress Controller")
         oauth2Proxy = Oauth2Proxy("Oauth2Proxy")
         ingress >> Edge(label="2. Authentication request",color="darkorange",note="abc",fontsize="12") >> oauth2Proxy
         oauth2Proxy >> Edge(label="Authenticated via OAuth2Proxy",color="darkorange",style="dashed",fontsize="12") >> ingress
         oauth2Proxy >> Edge(label="3. Dex Authentication",color="darkorange",fontsize="12") >> dex
         dex >> Edge(label="",color="darkorange",style="dashed",fontsize="12") >> oauth2Proxy
         oauth2Proxy >> Edge(label="4. Upstream jaeger internal service",color="darkorange",fontsize="12") >> svc

         oauth2Proxy >> Edge(label="",style="dashed") >> custom3
         user >> Edge(label="1. https://jaeger.abc-ck8s.com",color="darkgreen",fontsize="12") >> ingress
         ingress >> Edge(label="",style="dashed") >> custom2
