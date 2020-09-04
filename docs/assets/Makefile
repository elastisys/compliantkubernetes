compliance-basics.svg: \
		compliance-basics.dot \
		logos/cert-manager.png \
		logos/dex.png \
		logos/elasticsearch.png \
		logos/falco.png \
		logos/harbor.png \
		logos/letsencrypt.png \
		logos/kubernetes.png \
		logos/project-calico.png \
		logos/prometheus.png \
		logos/trivy.png \
		logos/velero.png
	dot -Tsvg $< > $@

logos/%.png:
	mkdir -p logos
	( \
		curl --fail https://branding.cncf.io/img/projects/$*/stacked/color/$*-stacked-color.svg || \
		curl --fail https://landscape.cncf.io/logos/$*.svg \
	) | rsvg-convert -w 100 > $@

logos/elasticsearch.png:
	curl https://static-www.elastic.co/v3/assets/bltefdd0b53724fa2ce/blt5ebe80fb665aef6b/5ea8c8f26b62d4563b6ecec2/brand-elasticsearch-220x130.svg | rsvg-convert -w 200 > $@

logos/letsencrypt.png:
		curl https://letsencrypt.org/images/le-logo-standard.svg | rsvg-convert -w 100 > $@
