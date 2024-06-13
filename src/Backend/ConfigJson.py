import json


class ConfigJson():
    def __init__(self):
        self.template_path = r"C:\Users\KOJ1CT\Desktop\Projetos\enp2-angle-analysis\src\Backend\jsontest.json"
        

    def read(self):
        
        with open(self.template_path, 'r') as template_file:
            template_json = json.load(template_file)
        
        
        colorSplit = template_json["Lines Color"].split(',')
        color = colorSplit[2] + "," + colorSplit[1] + "," + colorSplit[0]
        color = color.replace('(', '')
        color = color.replace(')', '')
        color = color.replace(' ', '')
        template_json["Lines Color"] = color
        
        colorSplit = template_json["Borders Color"].split(',')
        color = colorSplit[2] + "," + colorSplit[1] + "," + colorSplit[0]
        color = color.replace('(', '')
        color = color.replace(')', '')
        color = color.replace(' ', '')
        template_json["Borders Color"] = color
        
        colorSplit = template_json["Center Color"].split(',')
        color = colorSplit[2] + "," + colorSplit[1] + "," + colorSplit[0]
        color = color.replace('(', '')
        color = color.replace(')', '')
        color = color.replace(' ', '')
        template_json["Center Color"] = color
        
        colorSplit = template_json["Adjust Color"].split(',')
        color = colorSplit[2] + "," + colorSplit[1] + "," + colorSplit[0]
        color = color.replace('(', '')
        color = color.replace(')', '')
        color = color.replace(' ', '')
        template_json["Adjust Color"] = color
        
        
        return template_json


    def getColors(self):
        colorsList = []
        
        with open(self.template_path, 'r') as template_file:
            template_json = json.load(template_file)
        
        colorsList.append(template_json["Lines Color"])
        colorsList.append(template_json["Borders Color"])
        colorsList.append(template_json["Center Color"])
        colorsList.append(template_json["Adjust Color"])
    
        return colorsList
    
    def getWidths(self):
        colorsList = []
        
        with open(self.template_path, 'r') as template_file:
            template_json = json.load(template_file)
        
        colorsList.append(template_json["Lines Width"])
        colorsList.append(template_json["Borders Width"])
        colorsList.append(template_json["Center Width"])
        colorsList.append(template_json["Adjust Width"])
    
        return colorsList


    def set(self, widths = None, colors = None, path = None):
        
        with open(self.template_path, 'r') as template_file:
            template_json = json.load(template_file)
            
        if isinstance(widths, list) or isinstance(colors, list):
            template_json["Lines Width"] = widths[0]
            template_json["Borders Width"] = widths[1]
            template_json["Center Width"] = widths[2]
            template_json["Adjust Width"] = widths[3]
            
            template_json["Lines Color"] = str(colors[0])
            template_json["Borders Color"] = str(colors[1])
            template_json["Center Color"] = str(colors[2])
            template_json["Adjust Color"] = str(colors[3])
            
        if isinstance(path, str):
            template_json["Path"] = path

        with open(self.template_path, "w") as outfile:
            json.dump(template_json, outfile)
    
    
        