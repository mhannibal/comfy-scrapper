from xml.dom.minidom import parse
try :
    document = parse("sitemap.xml")    
    for i in document.getElementsByTagName("loc"):
        if i.firstChild:
            textValue = i.firstChild.nodeValue
            if textValue.find("sitemap_products_1.xml") >-1: 
                print(textValue)
except :
    raise


