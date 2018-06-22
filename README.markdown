Examples:

- To PDF: `cat examples/rabbitmq.dataflow.yaml | yaml2json | python -m dataflow -t graphviz | dot -Tpdf > temp.pdf && open temp.pdf`
- To HTML: `cat examples/rabbitmq.dataflow.yaml | yaml2json | python -m dataflow -t cytoscape | cytoscape > temp.html && open temp.pdf`

For constant refreshing: `fswatch --event Updated *.py WHATEVER.yaml | incessantly -- bash -c 'cat WHATEVER.yaml | yaml2json | python -m dataflow -t graphviz | dot -Tpdf > temp.pdf'`
