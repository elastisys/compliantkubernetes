from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.auth import Oauth2Proxy
from diagrams.onprem.identity import Dex
from diagrams.onprem.tracing import Jaeger
from diagrams.k8s.network import SVC
from diagrams.custom import Custom
from diagrams.onprem.aggregator import Fluentd


with Diagram(name="Option-4: Expose Jaeger UI and audit access via request logging in Oath2Proxy", show=False,direction="LR",filename="adr-0029-option4"):
    user = User("Jaeger user")
    dex = Dex("Dex")

    with Cluster("ck8s workload cluster"):
       svc = SVC("jaeger-query")
       jaeger_ui = [Custom("", "./adr-0029-Jaeger-UI.png")]
       svc >> Edge(label="5. Jaeger UI",color="darkgreen") >> jaeger_ui

       logging = Fluentd("logging")

       with Cluster("Authorization workflows"):
         ingress = Nginx("Ingress Controller")
         oauth2Proxy = Oauth2Proxy("Oauth2Proxy")
         ingress >> Edge(label="2. Authentication request",color="darkorange",fontsize="12") >> oauth2Proxy
         oauth2Proxy >> Edge(label="Authenticated via OAuth2Proxy",color="darkorange",style="dashed",fontsize="12") >> ingress
         oauth2Proxy >> Edge(label="3. Dex Authentication",color="darkorange",fontsize="12") >> dex
         dex >> Edge(label="",color="darkorange",style="dashed",fontsize="12") >> oauth2Proxy


       ingress >> Edge(label="4. Allowed request",color="darkorange",fontsize="12") >> svc
       user >> Edge(label="1. https://jaeger.abc-ck8s.com",color="darkgreen",fontsize="12") >> ingress

       oauth2Proxy >> Edge(label="Request logging enabled in OAuth2",color="darkorange",style="dashed",fontsize="12") >> logging
