import requests
import xmltodict
import json
import cx_Oracle
import request_soap
import variables as vb


def getProductum():

    # ##################################### CONNECTION #######################

    connection = cx_Oracle.connect(vb.connection)
    cursor = connection.cursor()

    # #################get products lists#############################

    prod_pageSize = vb.g_prod_pageSize
    prod_pageNumber = vb.g_prod_pageNumber

    request_product = request_soap.product(1, 1)

    encoded_request = request_product.encode('utf-8')
    head = {"host": vb.host,
            "Content-Type": "text/xml; charset=UTF-8",
            "Content-Length": str(len(encoded_request))}

    resp = requests.post(url=vb.vidal_service + "/merlin-service/services/ProductService",
                         headers=head,
                         data=encoded_request,
                         verify=False)

    ans = json.dumps(xmltodict.parse(resp.text))
    ans = json.loads(ans)
    TotalIds = int(
        ans['soap:Envelope']['soap:Body']['ns1:getAllProductsResponse']['ns1:pagedResultProduct'][
            'rowCount']['#text'])

    totalPaginas = TotalIds / prod_pageSize + 1

    idsP = []

    while prod_pageNumber < totalPaginas:
        i = 0
        request_product2 = request_soap.product(prod_pageSize, prod_pageNumber)

        encoded_request = request_product2.encode('utf-8')
        head = {"host": vb.host,
                "Content-Type": "text/xml; charset=UTF-8",
                "Content-Length": str(len(encoded_request))}

        resp = requests.post(url=vb.vidal_service + "/merlin-service/services/ProductService",
                             headers=head,
                             data=encoded_request,
                             verify=False)

        ans = json.dumps(xmltodict.parse(resp.text))
        ans = json.loads(ans)

        h1 = ans['soap:Envelope']['soap:Body'][
            'ns1:getAllProductsResponse']['ns1:pagedResultProduct']

        while i < prod_pageSize:
            idsP.append(h1['result']['product'][i]['id'])
            i += 1
        prod_pageNumber += 1
    resp.connection.close()

    # ###############################################PRESCRIPTION UNITS#######

    for id in idsP:
        request = request_soap.unit('PrescriptionUnits', 'Product', id)

        encoded_request = request.encode('utf-8')
        headers = {"host": vb.host,
                   "Content-Type": "text/xml; charset=UTF-8",
                   "Content-Length": str(len(encoded_request))}

        response = requests.post(url=vb.vidal_service + "/merlin-service/services/PosologyService",
                                 headers=headers,
                                 data=encoded_request,
                                 verify=False)
        doc1 = json.dumps(xmltodict.parse(response.text))
        doc = json.loads(doc1)

        try:
            productpresc = doc['soap:Envelope']['soap:Body']['ns1:searchPrescriptionUnitsByProductIdResponse']['ns1:prescriptionUnitList'][
                'prescriptionUnits']
            i = 0
            while i <= len(productpresc['prescriptionUnit']):
                try:

                    UnitId = str(vb.g_market) + '0' + str(vb.g_id_standard) + \
                        productpresc['prescriptionUnit'][i]['id'].rjust(9, '0')

                    insert_stat = "insert into lnk_product_um" + vb.suffix + "(ID_PRODUCT,ID_PRODUCT_SUPPLIER,ID_UNIT_MEASURE,ID_UNIT_MEASURE_CONTEXT,FLG_DEFAULT,FLG_FRACTIONABLE,FLG_STD) values ('" + \
                        id + "','" + vb.g_supplier + "'," + UnitId + ",2,'N','N','Y')"
                    cursor.execute(insert_stat)
                    i += 1
                except KeyError:

                    UnitId = str(vb.g_market) + '0' + str(vb.g_id_standard) + \
                        productpresc['prescriptionUnit']['id'].rjust(9, '0')

                    insert_stat = "insert into lnk_product_um" + vb.suffix + "(ID_PRODUCT,ID_PRODUCT_SUPPLIER,ID_UNIT_MEASURE,ID_UNIT_MEASURE_CONTEXT,FLG_DEFAULT,FLG_FRACTIONABLE,FLG_STD) values ('" + \
                        id + "','" + vb.g_supplier + "'," + UnitId + ",2,'N','N','Y')"
                    cursor.execute(insert_stat)
                    i = len(productpresc['prescriptionUnit']) + 1
                except IndexError:

                    i = len(productpresc['prescriptionUnit']) + 1
        except KeyError:
            continue
        except TypeError:
            continue
    response.connection.close()

    # ############################################### POSOLOGY UNITS #########

    for id in idsP:
        requestPol = request_soap.unit('PosologyUnit', 'Product', id)
        encoded_request = requestPol.encode('utf-8')
        headers = {"host": vb.host,
                   "Content-Type": "text/xml; charset=UTF-8",
                   "Content-Length": str(len(encoded_request))}

        response = requests.post(url=vb.vidal_service + "/merlin-service/services/PosologyService",
                                 headers=headers,
                                 data=encoded_request,
                                 verify=False)

        doc1 = json.dumps(xmltodict.parse(response.text))
        doc = json.loads(doc1)

        try:
            productposol = doc['soap:Envelope']['soap:Body']['ns1:searchPosologyUnitByProductIdResponse']['ns1:posologyUnitList'][
                'posologyUnits']
            i = 0
            while i <= len(productposol['posologyUnit']):
                try:
                    UnitId = str(vb.g_market) + '0' + str(vb.g_id_standard) + \
                        productposol['posologyUnit'][i]['id'].rjust(9, '0')
                    insert_stat = "insert into lnk_product_um" + vb.suffix + "(ID_PRODUCT,ID_PRODUCT_SUPPLIER,ID_UNIT_MEASURE,ID_UNIT_MEASURE_CONTEXT,FLG_DEFAULT,FLG_FRACTIONABLE,FLG_STD) values ('" + \
                        id + "','" + vb.g_supplier + "'," + UnitId + ",2,'N','N','Y')"
                    cursor.execute(insert_stat)
                    i += 1
                except KeyError:
                    UnitId = str(vb.g_market) + '0' + str(vb.g_id_standard) + \
                        productposol['posologyUnit']['id'].rjust(9, '0')
                    insert_stat = "insert into lnk_product_um" + vb.suffix + "(ID_PRODUCT,ID_PRODUCT_SUPPLIER,ID_UNIT_MEASURE,ID_UNIT_MEASURE_CONTEXT,FLG_DEFAULT,FLG_FRACTIONABLE,FLG_STD) values ('" + \
                        id + "','" + vb.g_supplier + "'," + UnitId + ",2,'N','N','Y')"
                    cursor.execute(insert_stat)
                    i = len(productposol['posologyUnit']) + 1
                except IndexError:
                    i = len(productposol['posologyUnit']) + 1
        except KeyError:
            pass
        except TypeError:
            pass
    response.connection.close()
    # ############################################### DOSE UNITS #############

    for id in idsP:
        requestP = request_soap.unit('DoseUnit', 'Product', id)

        encoded_request = requestP.encode('utf-8')
        headers = {"host": vb.host,
                   "Content-Type": "text/xml; charset=UTF-8",
                   "Content-Length": str(len(encoded_request))}

        response = requests.post(url=vb.vidal_service + "/merlin-service/services/PosologyService",
                                 headers=headers,
                                 data=encoded_request,
                                 verify=False)
        doc1 = json.dumps(xmltodict.parse(response.text))
        doc = json.loads(doc1)

        try:
            productdose = doc['soap:Envelope']['soap:Body']['searchDoseUnitByProductIdResponse']['ns1:doseUnitList'][
                'doseUnits']
            i = 0
            while i <= len(productdose):

                try:

                    UnitId = str(vb.g_market) + '0' + str(vb.g_id_standard) + \
                        productdose['doseUnit'][i]['id'].rjust(9, '0')

                    insert_stat = "insert into lnk_product_um" + vb.suffix + "(ID_PRODUCT,ID_PRODUCT_SUPPLIER,ID_UNIT_MEASURE,ID_UNIT_MEASURE_CONTEXT,FLG_DEFAULT,FLG_FRACTIONABLE,FLG_STD) values ('" + \
                        id + "','" + vb.g_supplier + "'," + UnitId + ",1,'N','N','Y')"

                    cursor.execute(insert_stat)

                    i += 1
                except KeyError:

                    UnitId = str(vb.g_market) + '0' + str(vb.g_id_standard) + \
                        productdose['doseUnit']['id'].rjust(9, '0')

                    insert_stat = "insert into lnk_product_um" + vb.suffix + "(ID_PRODUCT,ID_PRODUCT_SUPPLIER,ID_UNIT_MEASURE,ID_UNIT_MEASURE_CONTEXT,FLG_DEFAULT,FLG_FRACTIONABLE,FLG_STD) values ('" + \
                        id + "','" + vb.g_supplier + "'," + UnitId + ",1,'N','N','Y')"

                    cursor.execute(insert_stat)

                    i = len(productdose['doseUnit']) + 1
                except IndexError:
                    i = len(productdose['doseUnit']) + 1

        except KeyError:
            continue

    connection.commit()
    connection.close()
    print ("All products processed")
