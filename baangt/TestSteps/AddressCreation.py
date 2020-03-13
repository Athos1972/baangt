class AddressCreate:
    """
    This file Define a Singleton Class AddressCreate which will have static
        method returnAddress to return the address in format.


        CountryCode**
        PostlCode**
        CityName
        StreetName
        HouseNumber
        AdditionalData1
        AdditionalData2

        Input: value1 = {'CountryCode':"IN",'CityName':"Mohali"} [optional]
               value2 = "sales_"

        Output: {'sales_CountryCode':"IN","sales_PostalCode":"19883",
              "sales_CityName":"Mohali","sales_StreeName":"32HB",
               "sales_AdditionalData1":"Near Hospital",
               "sales_AdditionData2":"Ajanta Mandis Park"}


        Sample Usage:
                Default Value
                >> AddressCreate.returnAddress()

                Pass value of ('HouseNumber', 'AdditionalData1',
                 'AdditionalData2', 'StreetName', 'CityName', 'PostalCode',
                 'CountryCode' ) to change.

               For example:
                >> Update City Name
                  AddressCreate(value1={"CityName":"Something"})

                  or
                  AddressCreate({"CityName":"Something"})

                >> Update Country Name
                  AddressCreate({"CountryCode":"US"})



    """

    __instance = None

    class __AddressCreate:
        """ Inner class   """

        def __init__(self, value1={}, value2=""):
            addressData = {"HouseNumber": "6",
                           "AdditionalData1": "Near MahavirChowk",
                           "AdditionalData2": "Opposite St. Marish Church",
                           "StreetName": "GoreGaon",
                           "CityName": "Ambala",
                           "PostalCode": "160055",
                           "CountryCode": "India",
                           }
            prefixData = ""  # empty initially
            
            self.value1 = addressData
            self.value2 = prefixData

            # Now update the value
            self.updateValue(value1, value2)

        def updateValue(self, value1, value2):
            """ This function will process value1,value2 and
                prepare dictionary data
            """
            # value1
            try:
                value1 = dict(value1)
                value2 = str(value2)

            except Exception as e:
                print("Error Occured :  ", e)
            # process only dictionary data, ignore everything else
            if isinstance(value1, type({})):
                for key, value in value1.items():
                    if key in self.value1:
                        self.value1[key] = value

            if value2.strip():
                self.value2 = value2.strip()

        def __str__(self):
            """ AddressCreation print information"""
            return "AddressCreate Instance id :{} ".format(id(self))

        def __repr__(self):
            return "AddressCreate Instance id:{}\nvalue1: {}\nvalue2: {}".format(
                id(self), self.value1, self.value2)

    @staticmethod
    def getInstance():
        if AddressCreate.__instance is None:
            AddressCreate.__instance = AddressCreate.__AddressCreate()
        return AddressCreate.__instance

    def __new__(cls, value1={}, value2=""):
        """ Get the instance and update the value """
        if not AddressCreate.__instance:
            # Create new instance
            AddressCreate.__instance = AddressCreate.__AddressCreate(
                value1, value2)
        else:
            # Update old instance
            AddressCreate.__instance.updateValue(value1, value2)
        return AddressCreate.__instance

    @staticmethod
    def returnAddress():
        """This function will use value1 and value2 to prepare structured
            Address Data
        """
        # get the instance
        a = AddressCreate.getInstance()
        data = {}

        for key, val in a.value1.items():
            # prefix_value + addresskey = addresskey_value
            # if prefix = "Sales" and "CountryCode" = "India"
            # then final data will be data['Sales_CountryCode'] = India
            if a.value2:
                # prefix is given
                data[a.value2 + key] = val
            else:
                data[key] = val
        # finally return the processed dataDict

        return data
