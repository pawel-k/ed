# -*- coding: utf-8 -*-
import collections
from gensim import corpora
from gensim.models import ldamodel
from pl.edu.agh.ed.Graph import Graph
from pl.edu.agh.ed.community import best_partition
import networkx as nx
import logging
import codecs
import re
import pydot


def read_input(filename,stop_list,forms_dictionary):
    with codecs.open(filename, "r","utf-8") as file:
        data = file.read().lower()
        return normalize_document(data,stop_list,forms_dictionary)


def read_stop():
    with codecs.open("stop.txt", "r") as f:
        return set([word.strip() for word in f.read().decode('utf-8').split(',')])


def read_dictionary():
    dictionary = {}
    with codecs.open("odm.txt", "r","utf-8") as f:
        data = f.read()
        for line in data.split('\n'):
            words = line.split(',')
            for word in words:
                dictionary[word.strip()] = words[0].strip()
    return dictionary


def read_documents(dictionary, stop_list):
    documents = []
    with codecs.open("papsmall.txt", "r","utf-8") as f:
        data = f.read().lower()
        for document in re.split("#\d+", data):
            documents.append(normalize_document(document,stop_list,dictionary))
    return documents


def normalize_document(document,stop_list,dictionary):
    normalized_document=[]
    for word in re.findall('\w+', document.lower(), re.UNICODE):
        if word not in stop_list and word != '':
            try:
                normalized_document.append(dictionary[word])
            except KeyError:
                normalized_document.append(word)
                dictionary[word] = word
    return normalized_document

def draw_text_graph(graph, filename):
    printable_graph = pydot.Dot(graph_type='graph')
    for node in graph.get_nodes():
        printable_node = pydot.Node(node.get_word(), style="filled", fillcolor=node.get_color(),fontsize=node.size()*10)
        printable_graph.add_node(printable_node)
        for neighbour_node in node.get_neighbours():
            printable_graph.add_edge(pydot.Edge(printable_node,neighbour_node.get_word()))
    printable_graph.write_png('%s.png' % filename)

def color_graph(graph,colors):
    G=nx.Graph()
    for node in graph.get_nodes():
        G.add_node(node.get_word())
    for node in graph.get_nodes():
        for neighbour_node in node.get_neighbours():
            G.add_edge(node.get_word(),neighbour_node.get_word())
    groups = best_partition(G)
    for node in graph.get_nodes():
        node.set_color(colors[groups[node.get_word()]])

def create_text_graph(words_list,colors):
    graph = Graph()
    for i in range(len(words_list)):
        node = graph.get_node(words_list[i])
        for next_node_word in words_list[i+1:i+3]: #2 nodes ahead
            next_node = graph.get_node(next_node_word)
            node.connect_to(next_node)
    color_graph(graph,colors)
    return graph

def print_topics(model, dictionary, graph):
    for color,nodes_list in graph.get_colored_nodes().iteritems():
        text = [node.get_word() for node in nodes_list]
        topics_distribution = model[dictionary.doc2bow(text)]
        print color
        for topic_number,probability in topics_distribution:
            if probability>1e-1:
                print topic_number,probability


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
    stop_list = read_stop()
    forms_dictionary = read_dictionary()
    documents = read_documents(forms_dictionary, stop_list)[1:]
    all_tokens = sum([document_words for document_words in documents], [])
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in document_words if word not in tokens_once] for document_words in documents]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    model = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=10)
    colors = ["red", "green", "blue", "yellow", "pink", "orange", "purple", "white", "violet", "brown", "grey","red", "green", "blue", "yellow", "pink", "orange", "purple", "white", "violet", "brown", "grey"]
    normalized_document = read_input("marsz.txt",stop_list,forms_dictionary)
    graph = create_text_graph(normalized_document,colors)
    #draw_text_graph(graph, "test")
    print_topics(model,dictionary,graph)

if __name__ == '__main__':
    main()
