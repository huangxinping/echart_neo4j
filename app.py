from flask import Flask, jsonify, render_template
from py2neo import Graph
import random

app = Flask(__name__)
graph = Graph(host='192.168.0.210', port=7687, verify=False)


def buildNodes(nodeRecord):
    return {
        "category": random.randint(0, 4),
        "name": nodeRecord['n']['name'],
        "value": nodeRecord['n'].identity
    }


def buildLinks(relationRecord):
    return {
        "source": relationRecord['r'].start_node.identity,
        "target": relationRecord['r'].end_node.identity
    }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/graph')
def get_graph():
    nodes = list(map(buildNodes, graph.run('MATCH (n) RETURN n')))
    links = list(map(buildLinks, graph.run('MATCH ()-[r]->() RETURN r')))
    return jsonify({
        "type": "force",
        "categories": [
            {
                "name": "HTMLElement",
                "keyword": {},
                "base": "HTMLElement"
            },
            {
                "name": "WebGL",
                "keyword": {},
                "base": "WebGLRenderingContext"
            },
            {
                "name": "SVG",
                "keyword": {},
                "base": "SVGElement"
            },
            {
                "name": "CSS",
                "keyword": {},
                "base": "CSSRule"
            },
            {
                "name": "Other",
                "keyword": {}
            }
        ],
        "nodes": nodes,
        "links": links
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
