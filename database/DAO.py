from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getYear():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """select distinct YEAR(gds.`Date`) from go_daily_sales gds"""
            cursor.execute(query)
            for row in cursor:
                result.append(row[0])
            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def getCountry():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """select distinct gr.Country from go_retailers gr"""
            cursor.execute(query)
            for row in cursor:
                result.append(row[0])
            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def getRetailers(nazione):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary = True)
            query = """select * from go_retailers gr where gr.Country = %s"""
            cursor.execute(query, (nazione,))
            for row in cursor:
                result.append(Retailer(**row))
            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def getRetailersComuni(anno, nazione):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """select gds1.Retailer_code, gds2.Retailer_code, count(distinct gds1.Product_number) as peso
                from go_daily_sales gds1, go_daily_sales gds2, go_retailers gr1, go_retailers gr2
                where (gds1.Retailer_code > gds2.Retailer_code) and (gds1.Product_number = gds2.Product_number)
                and year(gds1.`Date`) = %s and (year(gds2.`Date`) = year(gds1.`Date`))
                and gds1.Retailer_code = gr1.Retailer_code and gds2.Retailer_code = gr2.Retailer_code
                and gr1.Country = %s and gr1.Country = gr2.Country 
                group by gds1.Retailer_code, gds2.Retailer_code"""
            cursor.execute(query, (anno,nazione,))
            for row in cursor:
                result.append(row)
            cursor.close()
            cnx.close()
            return result
