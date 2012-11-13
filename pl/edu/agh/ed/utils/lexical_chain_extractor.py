# coding=utf-8
import codecs
import re
from edu.agh.ed.utils.connector import CollocationsRetriever

def read_stoplist(file_name):
    with codecs.open(file_name,'r','utf-8') as file:
        data = file.read()
        return set(data.split("\n"))

def extract_chain_parts(input_text,stoplist):
    words = re.findall("\w+",input_text.decode('utf-8').lower(),re.UNICODE)
    return [word.encode('utf-8') for word in words if word not in stoplist]

def get_collocations(retriever,words):
    search_string = "** ".join(words)
    search_string+="**"
    results = retriever.retrieve(search_string)
    return {lemma:chi2 for (lemma, chi2, _forms) in results}


def remove_duplicates(new_chains):
    unique_chains = []
    for i in range(0,len(new_chains)):
        match = False
        for j in range(i+1,len(new_chains)):
            if len(set(new_chains[i]) - set(new_chains[j]))==0:
                match = True
                break
        if match is False:
            unique_chains.append(new_chains[i])
    return unique_chains


def remove_overlapping(finalized_chains):
    non_overlapping_chains = []
    length_sorted_chains = sorted(finalized_chains)
    for chain in length_sorted_chains:
        match = False
        for i in range(length_sorted_chains.index(chain)+1,len(length_sorted_chains)):
            if len(set(chain) - set(length_sorted_chains[i])) == 0:
                match = True
                break
        if match is False:
            non_overlapping_chains.append(chain)
    return non_overlapping_chains


def get_lexical_chains(chain_parts, retriever):
    current_chains = [[word] for word in chain_parts]
    finalized_chains = []
    for i in range(0,len(chain_parts)):
        new_chains = []
        for chain in current_chains:
            collocations = get_collocations(retriever,chain)
            collocations_lemma = collocations.keys()
            matched_collocations = [collocation for collocation in collocations_lemma if collocation in chain_parts and collocation not in set(chain)]
            if len(matched_collocations)>0:
                for collocation in matched_collocations:
                    chain_copy=chain[:]
                    chain_copy.append(collocation.encode('utf-8'))
                    new_chains.append(chain_copy)
            elif len(chain)>1:
                finalized_chains.append(chain)
        current_chains=remove_duplicates(new_chains)
    finalized_chains.extend(current_chains)
    non_overlapping_chains = remove_overlapping(finalized_chains)
    return non_overlapping_chains


def main():
    input_text = "auto fiat osobowy terenowy samolot lądować lotnisko"
    #input_text = "samolot lądować lotnisko"
    print input_text
    stoplist = read_stoplist("pl.txt")
    chain_parts = extract_chain_parts(input_text,stoplist)
    retriever = CollocationsRetriever()
    lexical_chains = get_lexical_chains(chain_parts,retriever)
    for chain in lexical_chains:
        print "found chain -> "+" ".join(chain)

main()