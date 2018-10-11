def CNG(Ps, Pn):
    return """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:Vidal">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:getAllCommonNameGroupFulls>
         <urn:name></urn:name>
         <urn:aggregates>
            <urn:Aggregate>DRUG</urn:Aggregate>
         </urn:aggregates>
         <urn:pageSize>""" + str(Ps) + """</urn:pageSize>
         <urn:pageNumber>""" + str(Pn) + """</urn:pageNumber>
      </urn:getAllCommonNameGroupFulls>
   </soapenv:Body>
</soapenv:Envelope>"""


def pack(Ps, Pn):
    return """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:Vidal">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:getAllPackages>
         <urn:packApiFilter>ALL</urn:packApiFilter>
         <urn:types>
            <urn:ProductType>VIDAL</urn:ProductType>
         </urn:types>
         <urn:marketStatuses>
            <urn:MarketStatus>AVAILABLE</urn:MarketStatus>
            <urn:MarketStatus>NEW</urn:MarketStatus>
            <urn:MarketStatus>DELETED</urn:MarketStatus>
            <urn:MarketStatus>DELETED_ONEYEAR</urn:MarketStatus>
         </urn:marketStatuses>
         <urn:pageNumber>""" + str(Pn) + """</urn:pageNumber>
         <urn:pageSize>""" + str(Ps) + """</urn:pageSize>
      </urn:getAllPackages>
   </soapenv:Body>
</soapenv:Envelope>"""


def product(Ps, Pn):
    return """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:Vidal">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:getAllProducts>
         <urn:productApiFilter>ALL</urn:productApiFilter>
         <urn:types>
            <urn:ProductType>VIDAL</urn:ProductType>
         </urn:types>
         <urn:marketStatuses>
            <urn:MarketStatus>AVAILABLE</urn:MarketStatus>
            <urn:MarketStatus>NEW</urn:MarketStatus>
            <urn:MarketStatus>DELETED</urn:MarketStatus>
            <urn:MarketStatus>DELETED_ONEYEAR</urn:MarketStatus>
         </urn:marketStatuses>
         <urn:pageNumber>""" + str(Pn) + """</urn:pageNumber>
         <urn:pageSize>""" + str(Ps) + """</urn:pageSize>
      </urn:getAllProducts>
   </soapenv:Body>
</soapenv:Envelope>"""


def unit(UnitType, ProductType, id):

    return u"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:Vidal">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:search""" + str(UnitType) + """By""" + str(ProductType) + """Id>
         <urn:""" + str(ProductType[0].lower() + ProductType[1:]) + """Id>""" + str(id) + """</urn:""" + str(ProductType[0].lower() + ProductType[1:]) + """Id>
      </urn:search""" + str(UnitType) + """By""" + str(ProductType) + """Id>
   </soapenv:Body>
</soapenv:Envelope>"""
