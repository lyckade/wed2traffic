# -*- coding: iso-8859-1 -*-

#import os


class Wed2traffic():
    """ 
    Extracts data out of apt.dat files generated with WED and converts it for
    the marginal GroundTraffic plugin.
    This class uses exact one input file. 
    
    It allows you to use the WED for editing the paths of your ground traffic.
    
    To define your objects you need to make a template file. This file will 
    be copied to your GraundTraffic.txt. All commands stay, just the command 
    path will be used.
    
    For the output file there are 2 modes availiable, which can be set over
    self.mode. The mode is the same as in the open() function:
    a = append 
        Appends the generated data to a file. 
    w = write
        Writes the generated data to one file. If this file is existing it will
        be overwritten.
    #=======================================================================
    # Information about the file format from the WED at:
    # http://data.x-plane.com/file_specs/XP%20APT1000%20Spec.pdf
    #=======================================================================
        
    """
    def __init__(self,inFile,templateFile,outFile):
        
        self.inFile = inFile
        self.templateFile = templateFile
        self.outFile = outFile
        
        self.titles = []
        
        #------------------------------------------------- default mode is write
        self.mode = "w"
        
        #=======================================================================
        # apd.dat row codes
        # Do not change!
        #=======================================================================
        
        #------- Defines the which row codes are used to extract the koordinates
        self.rowCodesNode = [111,112,113,114,115,116]
        #-------------------------------------- Defines the row codes for titles
        self.rowCodesTitle = [120]
        #------------------------------- The view point is used for the location
        self.rowCodeViewPoint = 14
        #-------------------------------------------------------- airport header
        self.rowCodeAirportHeader = 1
        
        # Get the possible titles
        self.getTitles()
    
    
    def extractPaths(self):
        """
        Generates the output file and writes all the paths into it.
        
        """
        #-------------------------------------------- Pointer to the output file
        outFile = open(self.outFile,self.mode)
        
        #------------------------------------------------------ write the header
        outFile.write("# Generated using wed2traffic\n# more information at xplaneblog.de\n")
        
        #----------------------------------------------------- ICAO and Location
        icao = self.searchRowCode(self.rowCodeAirportHeader)[0][4]
        location = self.searchRowCode(self.rowCodeViewPoint)[0]
        outFile.write("%s %s %s\n" % (icao,location[1],location[2]))
        
        tFile = open(self.templateFile,"r")
        for tl in tFile:
            if tl.startswith("path "):
                koordinates = self.getKoordinates(tl[5:].strip())
                for k in koordinates:
                    outFile.write("%s %s\n" % k)
                
                print "%s:%s" % (tl[5:].strip(),len(koordinates))
            else:
                outFile.write(tl)
        
        #for title in titles:
        #    koordinates = self.getKoordinates(title)
        #    for k in koordinates:
        #        outFile.write("%s %s\n" % k)
        tFile.close()
        outFile.close()
        
    def getKoordinates(self,title):
        """
        Exctracts the koordinates out from the input file an returns a list of touples
        with the format (x,y)
        @param title: The title as it is specified in the apt.dat file
        @type title: string
        """
        f = open(self.inFile,"r")
        koordinates = []
        addLine = False
        for l in f:
            items = self.parseLine(l)
            # Skip the entry if it is a empty line
            if len(items)==0:
                continue
            
            if items[0] in self.rowCodesTitle:
                if self.getTitle(l)==title:
                    addLine = True
                    continue
                else:
                    addLine = False
            # Wenn addLine True, dann duerfen die Koordinaten ermittelt werden
            if addLine:
                koordinates.append((items[1],items[2]))
        return koordinates
        f.close()
        
    def getTitle(self,line):
        """
        Extracts just the title without row code
        @param line: one line out of the input file with type title
        @type line: string
        """
        return line[len(line.split(" ")[0]):].strip()
    
    def getTitles(self):
        """
        Collect all titles of one file into self.titles
        """
        self.titles = []
        f = open(self.inFile,"r")
        for l in f:
            items = self.parseLine(l)
            if len(items)==0:
                continue
            if items[0] in self.rowCodesTitle:
                # appends just the string after the row code
                self.titles.append(self.getTitle(l))
        f.close()
        return True
        
        
        
    def parseLine(self,line):
        """
        Splits a line into a list. The not used empty spaces are not used
        @param line: one line out of the input file with type title
        @type line: string
        """
        l = line.strip().split(" ")
        items = []
        for i in l:
            if i <> '':
                if i.isdigit():
                    i = int(i)
                items.append(i)
        return items
    
    def searchRowCode(self,rowCode):
        """
        Collects all the rows with one row code and returns them as a list
        @param rowCode: The row code
        @type rowCode: Integer 
        """
        f = open(self.inFile,"r")
        rows = []
        for l in f:
            items = self.parseLine(l)
            if len(items)==0:
                continue
            elif items[0]==rowCode:
                rows.append(items)
        f.close()
        return rows
    
    def setFiles(self,inFile,templateFile,outFile):
        """
        @param inFile: The apt.dat file from the WED
        @type inFile: string
        @param templateFile: The file which includes the definitions for the Ground traffic
        @type templateFile: string
        @param outFile: The output file
        @type outFile: string
        """
        self.inFile = inFile
        self.templateFile = templateFile
        self.outFile = outFile
        return True
        
 
#w2t = Wed2traffic(inFile,templateFile,outFile)
#w2t.extractPaths()
