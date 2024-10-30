import json

class jsoning:
    def __init__(self,json_file):
               self.json_file = json_file
        
    def json_write(self,content,json_file):
        with open(json_file, "w") as j:
            json.dump(content,j,indent=2)
    
    def json_load_section(self,json_file,value):
        with open(json_file, "r") as j:
            json.load(j)
        for i in j[value]:
            print(i)
            
js = jsoning("D:\Code\Python\Discord-Economy-Bot\small_data.json")
file = "D:\Code\Python\Discord-Economy-Bot\small_data.json"
js.json_write("Balls",file)
js.json_load_section(file,"Balls")


        
        