from xml.dom.minidom import parse
import json
import requests 

CONST_SITEMAP=  "sitemap.xml"
class Parser:
    def __init__(self, url) -> None:
        self.sitemap_url = f"https://{url}/{CONST_SITEMAP}"
        self.sitemap_productlist_url = ""
        self.sitemap_productlist = []

    def get_file_from_url(self, url, local_file_name):
        try :
            response = requests.get(url)
            if response.ok:                            
                open(local_file_name, "w",  encoding='utf8').write(response.text)
                return local_file_name
        except :
            raise   

    def extract_productList_url(self):        
        try :
            file_name = self.get_file_from_url(self.sitemap_url, "temp_sitemap.xml")  
            document = parse(file_name)                
            for i in document.getElementsByTagName("loc"):
                if i.firstChild:
                    textValue = i.firstChild.nodeValue
                    if textValue.find("sitemap_products_1.xml") >-1: 
                        self.sitemap_productlist_url = textValue                        
                        return True
        except :
            raise
        return False   
    

    def extract_productList(self):        
        try :                
            file_name = self.get_file_from_url(self.sitemap_productlist_url, "temp_productlist.xml")  
            document = parse(file_name)    
            for i in document.getElementsByTagName("url"):                
                if i.childNodes[1] and i.childNodes[1].childNodes[0].nodeValue.find("/products/") == -1:
                    
                    continue
                product = {}                
                for el in i.childNodes:
                    name= el.nodeName                        
                    if name == 'image:image':
                            for imgel in el.childNodes:
                                if  imgel.nodeName == 'image:loc':
                                    if imgel.firstChild:                             
                                        product['src'] = imgel.firstChild.nodeValue                                
                                else:
                                    if imgel.firstChild:                             
                                        product[imgel.nodeName.replace(':','-')] = imgel.firstChild.nodeValue
                    elif name == 'loc':
                        if el.firstChild:                            
                            product["url"] = el.firstChild.nodeValue
                            product["json_url"] = f'{el.firstChild.nodeValue}.json'
                    elif name == 'lastmod':
                        if el.firstChild:                        
                            product["updated_at"] = el.firstChild.nodeValue
                    else :
                        if el.firstChild:                        
                            textValue = el.firstChild.nodeValue
                            #if name == "loc":
                            product[name] = textValue
                            #return True
                self.sitemap_productlist.append(product)
        except :
            raise
        return False   

    def parse_productJson(self, json_url):        
        #file_name = self.get_file_from_url( json_url, f"{json_url.split('/')[-1]}")                 
        response = requests.get(json_url)
        if response.ok: 
            product_dict = json.loads(response.text)
            print(f'{product_dict["product"]["id"]}: {product_dict["product"]["updated_at"]} {product_dict["product"]["title"]}')
            


    def __str__(self) -> str:
        return f"sitemap: {self.sitemap_url}"

if __name__ == "__main__":
    #partakefoods.com
    #thecomfy.com
    #https://www.naja.co/
    p = Parser("thecomfy.com")
    #print(p)    
    # p.extract_productList2()
    if p.extract_productList_url():
        p.extract_productList()
    for i in p.sitemap_productlist:
        #print(i["json_url"], '\n')
        p.parse_productJson(i["json_url"])
