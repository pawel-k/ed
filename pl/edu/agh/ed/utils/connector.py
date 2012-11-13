# coding=utf-8
import urllib
from xml.dom import minidom

class CollocationsRetriever(object):
    def __init__(self):
        self.servlet = "http://nkjp.uni.lodz.pl/CollocationsInXML"
        self.offset = 0
        self.limit = 10000
        self.span = 4
        self.collocationalContextLeft = 1
        self.collocationalContextRight = 1
        self.minCoocFreq = 5
        self.posOfCollocate = "any"
        self.sort = "srodek"
        self.preserve_order = "true"
        self.dummystring = "ąĄćĆęĘłŁńŃóÓśŚźŹżŻ"
        self.sid = 0.508211354685388
        self.m_date_from = "RRRR"
        self.m_date_to = "RRRR"
        self.m_nkjpSubcorpus = "balanced"
        self.m_style = "---"
        self.m_channel = "---"
        self.m_styles = ", ---"
        self.m_channels = ", ---"

    def __query_for_collocations(self, query):
        params = urllib.urlencode(
            {'query': query, 'offset': self.offset, 'span': self.span, 'sort': self.sort, 'second_sort': 'srodek',
             'limit': self.limit,
             'preserve_order': self.preserve_order, 'dummystring': self.dummystring,
             'sid': self.sid, 'm_date_from': self.m_date_from, 'm_date_to': self.m_date_to, 'm_styles': self.m_styles,
             'm_channels': self.m_channels,
             "m_nkjpSubcorpus": self.m_nkjpSubcorpus, "collocationalContextLeft": self.collocationalContextLeft,
             "collocationalContextRight": self.collocationalContextRight,
             "minCoocFreq": self.minCoocFreq, "posOfCollocate": self.posOfCollocate, "m_style": self.m_style,
             "m_channel": self.m_channel,
             "m_styles": self.m_styles, "m_channels": self.m_channels})
        f = urllib.urlopen(self.servlet, params)
        return f.read()

    def __get_value(self, node):
        return node.childNodes[0].data

    def __get_by_name(self, node, name):
        return node.getElementsByTagName(name)[0]

    def retrieve(self, query):
        data = self.__query_for_collocations(query)
        document = minidom.parseString(data)
        nodes = document.childNodes
        value = self.__get_value
        node = self.__get_by_name
        results = []
        for collocation in nodes[0].getElementsByTagName("collocation"):
            lemma = value(node(collocation, "lemma"))
            chi2 = value(node(collocation, "chi2"))
            forms = collocation.getElementsByTagName("forms")
            results.append((lemma, chi2, [(value(node(form, "f")), int(form.getAttribute("freq"))) for form in
                              forms[0].getElementsByTagName("form")]))
        return results

def main():
    retriever = CollocationsRetriever()
    results = retriever.retrieve("pociąg**")
    for (lemma, chi2, forms) in results:
        print "lemma: ", lemma, ", chi2: ", chi2
        for (form, freq) in forms:
            print "\tform= '" + form + "', frequency=", freq

if __name__ == "__main__":
    main()

