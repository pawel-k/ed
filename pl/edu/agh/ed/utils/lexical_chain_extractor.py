# coding=utf-8
import codecs
import re
from sets import Set
from edu.agh.ed.utils.connector import CollocationsRetriever

def read_stoplist(file_name):
    with codecs.open(file_name,'r') as file:
        data = file.read()
        return Set(data.split("\n"))

def extract_chain_parts(input_text,stoplist):
    words = re.findall("\w+",input_text.lower(),re.UNICODE)
    return Set([word for word in words if word not in stoplist])

def get_collocations(retriever,words):
    search_string = "** ".join(words);
    search_string+="**"
    results = retriever.retrieve(search_string)
    return {lemma:chi2 for (lemma, chi2, _forms) in results}


def remove_duplicates(new_chains):
    #TODO remove duplicates from list
    return new_chains


def get_lexical_chains(chain_parts, retriever):
    current_chains = [[word] for word in chain_parts]
    finalized_chains = []
    for i in range(0,len(chain_parts)):
        new_chains = []
        for chain in current_chains:
            collocations = get_collocations(retriever,chain)
            collocations_lemma = collocations.keys()
            matched_collocations = [collocation for collocation in collocations_lemma if collocation in chain_parts and collocation not in Set(chain)]
            if len(matched_collocations)>0:
                for collocation in matched_collocations:
                    chain_copy=chain[:]
                    chain_copy.append(collocation)
                    new_chains.append(chain_copy)
            elif len(chain)>1:
                finalized_chains.append(chain)
        current_chains=remove_duplicates(new_chains)
    finalized_chains.extend(current_chains)
    return finalized_chains


def main():
    input_text = "auto fiat osobowy terenowy"
    print input_text
    stoplist = read_stoplist("pl.txt")
    chain_parts = extract_chain_parts(input_text,stoplist)
    retriever = CollocationsRetriever()
    lexical_chains = get_lexical_chains(chain_parts,retriever)
    for chain in lexical_chains:
        print chain

main()