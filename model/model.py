import copy

from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.bestSol = []
        self.bestPeso = -1

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

    def trovaCammino(self,N):
        parziale = []
        self.ricorsione(parziale,N)
        return self.bestSol, self.bestPeso

    def ricorsione(self, parziale, N):
        if len(parziale) == N and self.isChiuso(parziale):
            if self.getPeso(parziale) > self.bestPeso:
                self.bestPeso = self.getPeso(parziale)
                self.bestSol = copy.deepcopy(parziale)
            return

        for a in self.grafo.edges(data = True):
            if self.isCorrect(a, parziale):
                parziale.append(a)
                self.ricorsione(parziale,N)
                parziale.pop()

    def isChiuso(self, parziale):
        # Verifica se il percorso parziale è chiuso
        # Controlla che il primo nodo sia uguale all'ultimo nodo
        if len(parziale) < 2:
            return False  # Un ciclo chiuso richiede almeno 2 archi
        ret1 = parziale[0][0]  # Nodo iniziale del percorso
        ret2 = parziale[-1][1]  # Nodo finale del percorso
        return ret1 == ret2

    """def isCorrect(self, a, parziale):
        if len(parziale) == 0:
            return True
        if len (parziale) >= 1:
            if parziale[-1][1] == a[0]:
                for e in parziale:
                    if a[1] == e[1]:
                        return False
                return True
            else:
                return False"""

    def isCorrect(self, a, parziale):
        if not parziale:
            return True  # Se non ci sono archi, qualsiasi arco è valido come inizio

        # Nodo finale dell'ultimo arco del percorso parziale
        ultimo_nodo = parziale[-1][1]

        # Verifica che il nuovo arco inizi dal nodo finale del percorso
        if ultimo_nodo == a[0]:
            # Ottieni il nodo di partenza per il controllo finale
            nodo_iniziale = parziale[0][0]

            # Controlla se il nodo finale è già stato visitato, evitando cicli interni
            visited_nodes = {edge[0] for edge in parziale} | {edge[1] for edge in parziale}

            # Permette di tornare al nodo di partenza alla fine, ma vieta altri nodi già visitati
            if a[1] in visited_nodes and a[1] != nodo_iniziale:
                return False

            return True  # L'arco è valido se rispetta queste condizioni

        return False  # Rifiuta l'arco se non parte dal nodo finale dell'ultimo arco

    def getPeso(self, parziale):
        peso = 0
        for e in parziale:
            peso += e[2]['weight']
        print(peso)
        return peso

