#!/usr/bin/env python
'''Created by Daniel Sindhikara, sindhikara@gmail.com
Program converts ACS text itinerary to neat rtf
    Copyright (C) 2012  Daniel J. Sindhikara

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
import sys
from PyRTF import *


class Itinerary:
    '''
Contains information for each event      
    '''
    def __init__(self):
        self.type="Presentation"# default
        self.doc=Document()
        self.ss=self.doc.StyleSheet
        self.section=Section()
        self.doc.Sections.append(self.section)

    def formatparagraph(self):
        p=Paragraph(self.ss.ParagraphStyles.Normal)
        if self.type=="Event":
            p.append(TEXT("%s - %s" % (self.starttime,self.endtime),colour=self.ss.Colours.Violet,size=16))
            p.append(TEXT(self.room[:-2],colour=self.ss.Colours.Red,size=12))
            p.append(TEXT(self.title,size=16))
            self.section.append(p)
        if self.type=="Intermission":
            pass
        if self.type=="Presentation":
            p.append(TEXT(self.starttime,colour=self.ss.Colours.Violet,size=16))
            p.append(TEXT(self.room[:-2],colour=self.ss.Colours.Red,size=12))
            p.append(TEXT(self.title,size=16,colour=self.ss.Colours.Blue))
            p.append(TEXT(self.authors,size=14))
            self.section.append(p)
        if self.type=="Date":
            p.append(TEXT(self.title,size=32))
            self.section.append(p)
        #reset everything except for room
        self.title=None
        self.type="Presentation"
    def addline(self,line):
        '''
        Incorporate new line into this class, return -1 if a new Event object should be created
        '''
        if "Event Name:" in line:
            self.type="Event"
            splitline=line.split("Event Name:")
            self.title=splitline[1]
        if "August" in line and "2012" in line:
            self.type="Date"
            self.title=line
            self.formatparagraph()
        if "Intermission" in line:
            self.type="Intermission"
            self.formatparagraph() #Don't print anything
        if "Title:" in line:
            self.title=line.split("Title:")[1]
        if "Room:" in line:
            self.room = line
            if self.type=="Event" :
                self.formatparagraph() # This is the end for Events
        if "Presentation Time:" in line:
            self.starttime=line.split("Presentation Time:")[-1]
        if "Start Time:" in line:
            self.starttime=line.split("Start Time:")[-1]
        if "End Time:" in line:
            self.endtime=line.split("End Time:")[-1]
        if "Authors:" in line:
            splitline=line.split("^M")
            splitline=splitline[0].split("Authors:")
            self.authors=splitline[1]
            self.formatparagraph() # this the  end for presentations

            
def main():
    minargs=1
    numargs=len(sys.argv)
    print '''
    cleanACSitinerary.py  Copyright (C) 2012 Daniel J. Sindhikara
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions;
    '''
    if(numargs<minargs) :
        print "# format cleanACSitinerary.py <textfile>"
    	print "Insufficient arguments, need ",minargs," : ",numargs
    	exit()
    textfile=open(sys.argv[1])
    myit=Itinerary()
    for line in textfile.readlines():
        myit.addline(line)
    DR=Renderer()
    DR.Write(myit.doc,open("itinerary.rtf","w"))

if __name__ == '__main__' :
    main()
