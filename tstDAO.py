from database.DAO import DAO
listaRetailer = DAO.getRetailersComuni(2015, "Mexico")
for r in listaRetailer:
    print(r[0])