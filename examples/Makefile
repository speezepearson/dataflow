all:
	make $$(for f in *.yaml; do BASE=$${f%.yaml}; echo $$BASE.html $$BASE.pdf $$BASE.png; done)

clean:
	rm -f *.html *.json *.dot *.png *.pdf

%.html: %.json ../__main__.py ../__init__.py
	cat $< | python -m dataflow -t cytoscape | cytoscape > $@

%.dot: %.json ../__main__.py ../__init__.py
	cat $< | python -m dataflow -t graphviz > $@

%.json: %.yaml
	cat $< | python -c 'import json, sys, yaml; print(json.dumps(yaml.load(sys.stdin)))' >$@

%.pdf: %.dot
	dot -Tpdf < $< > $@

%.png: %.dot
	dot -Tpng < $< > $@
