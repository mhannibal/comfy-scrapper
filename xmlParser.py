import xml.sax
from xml.sax import parse


class SiteMapHandler( xml.sax.ContentHandler ):
    def __init__(self):
      self.CurrentData = ""
      self.loc = ""
    

    def startElement(self, name, attrs):
         if name == "loc":
            self.CurrentData = "loc"


    def endElement(self, tag):
        if self.CurrentData == "loc":
            self.CurrentData = ""            


    def characters(self, content):        
        if self.CurrentData == "loc":
            self.loc = content
            print(len(content))
            print("#"*10)
            print(content)
            



if ( __name__ == "__main__"):

    # create an XMLReader
    parse("sitemap.xml", SiteMapHandler())

 