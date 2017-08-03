import linecache
import sys

import pdb

import time
#Tree_Input = open('./Tree.txt', mode='rb')

Tree_Input = sys.argv[1]
FUNC_Input = sys.argv[2]
GO_Matched = sys.argv[3]



GO_Seen = []
with open (Tree_Input,'r') as t:
    for line in t:

        if "GO" in line:

            split_line = line.split(" ")
            xCount = -1
            for x in split_line:
                xCount = xCount+1


                if "GO" in x and x not in GO_Seen:
                    GO_Seen.append(split_line[xCount])
                    lineNum = 0
                    lineDefNum = 0


                    Func_LineNum = -1
                    GO_Input = open('./go.obo', mode='rb')
                    for GOline in GO_Input:
                        lineNum = lineNum+1


                        if split_line[xCount] in GOline and "id:" in GOline:
                            lineDefNum = lineNum
                            while True:

                                #if "def" not in linecache.getline('./go.obo',lineNum+3): # Fix alt id to Def
                                if "alt_id" in linecache.getline('./go.obo',lineDefNum+3):
                                    print linecache.getline('./go.obo',lineDefNum+3)
                                    print lineDefNum

                                    lineDefNum = lineDefNum +1

                                    print lineDefNum

                                elif "def" in  linecache.getline('./go.obo',lineDefNum+3):

                                    break


                            lineNameNum = lineNum
                            if "namespace" in linecache.getline('./go.obo', lineNum + 1):

                                lineNameNum = lineNameNum + 1

                            with open(FUNC_Input,'r') as f, open(GO_Matched,'a') as out:
                                for line in f:
                                    Func_LineNum = Func_LineNum+1
                                    split = line.split(",")## , or \t
                                    if split_line[xCount] in line:
                                    	#pdb.set_trace()
                                        print split
                                        print split[8]
                                        out.write(split[0]+"    "+split_line[xCount]+"    "+linecache.getline('./go.obo',lineNameNum+1).rstrip("\r\n")+"    "+linecache.getline('./go.obo',lineDefNum+3).rstrip("\r\n")+" Enrichment Value: "+split[8]+" Enrichment Position: "+str(Func_LineNum)+"\n")
                                        print (split[0]+"    "+split_line[xCount]+"  "+linecache.getline('./go.obo',lineNameNum+1).rstrip("\r\n")+"    "+linecache.getline('./go.obo',lineDefNum+3).rstrip("\r\n")+" Enrichment Value: "+split[8]+" Enrichment Position: "+str(Func_LineNum-1)+"\n")

                            break
