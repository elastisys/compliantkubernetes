---
description: Documentation for Elastisys Compliant Kubernetes, the security-focused Kubernetes distribution.
hide:
  - navigation
  - toc
---

# Elastisys Compliant Kubernetes

<p class="hero-text">
<strong>Innovate at speed in regulated industries</strong>
</p>
<p class="hero-text">
Elastisys Compliant Kubernetes enables organizations across Europe to accelerate innovation through open source cloud-native technology, while ensuring security and regulatory compliance.
</p>

## What is Elastisys Compliant Kubernetes?

<embed src="img/marchitecture.drawio.svg" alt="Components of Elastisys Compliant Kubernetes" width="100%"/>

## Benefits of Elastisys Compliant Kubernetes

<dl id="benefits">
    <dt>Kubernetes Platform</dt>
    <dd>Built with CNCF projects, public Architectural Decision Records (ADRs), and great application for application developers.</dd>
    <dt>GDPR, ISO-27001, NIS2</dt>
    <dd>Built to enable companies to achieve EU regulator compliance.</dd>
    <dt>Cloud agnostic, running in production in 10+ clouds</dt>
    <dd>Managed service available on supported EU clouds, or with enterprise-level support on any cloud or on-premise installation.</dd>
</dl>

## Elastisys Compliant Kubernetes is trusted by industry leaders

<ul id="trusted-by">
    <li><img src="organizations/carasent.png" alt="Logo of Carasent" /></li>
    <li><img src="organizations/elsa-science.png" alt="Logo of Elsa Science" /></li>
    <li><img src="organizations/vivium.png" alt="Logo of Vivium" /></li>
    <li><img src="organizations/tempus.png" alt="Logo of Tempus" /></li>
    <li><img src="organizations/goozo.png" alt="Logo of Goozo" /></li>
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

## How do I get started?

![The Journey for Application Developers](img/getting-started-developers.png)

Getting started guides:

* [for Application Developers](user-guide/prepare.md)
* [for Platform Administrators](operator-manual/index.md)
* [for CISOs (Chief Information Security Officers)](ciso-guide/index.md)

## Would you like to contribute?

We want to build the next generation of cloud native technology where data security and privacy is the default setting.

Join us on our mission as a contributor? Go to the [guide for contributors](contributor-guide/index.md).
