from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self.grafo = nx.Graph()

    def getYears(self):
        return DAO.getYear()

    def getCountries(self):
        return DAO.getCountry()

    def creaGrafo(self, anno, nazione):
        self.grafo.clear()
        listaRetailer = DAO.getRetailers(nazione)
        self.grafo.add_nodes_from(listaRetailer)
        self.retailerMap = {}
        for r in listaRetailer:
            self.retailerMap[r.Retailer_code] = r
        listaRetailerComuni = DAO.getRetailersComuni(anno, nazione)
        for r in listaRetailerComuni:
            ret1 = self.retailerMap[r[0]]
            ret2 = self.retailerMap[r[1]]
            peso = r[2]
            self.grafo.add_edge(ret1, ret2, weight=peso)

    def getNumNodes(self):
        return len(self.grafo.nodes())

    def getNumEdges(self):
        return len(self.grafo.edges())

    def trovaVolume(self):
        nodi = self.grafo.nodes()
        dictVol = {}
        for n in nodi:
            volume = 0
            archiInc = self.grafo.edges(n, data=True)
            for u, v, data in archiInc:
                volume += data['weight']
            if volume > 0:
                dictVol[n] = volume
        dictVol_ordinato = dict(sorted(dictVol.items(), key=lambda item: item[1], reverse=True))
        print(dictVol_ordinato)
        return dictVol_ordinato