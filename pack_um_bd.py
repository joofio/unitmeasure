import requests
import xmltodict
import json
import cx_Oracle
import request_soap
import variables as vb


def getPackum():

    # ############################## CONNECTION #######################

    connection = cx_Oracle.connect(vb.connection)
    cursor = connection.cursor()

    # ###############################################get all ids PACK#########

    prod_pageSize = vb.g_prod_pageSize
    prod_pageNumber = vb.g_prod_pageNumber

    request_pack = request_soap.pack(1, 1)

    encoded_request = request_pack.encode('utf-8')
    head = {"Host": vb.host,
            "Content-Type": "text/xml; charset=UTF-8",
            "Content-Length": str(len(encoded_request))}

    resp = requests.post(url=vb.vidal_service + "/merlin-service/services/PackService",
                         headers=head,
                         data=encoded_request,
                         verify=False)

    ans = json.dumps(xmltodict.parse(resp.text))
    ans = json.loads(ans)
    TotalIds = int(
        ans['soap:Envelope']['soap:Body']['ns1:getAllPackagesResponse']['ns1:pagedResultPack'][
            'rowCount']['#text'])

    totalPaginas = TotalIds / prod_pageSize + 1

    idsPack = []

    while prod_pageNumber < totalPaginas:
        i = 0
        request_pack2 = request_soap.pack(prod_pageSize, prod_pageNumber)

        encoded_request = request_pack2.encode('utf-8')
        head = {"Host": vb.host,
                "Content-Type": "text/xml; charset=UTF-8",
                "Content-Length": str(len(encoded_request))}

        resp = requests.post(url=vb.vidal_service + "/merlin-service/services/PackService",
                             headers=head,
                             data=encoded_request,
                             verify=False)

        ans = json.dumps(xmltodict.parse(resp.text))
        ans = json.loads(ans)
        h1 = ans['soap:Envelope']['soap:Body'][
            'ns1:getAllPackagesResponse']['ns1:pagedResultPack']
        while i < prod_pageSize:
            idsPack.append(h1['result']['pack'][i]['id'])
            i += 1
        prod_pageNumber += 1

    # ###########################################POSOLOGY UNITS################

    for id in idsPack:
        request = request_soap.unit('PosologyUnit', 'Package', id)

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
            packposol = doc['soap:Envelope']['soap:Body']['ns1:searchPosologyUnitByPackageIdResponse']['ns1:posologyUnitList'][
                'posologyUnits']
            i = 0
            while i <= len(packposol['posologyUnit']):
                try:
                    UnitId = str(vb.g_market) + '0' + str(vb.g_id_standard) + \
                        packposol['posologyUnit'][i]['id'].rjust(9, '0')
                    id_product = vb.prefix_level3 + id
                    insert_stat = "insert into lnk_product_um" + vb.suffix + "(ID_PRODUCT,ID_PRODUCT_SUPPLIER,ID_UNIT_MEASURE,ID_UNIT_MEASURE_CONTEXT,FLG_DEFAULT,FLG_FRACTIONABLE,FLG_STD) values ('" + \
                        id_product + "','" + vb.g_supplier + "'," + UnitId + ",2,'N','N','Y')"
                    cursor.execute(insert_stat)
                    i += 1
                except KeyError:
                    UnitId = str(vb.g_market) + '0' + str(vb.g_id_standard) + \
                        packposol['posologyUnit']['id'].rjust(9, '0')
                    id_product = vb.prefix_level3 + id
                    insert_stat = "insert into lnk_product_um" + vb.suffix + "(ID_PRODUCT,ID_PRODUCT_SUPPLIER,ID_UNIT_MEASURE,ID_UNIT_MEASURE_CONTEXT,FLG_DEFAULT,FLG_FRACTIONABLE,FLG_STD) values ('" + \
                        id_product + "','" + vb.g_supplier + "'," + UnitId + ",2,'N','N','Y')"
                    cursor.execute(insert_stat)
                    i = len(packposol['posologyUnit']) + 1
                except IndexError:
                    i = len(packposol['posologyUnit']) + 1
        except KeyError:
            pass
        except TypeError:
            pass

    # ################################################### PRESCRIPTION UNITS #

    for id in idsPack:
        request = request_soap.unit('PrescriptionUnits', 'Package', id)

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
            packpresc = doc['soap:Envelope']['soap:Body']['ns1:searchPrescriptionUnitsByPackageIdResponse']['ns1:prescriptionUnitList'][
                'prescriptionUnits']
            i = 0
            while i <= len(packpresc['prescriptionUnit']):
                try:

                    UnitId = str(vb.g_market) + '0' + str(vb.g_id_standard) + \
                        packpresc['prescriptionUnit'][i]['id'].rjust(9, '0')
                    id_product = vb.prefix_level3 + id
                    insert_stat = "insert into lnk_product_um" +vb.suffix + "(ID_PRODUCT,ID_PRODUCT_SUPPLIER,ID_UNIT_MEASURE,ID_UNIT_MEASURE_CONTEXT,FLG_DEFAULT,FLG_FRACTIONABLE,FLG_STD) values ('" + \
                        id_product + "','" + vb.g_supplier + "'," + UnitId + ",2,'N','N','Y')"
                    cursor.execute(insert_stat)
                    i += 1

                except KeyError:

                    UnitId = str(vb.g_market) + '0' + str(vb.g_id_standard) + \
                        packpresc['prescriptionUnit']['id'].rjust(9, '0')

                    id_product = vb.prefix_level3 + id

                    insert_stat = "insert into lnk_product_um" + vb.suffix + "(ID_PRODUCT,ID_PRODUCT_SUPPLIER,ID_UNIT_MEASURE,ID_UNIT_MEASURE_CONTEXT,FLG_DEFAULT,FLG_FRACTIONABLE,FLG_STD) values ('" + \
                        id_product + "','" + vb.g_supplier + "'," + UnitId + ",2,'N','N','Y')"
                    cursor.execute(insert_stat)

                    i = len(packpresc['prescriptionUnit']) + 1

                except IndexError:

                    i = len(packpresc['prescriptionUnit']) + 1

        except KeyError:
            pass
        except TypeError:
            pass

    connection.commit()
    cursor.close()
    print("All Packages processed")
