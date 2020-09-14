all: \
		compliance-basics.png \
		ck8s-c4model-level1.png \
		ck8s-c4model-level2.png

preview:
		echo "Performing continuous preview ..." >&2
		while true; do \
				make all; \
				inotifywait -e close_write . ; \
		done

%.svg: %.dot
	dot -Tsvg $< > $@

%.png: %.dot
	dot -Tpng $< > $@

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
