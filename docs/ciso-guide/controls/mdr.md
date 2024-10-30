# MDR (Regulation (EU) 2017/745)

{%
   include-markdown './_common.include'
   start='<!--legal-disclaimer-start-->'
   end='<!--legal-disclaimer-end-->'
%}

!!!note

    CE certification of a medical device according to the EU MDR can lead a huge commercial benefit, but it is a significant project.
    To start the certification process thorough knowledge of the regulation is required.

    This page only points you to the MDR concerns relevant for Welkin.

If you place or make a medical device available, or put them into service, on the European market, then you must comply with the Medical Device Regulation (MDR).

As of 2023, there is at least one Medical Device Software running on Welkin that is CE certified according to MDR class IIa.

## Article 110: Data protection

This article makes explicit reference to GDPR. See [GDPR controls](gdpr.md).

## Annex I: General Safety and Performance Requirements

This annex makes reference to information security, for example in 17.2.
You might want to check [ISO 27001](iso-27001.md) controls, since that is one of the most recognized information security standards.

## Annex VI: UDI-related

This annex makes explicit reference to change management, for example in 6.5.2 and 6.5.3.

See [how many environments](../../user-guide/how-many-environments.md) to reduce the risk associated with updating the Welkin environments hosting your software medical device.
While rather unlikely, you really want to make sure that your software medical device preserves its original performance with the new version of Kubernetes.

[TAGS]

## Further reading

- [Regulation (EU) 2017/745 on Medical Devices](https://eur-lex.europa.eu/eli/reg/2017/745/2023-03-20)
- [Medicintekniska produkter on IVO](https://www.ivo.se/vard-omsorgsgivare/anmal-handelse-lamna-underrattelse/medicintekniska-produkter/)
