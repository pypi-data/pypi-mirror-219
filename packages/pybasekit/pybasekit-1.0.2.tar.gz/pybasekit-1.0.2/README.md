Do not use this for anything big as its not a secure way to store data.
This is meant to be used for fun and creating things for yourself or with a small group of people.

Example code:

import pybasekit

service = pybasekit.Start() # starts the service
NewDB = service.CreateDB("MyDatabase", "key") # creates a new database called MyDatabase and with the key "key"
db = service.ConnectDB("MyDatabase", "key") # Connects to the database using the same key
section = db.create_section("newsection") # Creates a section in the database to store data
collect = db.get_section_data("newsection") # Gets all data from section
print(collect) # prints the data from the section

Not all features were included in the example here are all the features:
    Start()/
        CreateDB(name, key)
        ConnectDB(name, key)/
            create_section(section_title)
            insert_data(section, Data_Title, Data_Value)
            insert_list(section, Data_Title, List)
            get_data(self, section, Data_Title)
            remove_data(section, Data_Title)
            update_data_value(section, Data_Title, New_Value)
            get_all_data()
            get_section_data(section)


