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

def formatline(line,p,ss):

    endpara=False
    if "Intermission" not in line:
        if "August" in line and "2012" in line:
            p.append(TEXT(line,size=32))
            endpara=True
        if "Room" in line:
            truncated=line[:-2]
            p.append(TEXT(truncated,size=12,colour=ss.Colours.Red))
        if "Presentation Time" in line:
            splitline=line.split()
            p.append(TEXT(" %s %s\n" % (splitline[-2],splitline[-1]),size=12,colour=ss.Colours.Violet))
            #endpara=True
        if "Title:" in line:
            splitline=line.split("Title:")
            p.append(TEXT("%s" % splitline[1],size=16,colour=ss.Colours.Blue))
        if "Authors:" in line:
            splitline=line.split("^M")
            splitline=splitline[0].split("Authors:")
            p.append(TEXT("%s\n\n" % splitline[1],size=14))
            endpara=True
    return(p,endpara)

def main():
    doc = Document()
    ss=doc.StyleSheet
    section=Section()
    doc.Sections.append(section)
    p=Paragraph(ss.ParagraphStyles.Normal)
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
    for line in textfile.readlines():
        p,endpara=formatline(line,p,ss)
        if endpara:
            section.append(p)
            p=Paragraph(ss.ParagraphStyles.Normal)
    DR=Renderer()
    DR.Write(doc,open("itinerary.rtf","w"))

if __name__ == '__main__' :
    main()
