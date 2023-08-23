---
description: Documentation for Elastisys Compliant Kubernetes, the security-focused Kubernetes distribution.
hide:
  - navigation
  - toc
---

# Innovate at speed in regulated industries

Elastisys Compliant Kubernetes enables organizations across Europe to accelerate innovation through open source cloud-native technology, while ensuring security and regulatory compliance.

<nav>
<dl class="columns-3">
  <div>
    <dt>For application developers</dt>
    <dd><a role="button" href="./user-guide/">Learn more</a></dd>
  </div>

  <div>
    <dt>For CISOs and DPOs</dt>
    <dd><a role="button" href="./ciso-guide/">Learn more</a></dd>
  </div>

  <div>
    <dt>For platform administrators</dt>
    <dd><a role="button" href="./operator-manual/">Learn more</a></dd>
  </div>
</ul>
</nav>

## What is Elastisys Compliant Kubernetes?

<embed src="img/marchitecture.drawio.svg" alt="Components of Elastisys Compliant Kubernetes" width="100%"/>

## Benefits of Elastisys Compliant Kubernetes

<dl class="columns-3">
  <div>
    <dt>The platform you would build yourself</dt>
    <dd>
        Built with CNCF projects,
        public <a href="./adr">Architectural Decision Records</a>,
        as well as great documentation for
            <a href="./user-guide/">application developers</a>.
    </dd>
  </div>
  <div>
    <dt>Loved❤️ by CISOs👮 and DPOs🧑‍⚖️ </dt>
    <dd>
        Built around controls to achieve EU regulatory compliance with:
        <a href="./ciso-guide/controls/gdpr/">GDPR</a>,
        <a href="./ciso-guide/controls/iso-27001/">ISO 27001</a>,
        <a href="./ciso-guide/controls/bsi-it-grundschutz/">NIS2 (BSI IT-Grundschutz)</a>.
    </dd>
  </div>
  <div>
    <dt>Cloud agnostic, running in production in 10+ clouds</dt>
    <dd>
        Runs on many EU clouds or <a href="../operator-manual/on-prem-standard/">on-prem</a>.
    </dd>
  </div>
</dl>

## Elastisys Compliant Kubernetes is trusted by industry leaders

<ul id="trusted-by">
    <li><img src="img/logos/orgs/carasent.png" alt="Logo of Carasent" /></li>
    <li><img src="img/logos/orgs/elsa.svg" alt="Logo of Elsa Science" /></li>
    <li><img src="img/logos/orgs/vivium.png" alt="Logo of Vivium" /></li>
    <li><img src="img/logos/orgs/tempus.png" alt="Logo of Tempus" /></li>
    <li><img src="img/logos/orgs/goozo.svg" alt="Logo of Goozo" /></li>
</ul>

<section id="customer-quotes" class="carousel">
    <button id="customer-quotes-prev">&#8249;</button>
    <button id="customer-quotes-next">&#8250;</button>
    <ul>
        <li style="background: red;">1</li>
        <li style="background: blue;">2</li>
        <li>3</li>
        <li>4</li>
    </ul>
</section>
<script type="text/javascript">
const customerQuotes = document.getElementById("customer-quotes").querySelector("ul");
const quotes = customerQuotes.querySelector("li");
const prevButton = document.getElementById("customer-quotes-prev");
const nextButton = document.getElementById("customer-quotes-next");
prevButton.addEventListener("click", () => {
    const slideWidth = quotes.clientWidth;
    customerQuotes.scrollLeft -= slideWidth;
});
nextButton.addEventListener("click", () => {
    const slideWidth = quotes.clientWidth;
    customerQuotes.scrollLeft += slideWidth;
});
setInterval(() => {
    const slideWidth = quotes.clientWidth;
    if (! customerQuotes.matches(':hover')) {
        console.log('mouse is not over the element, scrolling')
        var value = (customerQuotes.scrollLeft + slideWidth) % (customerQuotes.children.length * slideWidth);
        customerQuotes.scrollLeft = value;
    }
}, 2000);
</script>

<ul class="cncf-links">
    <li>
        <img src="logos/cncf-silver-member.png">
        <br>
        Maintained by Elastisys, proud CNCF silver member
    </li>
    <li>
        <img src="logos/cncf-certified-kubernetes.png">
        <br>
        Our platform is a CNCF Certified Kubernetes Distribution
    </li>
</ul>


## Commercial offering

<div class="wrapper">
    <div class="box">
        <h3>Managed Services</h3>
        <p>A full Kubernetes platform, with logging, monitoring, and more. PostgreSQL, RabbitMQ, and Redis on top. All secure and fully managed by us.</p>
        <button>Learn more</button>
    </div>
    <div class="box">
        <h3>Consulting</h3>
        <p>Extend your team with our cloud native experts. Develop and deploy apps faster and with more confidence in a DevSecOps fashion.</p>
        <button>Learn more</button>
    </div>
    <div class="box">
        <h3>Training</h3>
        <p>Level up your team's skills with our wide range of courses, both tailor-made and official Kubernetes ones from the Linux Foundation.</p>
        <button>Learn more</button>
    </div>
    <div class="box">
        <h3>Support</h3>
        <p>Leverage Elastisys Compliant Kubernetes on-prem with implementation and continuous support.</p>
        <button>Learn more</button>
    </div>
</div>
