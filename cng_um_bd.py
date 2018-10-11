import requests
import xmltodict
import json
import cx_Oracle
import request_soap
import variables as vb

def getCNGum():

    # ##################################### CONNECTION #######################

    connection = cx_Oracle.connect(vb.connection)
    cursor = connection.cursor()

    # ####################################get all ids CNG############################################

    prod_pageSize = vb.g_prod_pageSize
    prod_pageNumber = vb.g_prod_pageNumber

    request1 = request_soap.CNG(1, 1)

    encoded_request = request1.encode('utf-8')
    head = {"Host": vb.host,
            "Content-Type": "text/xml; charset=UTF-8",
            "Content-Length": str(len(encoded_request))}

    resp = requests.post(url=vb.vidal_service + "/merlin-service/services/CommonNameGroupService",
                         headers=head,
                         data=encoded_request,
                         verify=False)

    ans = json.dumps(xmltodict.parse(resp.text))
    ans = json.loads(ans)
    TotalIds = int(ans['soap:Envelope']['soap:Body']['ns1:getAllCommonNameGroupFullsResponse'][
                   'ns1:pagedResultCommonNameGroupFull']['rowCount']['#text'])

    totalPaginas = TotalIds / prod_pageSize + 1

    ids = []

    while prod_pageNumber < totalPaginas:
        i = 0
        request2 = request_soap.CNG(prod_pageSize, prod_pageNumber)

        encoded_request = request2.encode('utf-8')
        head = {"Host": vb.host,
                "Content-Type": "text/xml; charset=UTF-8",
                "Content-Length": str(len(encoded_request))}

        resp = requests.post(url=vb.vidal_service + "/merlin-service/services/CommonNameGroupService",
                             headers=head,
                             data=encoded_request,
                             verify=False)

        ans = json.dumps(xmltodict.parse(resp.text))
        ans = json.loads(ans)

        h1 = ans['soap:Envelope']['soap:Body'][
            'ns1:getAllCommonNameGroupFullsResponse']['ns1:pagedResultCommonNameGroupFull']

        while i < prod_pageSize:
            ids.append(h1['result']['commonNameGroupFull']
                       [i]['commonNameGroup']['id'])
            i += 1
        prod_pageNumber += 1

    # ############################################# DOSE UNITS ###############

    for id in ids:

        request = request_soap.unit('DoseUnit', 'CommonNameGroup', id)

        encoded_request = request.encode('utf-8')
        headers = {"Host": vb.host,
                   "Content-Type": "text/xml; charset=UTF-8",
                   "Content-Length": str(len(encoded_request))}
        response = requests.post(url=vb.vidal_service + "/merlin-service/services/PosologyService",
                                 headers=headers,
                                 data=encoded_request,
                                 verify=False)
        doc1 = json.dumps(xmltodict.parse(response.text))
        doc = json.loads(doc1)

        try:
            cngdose = doc['soap:Envelope']['soap:Body'][
                'ns1:searchDoseUnitByCommonNameGroupIdResponse']['ns1:doseUnitList']['doseUnits']
            i = 0
            while i <= len(cngdose['doseUnit']):
                try:
                    UnitId = str(vb.g_market) + '0' + str(vb.g_id_standard) + \
                        cngdose['doseUnit'][i]['id'].rjust(9, '0')
                    id_product = vb.prefix_level0 + id
                    insert_stat = "insert into lnk_product_um" + vb.suffix + "(ID_PRODUCT,ID_PRODUCT_SUPPLIER,ID_UNIT_MEASURE,ID_UNIT_MEASURE_CONTEXT,FLG_DEFAULT,FLG_FRACTIONABLE,FLG_STD) values ('" + \
                        id_product + "','" + vb.g_supplier + "'," + UnitId + ",1,'N','N','Y')"
                    cursor.execute(insert_stat)
                    i += 1
                except KeyError:
                    UnitId = str(vb.g_market) + '0' + str(vb.g_id_standard) + \
                        cngdose['doseUnit']['id'].rjust(9, '0')
                    id_product = vb.prefix_level0 + id
                    insert_stat = "insert into lnk_product_um" + vb.suffix + "(ID_PRODUCT,ID_PRODUCT_SUPPLIER,ID_UNIT_MEASURE,ID_UNIT_MEASURE_CONTEXT,FLG_DEFAULT,FLG_FRACTIONABLE,FLG_STD) values ('" + \
                        id_product + "','" + vb.g_supplier + "'," + UnitId + ",1,'N','N','Y')"
                    cursor.execute(insert_stat)
                    i = len(cngdose['doseUnit']) + 1
                except IndexError:
                    i = len(cngdose['doseUnit']) + 1
        except KeyError:
            pass
        except TypeError:
            pass

    # ############################################### POSOLOGY UNITS #########

    for id in ids:
        request = request_soap.unit('PosologyUnit', 'CommonNameGroup', id)

        encoded_request = request.encode('utf-8')
        headers = {"Host": vb.host,
                   "Content-Type": "text/xml; charset=UTF-8",
                   "Content-Length": str(len(encoded_request))}
        response = requests.post(url=vb.vidal_service + "/merlin-service/services/PosologyService",
                                 headers=headers,
                                 data=encoded_request,
                                 verify=False)
        doc1 = json.dumps(xmltodict.parse(response.text))
        doc = json.loads(doc1)

        try:
            cngposol = doc['soap:Envelope']['soap:Body']['ns1:searchPosologyUnitByCommonNameGroupIdResponse'][
                'ns1:posologyUnitList']['posologyUnits']
            i = 0
            while i <= len(cngposol['posologyUnit']):
                try:
                    UnitId = str(vb.g_market) + '0' + str(vb.g_id_standard) + \
                        cngposol['posologyUnit'][i]['id'].rjust(9, '0')
                    id_product = vb.prefix_level0 + id
                    insert_stat = "insert into lnk_product_um" + vb.suffix + "(ID_PRODUCT,ID_PRODUCT_SUPPLIER,ID_UNIT_MEASURE,ID_UNIT_MEASURE_CONTEXT,FLG_DEFAULT,FLG_FRACTIONABLE,FLG_STD) values ('" + \
                        id_product + "','" + vb.g_supplier + "'," + UnitId + ",2,'N','N','Y')"
                    cursor.execute(insert_stat)
                    i += 1
                except KeyError:
                    UnitId = str(vb.g_market) + '0' + str(vb.g_id_standard) + \
                        cngposol['posologyUnit']['id'].rjust(9, '0')
                    id_product = vb.prefix_level0 + id
                    insert_stat = "insert into lnk_product_um" + vb.suffix + "(ID_PRODUCT,ID_PRODUCT_SUPPLIER,ID_UNIT_MEASURE,ID_UNIT_MEASURE_CONTEXT,FLG_DEFAULT,FLG_FRACTIONABLE,FLG_STD) values ('" + \
                        id_product + "','" + vb.g_supplier + "'," + UnitId + ",2,'N','N','Y')"
                    cursor.execute(insert_stat)
                    i = len(cngposol['posologyUnit']) + 1
                except IndexError:

                    i = len(cngposol['posologyUnit']) + 1
        except KeyError:

            pass
    connection.commit()
    connection.close()
    print ("ALL CNG processed")
