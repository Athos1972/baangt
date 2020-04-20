import json
import os
# This Python file uses the following encoding: utf-8


class GlobalSettings:
    """ A Singleton Class to hold all settings in Baant.
    Read globalSettings.json file and prepare dictonary data.
    Method:
        getInstance : Public static method to get return Instance object
        saveSimpleJson:  Save settings as json file
        returnSetting:  Return dictionary of all settings

    JsonFile Each Entry Format:
        "variableName":{ Actual Variable Name used in program
                        "hint ": This information will be shown as tooltip
                        "type":  based on input, Form field created
                                 bool : Checkbox
                                 type : TextInputBox
                                 select :  ComboBox
                        "default":  Default value if nothing is provided
                        "options" :  List Type for all type of possible
                         "display" : This will be displayed
                      }
    """
    __instance = None

    class __GlobalSettings:
        """ Inner Class which will be used """

        def __init__(self, jsonfile=None):
            """ Initialize the config data from json file """
            self.config = {}
            if jsonfile:
                # internally call initBaseConfig and addValue
                self.addValue(jsonfile)
            else:
                self.initBaseConfig()

        def initBaseConfig(self):
            """ This function will initialize the config data
            with globalSetting.json content
            """
            # init the file to base state
            if self.config:
                self.config = {}
            globalFile = "globalSetting.json"
            if not os.path.isfile(globalFile):
                dirpath = os.path.dirname(os.path.abspath(__file__))
                globalFile = os.path.join(dirpath, 'globalSetting.json')
            if not os.path.isfile(globalFile):
                # package attempt is failed
                dirpath = os.getcwd()
                globalFile = os.path.join(os.path.dirname(dirpath), 'globalSetting.json')
            # alert on console if globalSettings not found
            if not os.path.isfile(globalFile):
                print(" {} File not a valid file ".format(globalFile))
            data = self.parseJsonfile(globalFile)
            self.config = data


        def isValidFile(self, jsonfile):
            """ This return True if it can be opened """
            try:
                with open(jsonfile) as f:
                    json.loads(f.read())
                return True
            except Exception as e:
                print("Unable to read the file {}".format(jsonfile))
                print(e)
                return False

        def filterIniKey(self, filterkey=[]):
            """ This function will remove
            RootPath, ScreenshotPath, ImportPath, ExportPath
            """
            data = {}
            iniData = {'RootPath', 'ScreenshotPath',
                       'ImportPath', 'ExportPath'}
            if filterkey:
                iniData.update(filterkey)

            for key, value in self.config.items():
                if key not in iniData:
                    data[key] = value

            return data

        def parseJsonfile(self, jsonfile):
            """ This function will parse the input json file,
            and return  formated as per baangt
            Accept Format:
                "Release":{'hint':"somehint','type':'bool',
                            'options':['some optins'],
                             'displayText':"shown"
                             }
                 "Release":"22.21.b.dev"
            """
            if self.isValidFile(jsonfile):
                # loop with each variable
                # empty dictionary to store the parse valued
                resultDict = {}
                with open(jsonfile) as f:
                    data = json.loads(f.read())
                    # check if its globalSetting.json
                    if data.get('settings'):
                        # parse the global file
                        resultDict.update(data['settings'])
                    else:
                        for key, value in data.items():
                            resultDict[key] = GlobalSettings.transformToDict(value)

                return resultDict
            else:
                print("Invalid Format ")
                return {}

        def addValue(self, jsonfile):
            """ This will update the existing settings with given dictionary
            of data in json file.
            Also, this will remove all current dictionary data

            """
            # init with base config
            self.initBaseConfig()

            # path should be absolute to process the file
            parsed_data = self.parseJsonfile(jsonfile)
            if parsed_data:
                for key, value in parsed_data.items():
                    if key in self.config:
                        self.config[key]['default'] = value['default']
                    else:
                        self.config[key] = value

        def updateValue(self, dictData):
            """ This function will update existing Dictionary setting
            from the provided value
            """
            if isinstance(dictData, dict):
                # loop each items
                for key in dictData:
                    if key in self.config:
                        # The key is present so update the value
                        self.config[key]['default'] = dictData[key]

    def __new__(cls, jsonfile=None):
        """ Get the instance and update the value """
        if not GlobalSettings.__instance:
            # Create New instance
            GlobalSettings.__instance = GlobalSettings.__GlobalSettings(
                                     jsonfile
                                     )
        else:
            GlobalSettings.__instance.addValue(jsonfile)
        return GlobalSettings.__instance

    @staticmethod
    def getInstance():
        """ Return current instance of Class"""
        if GlobalSettings.__instance is None:
            # Create a new instance
            GlobalSettings.__instance = GlobalSettings.__GlobalSettings()
        return GlobalSettings.__instance

    @staticmethod
    def transformToDict(value):
        """ this convert value to dictionary format with keys
        "hint" : default to value
        "type" : default to "text"
        "default":  default to value
        "options" :  default to value
        "diplayText" :  default to value
        Example:  Input = "path"
                  Output = {'hint':'path',
                            'type': 'text',
                            'default': 'path',
                            'options': ['path'],
                            'displyText': 'path'
                            }
        """
        data = {}
        if isinstance(value, dict):
            # dictionary item, get the require parameter
            defaultValue = value.get('default','sampleValue')
            data['hint'] = value.get('hint', defaultValue)
            data['type'] = value.get('type', 'text')
            data['options'] = value.get('options', [defaultValue])
            data['displayText'] = value.get('displayText', defaultValue)
            data['default'] = defaultValue

            # return data
            return data
        elif isinstance(value, str):
            value = value
        elif isinstance(value, set):
            value = value.pop()
        elif isinstance(value, bool):
            value = str(value)
        else:
            print("Invalid value  : {}".format(value))
            value = "exampleValue"
        data['hint'] = value
        data['type'] = 'text'
        data['options'] = [value]
        data['displayText'] = value
        data['default'] = value

        return data


if __name__ == "__main__":
    print("Initializing the data")
    d = GlobalSettings('globalSetting.json')
    print(d.config)
