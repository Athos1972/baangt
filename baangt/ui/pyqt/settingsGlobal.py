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
    """
    __instance = None

    class GlobalSettings:
        """ Inner Class which will be used """

        def __init__(self):
            """ Initialize the config data from json file """
            self.config = {}
            try:
                with open("globalSettings.json", "r") as f:
                    data = json.loads(f.read())
            except Exception as e:
                print("Error Occured while reading globalSettings.json file")
                print(e)
                data = {}
            self.config = data

        def updateValue(self, jsonfile):
            """ This will update the existing settings with given dictionary
            of data in json file
            """
            # path should be absolute to process the file
            if os.path.isabs(jsonfile):
                raise Exception("File can't be opened")
            try:
                with open(jsonfile, 'r') as f:
                    jsondata = json.loads(f.read())
            except Exception as e:
                print("Exception occured. Ignoring reading")
                print(e)
                jsondata = {}

            # update the global settings
            for localvar in jsondata:
                for globalvar in self.config:
                    # if type is simple key value
                    if isinstance(globalvar, dict):
                        # Global variable is in standard format
                        # Compare with variableName attributes
                        if globalvar['variableName'].lower() == localvar.lower():
                            globalvar['value'] = jsondata[localvar]
                            # clear the data from localvar
                            del(jsondata[localvar])

                    elif isinstance(globalvar, str):
                        # the variable is of type string
                        # like Path, OutputDir, Screenshot dir
                        if globalvar.lower() == localvar.lower():
                            # update the Value
                            self.config[globalvar] = jsondata[localvar]
                            # remove the key value pair from localvar
                            del(jsondata[localvar])
            # Add unrecognized data to GlobalSetting
            self.config.extends(jsondata.items())

             # New Settings which is not found, can be added here







# if__name__ == "__main__":
#     pass
