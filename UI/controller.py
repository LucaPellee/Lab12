import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        listaAnni = self._model.getYears()
        for a in listaAnni:
            self._view.ddyear.options.append(ft.dropdown.Option(a))

        listaCountry = self._model.getCountries()
        for c in listaCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))
        self._view.update_page()


    def handle_graph(self, e):
        anno = self._view.ddyear.value
        country = self._view.ddcountry.value
        self._model.creaGrafo(anno, country)
        nNodes = self._model.getNumNodes()
        nEdges = self._model.getNumEdges()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero  di vertici: {nNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nEdges}"))
        self._view.update_page()



    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()
        dictVol = self._model.trovaVolume()
        for k, v in dictVol.items():  # k è la chiave, v è il valore
            self._view.txtOut2.controls.append(ft.Text(f"{k} -- {v}"))
        self._view.update_page()



    def handle_path(self, e):
        self._valoreNum = self._view.txtN.value
        try:
            numTratte = int(self._valoreNum)
        except ValueError:
            self._view.create_alert("Inserire valore numerico")
        if numTratte < 2:
            self._view.create_alert("Il valore deve essere almeno 2")
            return
        soluzione, peso = self._model.trovaCammino(numTratte)
        self._view.txtOut3.controls.clear()
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {peso}"))
        for s in soluzione:
            self._view.txtOut3.controls.append(ft.Text(f"{s[0]} --> {s[1]}: {s[2]['weight']}"))
        self._view.update_page()
