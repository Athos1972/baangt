from baangt.base import GlobalConstants as GC

class AddressCreate:

    returnDict = {
        GC.ADDRESS_COUNTRYCODE: "",
        GC.ADDRESS_POSTLCODE: "",
        GC.ADDRESS_CITYNAME: "",
        GC.ADDRESS_STREETNAME: "",
        GC.ADDRESS_HOUSENUMBER: "",
        GC.ADDRESS_ADDITION1: "",
        GC.ADDRESS_ADDITION2: ""
    }

    def __init__(self, addressFilterCriteria:dict):
        self.filterCriteria = addressFilterCriteria
        pass

    def returnAddress(self):
        # fixme: Implement the functionality.

        result = self.returnDict
        if self.filterCriteria.get(GC.ADDRESS_COUNTRYCODE) == 'AT' or not self.filterCriteria:
            result[GC.ADDRESS_COUNTRYCODE] = "AT"
            result[GC.ADDRESS_CITYNAME] = "Wien"
            result[GC.ADDRESS_POSTLCODE] = "1020"
            result[GC.ADDRESS_STREETNAME] = "Castellezgasse"
            result[GC.ADDRESS_HOUSENUMBER] = "32"
            result[GC.ADDRESS_ADDITION1] = "5"
        elif self.filterCriteria.get(GC.ADDRESS_COUNTRYCODE) == 'CY':
            result[GC.ADDRESS_COUNTRYCODE] = "CY"
            result[GC.ADDRESS_CITYNAME] = "Larnaca"
            result[GC.ADDRESS_POSTLCODE] = "6020"
            result[GC.ADDRESS_STREETNAME] = "Pavlou Valsamaki"
            result[GC.ADDRESS_HOUSENUMBER] = "1"
            result[GC.ADDRESS_ADDITION1] = "Apt 202"

        return self.returnDict

