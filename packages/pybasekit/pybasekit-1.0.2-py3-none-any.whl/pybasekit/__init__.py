import os
import random
import json

class Encryption:
    '''
    This is a very simple encryption method not meant to be used outside of home projects.
    If used outside home/personal projects, use a different method or you will be at risk.
    '''
    @staticmethod
    def encrypt(text):
        encrypted_text = ""
        for c in text:
            block = str(ord(c) * 7719)
            block = "0" * (3 - len(block)) + block
            encrypted_text += block + "."
        return encrypted_text[:-1]

    @staticmethod
    def decrypt(text):
        decrypted_text = ""
        blocks = text.split(".")
        for block in blocks:
            if block:
                value = int(block) // 7719
                decrypted_text += chr(value)
        return decrypted_text


class Start:
    '''
    Start class to start the services and hold all the other classes and functions,
    sets the main folder to hold all database information.
    '''
    Folder = "pybase_db"

    def __init__(self, folder_name=None):
        if folder_name is not None:
            self.__class__.Folder = folder_name
        if not os.path.exists(self.Folder):
            os.makedirs(self.Folder)

    class CreateDB:
        '''
        User sets a key and class creates a new .pybase file with a simple encrypted key
        and database base information. Returns "200 OK" if run correctly.
        '''
        def __init__(self, name, key):
            self.name = name

        def __new__(self, name, key):
            self.__key = key
            if os.path.exists(f"{Start.Folder}/{name}.pybase") == False:
                start = open(f"{Start.Folder}/{name}.pybase", "a+")
                build = Encryption.encrypt(
                    '{  "DatabaseData": {    "SectionTitles": {}  },  "Data": {}}'
                )
                start.write(f"{Encryption.encrypt(self.__key)}\n{build}")
                return "200 OK"
            else:
                return "404"

    class ConnectDB:
        '''
        Connects to a .pybase file. Returns "200 OK" if access key is correct,
        otherwise returns "Failed to connect: 401" or "Failed to connect: 404".
        '''
        def __init__(self, db_name, access_key):
            self.name = db_name
            self.key = access_key

        def VerifyAUTH(self):
            '''
            Verifies that the user is connected to the .pybase file.
            Returns True if authenticated, otherwise returns False.
            '''
            if os.path.exists(f"{Start.Folder}/{self.name}.pybase") == True:
                data = open(f"{Start.Folder}/{self.name}.pybase", "r+")
                if str(self.key) == str(Encryption.decrypt(data.readline().strip("\n"))):
                    return True
                else:
                    return False
            else:
                return False

        def __str__(self):
            # If Authed, connects
            AUTH = self.VerifyAUTH()
            if AUTH == False:
                return "Failed to connect: 404"
            else:
                if AUTH == True:
                    return "200 OK"
                else:
                    return "Failed to connect: 401"

        def create_section(self, section_title):
            '''
            Checks if authenticated, then creates a new section for the database
            if the section is not already created.
            '''
            auth = self.VerifyAUTH()
            if auth == True:
                lines = []
                with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                    lines = Data.readlines()[1:]
                    data = Encryption.decrypt(lines[0])
                    data = data.replace("'", '"')
                    undata = json.loads(data)
                    if section_title in undata["DatabaseData"]["SectionTitles"]:
                        return "Section is already created"
                    else:
                        newValue = {
                            "DatabaseData": {
                                "SectionTitles": {section_title: section_title}
                            }
                        }
                        undata["DatabaseData"]["SectionTitles"].update(newValue["DatabaseData"]["SectionTitles"])
                        undata["Data"].update({section_title: {}})
                        t = open(f"{Start.Folder}/{self.name}.pybase", "w")
                        undata = Encryption.encrypt(json.dumps(undata))
                        tt = Encryption.encrypt(self.key)
                        t.write(tt + "\n" + undata)
                        return section_title
            else:
                return "401"

        def insert_data(self, section, Data_Title, Data_Value):
            '''
            If authenticated, inserts data if data title is not already in the section.
            '''
            AUTH = self.VerifyAUTH()
            if AUTH == True:
                lines = []
                with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                    lines = Data.readlines()[1:]
                    data = Encryption.decrypt(lines[0])
                    data = data.replace("'", '"')
                    undata = json.loads(data)
                    if section in undata["DatabaseData"]["SectionTitles"]:
                        if str(Data_Title) not in undata["Data"][str(section)]:
                            undata["Data"][str(section)][str(Data_Title)] = Data_Value
                            t = open(f"{Start.Folder}/{self.name}.pybase", "w")
                            t.write(
                                f"{Encryption.encrypt(self.key)}\n{Encryption.encrypt(json.dumps(undata))}"
                            )
                            return "200 OK"
                        else:
                            return "Data Title is already in section"
                    else:
                        return "Could not find section: 404"
            else:
                return "401"

        def insert_list(self, section, Data_Title, List):
            '''
            If authenticated, inserts a list into the section if the section exists.
            '''
            AUTH = self.VerifyAUTH()
            if AUTH:
                if type(List) == list:
                    lines = []
                    with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                        lines = Data.readlines()[1:]
                        data = Encryption.decrypt(lines[0])
                        data = data.replace("'", '"')
                        undata = json.loads(data)
                        if section in undata["DatabaseData"]["SectionTitles"]:
                            if str(Data_Title) not in undata["Data"][str(section)]:
                                undata["Data"][str(section)][str(Data_Title)] = List
                                t = open(f"{Start.Folder}/{self.name}.pybase", "w")
                                t.write(
                                    f"{Encryption.encrypt(self.key)}\n{Encryption.encrypt(json.dumps(undata))}"
                                )
                                return "200 OK"
                            else:
                                return "Data Title is already in section"
                        else:
                            return "Could not find section: 404"
                    return "200 OK"
                else:
                    return f"List is not in correct format. Your type is currently {type(List)}"
            else:
                return "401"

        def get_data(self, section, Data_Title):
            '''
            If authenticated, retrieves data from the specified section and data title.
            '''
            AUTH = self.VerifyAUTH()
            if AUTH == True:
                lines = []
                with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                    lines = Data.readlines()[1:]
                    data = Encryption.decrypt(lines[0])
                    data = data.replace("'", '"')
                    undata = json.loads(data)
                    if section in undata["DatabaseData"]["SectionTitles"]:
                        if str(Data_Title) in undata["Data"][str(section)]:
                            return undata["Data"][str(section)][str(Data_Title)]
                        else:
                            return "Could not find data: 404"
                    else:
                        return "Could not find section: 404"
            else:
                return "401"

        def remove_data(self, section, Data_Title):
            '''
            If authenticated, removes data from the specified section and data title.
            '''
            AUTH = self.VerifyAUTH()
            if AUTH == True:
                lines = []
                with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                    lines = Data.readlines()[1:]
                    data = Encryption.decrypt(lines[0])
                    data = data.replace("'", '"')
                    undata = json.loads(data)
                    if section in undata["DatabaseData"]["SectionTitles"]:
                        if str(Data_Title) in undata["Data"][str(section)]:
                            del undata["Data"][str(section)][str(Data_Title)]
                            t = open(f"{Start.Folder}/{self.name}.pybase", "w")
                            t.write(
                                f"{Encryption.encrypt(self.key)}\n{Encryption.encrypt(json.dumps(undata))}"
                            )
                            return "200 OK"
                        else:
                            return "Could not find data: 404"
                    else:
                        return "Could not find section: 404"
            else:
                return "401"

        def update_data_value(self, section, Data_Title, New_Value):
            '''
            If authenticated, updates the value of the specified data in the section.
            '''
            AUTH = self.VerifyAUTH()
            if AUTH == True:
                lines = []
                with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                    lines = Data.readlines()[1:]
                    data = Encryption.decrypt(lines[0])
                    data = data.replace("'", '"')
                    undata = json.loads(data)
                    if section in undata["DatabaseData"]["SectionTitles"]:
                        if str(Data_Title) in undata["Data"][str(section)]:
                            undata["Data"][str(section)][str(Data_Title)] = New_Value
                            t = open(f"{Start.Folder}/{self.name}.pybase", "w")
                            t.write(
                                f"{Encryption.encrypt(self.key)}\n{Encryption.encrypt(json.dumps(undata))}"
                            )
                            return undata["Data"][str(section)][str(Data_Title)]
                        else:
                            return "Could not find data: 404"
                    else:
                        return "Could not find section: 404"
            else:
                return "401"

        def get_all_data(self):
            '''
            If authenticated, retrieves all data from the database.
            '''
            AUTH = self.VerifyAUTH()
            if AUTH == True:
                lines = []
                with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                    lines = Data.readlines()[1:]
                    data = Encryption.decrypt(lines[0])
                    data = data.replace("'", '"')
                    undata = json.loads(data)
                    return undata["Data"]
            else:
                return "401"

        def get_section_data(self, section):
            '''
            If authenticated, retrieves data from the specified section.
            '''
            AUTH = self.VerifyAUTH()
            if AUTH == True:
                lines = []
                with open(f"{Start.Folder}/{self.name}.pybase") as Data:
                    lines = Data.readlines()[1:]
                    data = Encryption.decrypt(lines[0])
                    data = data.replace("'", '"')
                    undata = json.loads(data)
                    if section in undata["DatabaseData"]["SectionTitles"]:
                        return undata["Data"][str(section)]
                    else:
                        return "Could not find section: 404"
            else:
                return "401"
            

'''

    Once again this is not meant to be used outside personal project as it will put the information in the database you created at risk.
    If you want to make it secure you can modify the code but with with the current encryption and decryption

    Meant for personal learning and person softwares and thing like that.


    Last module update: 7/13/23

'''