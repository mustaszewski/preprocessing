#
# prior to using this script, convert all NKJP TEI Files to simple XML:
# $ $ python3 tei2xces.py resources/NKJP_1M/ cleanedcorpus/xml/
#
# Once all XML files have been generated, you can use this script to convert the XML files to a tagged text file (.tag), tabulator-separated file (.tab) and the non-annotated plain text (.txt)
# 
# usage of this script:
# python3 xml2TagTabTxt.py cleanedcorpus/xml/ cleanedcorpus/tags/ cleanedcorpus/tab/ cleanedcorpus/txt/
#
# concatenate single tag/tab/txt files to one big file:
# $ cat cleanedcorpus/tab/*.tab > cleanedcorpus/taball.tab
#
# count lines of newly generated files
# $ wc -l cleanedcorpus/taball.tab 
#
# to create frequency list ("histogram") of uniqe tags in taball.tab:
# $ cut -f 3 cleanedcorpus/taball.tab | sort | uniq -c | sort -k 1 -nr > cleanedcorpus/tagsethistogram.txt
#
# wc -l cleanedcorpus/tagsethistogram.txt 
#
# to calculate word frequencies (unigram counts):
# $ cut -f 1 cleanedcorpus/taball.tab | sort | uniq -c | sort -k 1 -nr > cleanedcorpus/wordcount.txt
#
#to inspect the results of the tag and determine the grammatical classes accounted for each POS, run grep searches
# $ grep -P "\tppron3" cleanedcorpus/MorphosyntacticTags/Tagset_Full/taball.tab | cut -f 3 > grammarvaluesoverview.txt 
#
# Grep AGLT tags:
# $ grep -P "aglt" cleanedcorpus/tagsall.tag
#
# To execute all commands consecutively:
# $ python3 xml2TagTabTxt.py cleanedcorpus/xml/ cleanedcorpus/tags/ cleanedcorpus/tab/ cleanedcorpus/txt/ sent no 1 removeblanks && cat cleanedcorpus/tab/*.tab > cleanedcorpus/taball.tab && cat cleanedcorpus/tags/*.tag > cleanedcorpus/tagsall.tag && cat cleanedcorpus/txt/*.txt > cleanedcorpus/txtall.txt && wc -l cleanedcorpus/tagsall.tag && wc -l cleanedcorpus/taball.tab && wc -l cleanedcorpus/txtall.txt && cut -f 3 cleanedcorpus/taball.tab | sort | uniq -c | sort -k 1 -nr > cleanedcorpus/tagsethistogram.txt && wc -l cleanedcorpus/tagsethistogram.txt
#
# Look for faulty blanks
# $ egrep "[^_]*_[a-zA-Z0-9]*" /home/m9/AdvancedCorpus_FinalProject/cleanedcorpus/tags/*
# $ egrep  "(^[^_]*| [^_]*) " cleanedcorpus/tags/*.tag


import sys, os
from lxml import etree


def xml2tab(xmlfile):
	
	filename = xmlfile.split("/")[-1]
	outfilenameTab = outdirTab+filename.split(".")[0]+".tab"
	open(outfilenameTab, "w").close()
	outfileTab = open(outfilenameTab,"a")
	parser = etree.XMLParser(remove_blank_text=True) # discard whitespace nodes
	tree = etree.parse(xmlfile, parser)
	root = tree.getroot()
	for chunk in root.xpath("//chunk"):
		tabLine = ""
		if chunk.get("type") == chunksplit: # change this to == "p" if you want to segment output by paragraphs (blank line only after paragraphs)
			for token in chunk.xpath(".//tok"): # iterate over all tokens 
				for entry in token:
					if entry.tag == "orth":
						surface = entry.text
						if removeblanks == "removeblanks":
							surface = surface.replace(" ", "") # comment out if whitespaces in token are to be kept
					if entry.get("disamb"):
						base = entry.getchildren()[0].text
						ctag = entry.getchildren()[1].text
				if reductionlevel == "0":
					tabLine = surface + "\t" + ctag + "\n"
				else:
					ctagReduced = eval(reductionfunctioncall) # comment out if no tag reduction desired
					tabLine = surface + "\t" + ctagReduced + "\n" # use this line if reduction is
				outfileTab.write(tabLine)
			outfileTab.write("\n")

	outfileTab.close()

def xml2tsv(xmlfile):
	
	filename = xmlfile.split("/")[-1]
	outfilenameTsv = outdirTsv+filename.split(".")[0]+".tsv"
	open(outfilenameTsv, "w").close()
	outfileTsv = open(outfilenameTsv,"a")
	parser = etree.XMLParser(remove_blank_text=True) # discard whitespace nodes
	tree = etree.parse(xmlfile, parser)
	root = tree.getroot()
	for chunk in root.xpath("//chunk"):
		tsvLine = ""
		if chunk.get("type") == chunksplit: # change this to == "p" if you want to segment output by paragraphs (blank line only after paragraphs)
			for token in chunk.xpath(".//tok"): # iterate over all tokens 
				for entry in token:
					if entry.tag == "orth":
						surface = entry.text
						if removeblanks == "removeblanks":
							surface = surface.replace(" ", "") # comment out if whitespaces in token are to be kept
					if entry.get("disamb"):
						base = entry.getchildren()[0].text
						ctag = entry.getchildren()[1].text
				if reductionlevel == "0":
					tsvLine = surface + "\t" + ctag + "\t" + base + "\n"
				else:
					ctagReduced = eval(reductionfunctioncall) # comment out if no tag reduction desired
					tsvLine = surface + "\t" + ctagReduced + "\t" + base + "\n" # use this line if reduction is
				outfileTsv.write(tsvLine)
			outfileTsv.write("\n")

	outfileTsv.close()




def xml2txt(xmlfile):
	
	filename = xmlfile.split("/")[-1]
	outfilenameTxt = outdirTxt+filename.split(".")[0]+".txt"
	open(outfilenameTxt, "w").close()
	outfileTxt = open(outfilenameTxt,"a")

	parser = etree.XMLParser(remove_blank_text=True) # discard whitespace nodes
	tree = etree.parse(xmlfile, parser)
	root = tree.getroot()
	nospace = False
	paragraphsRaw = []

	for chunk in root.xpath("//chunk"):
		parRaw = ""
		if chunk.get("type") == chunksplit: # change this to == "p" if you want to segment output by paragraphs (1 line = 1 par)
			for token in chunk.xpath(".//tok"): # iterate over all tokens 
				for entry in token:
					if entry.tag == "orth":
						surface = entry.text
						if removeblanks == "removeblanks":
							surface = surface.replace(" ", "") # comment out if whitespaces in token are to be kept
						if not nospace:
							parRaw = parRaw +" "
						parRaw += entry.text
				siblings = token.getnext()
				if siblings is not None:
					if siblings.tag =="ns":
						nospace = True
					else:
						nospace = False
				else:
					nospace = False
			paragraphsRaw.append(parRaw.strip())
	i = 0
	for par in paragraphsRaw:
		par += "\n"
		i += 1
		outfileTxt.write(par)
		if blankline == "yes":
			if i < len(paragraphsRaw): # remove this 2 lines if 2 blank between paragraphs is desired in output
				outfileTxt.write("\n") # remove this 2 lines if 2 blank between paragraphs is desired in output
	outfileTxt.close()

def reducetags1(morphsynTag):
	tags = morphsynTag.split(":")
	pos = tags[0]

	if pos == "ppron12":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]+":"+tags[4]
	elif pos == "praet":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "winien":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "conj":
		morphsynTagReduced = pos
	elif pos == "comp":
		morphsynTagReduced = pos
	elif pos == "qub":
		morphsynTagReduced = pos
	else:
		morphsynTagReduced = morphsynTag

	return(morphsynTagReduced)

def reducetags2(morphsynTag):
	tags = morphsynTag.split(":")
	pos = tags[0]

	if pos == "ger":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]+":"+tags[4]
	elif pos == "num":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "numcol":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "ppron12":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]+":"+tags[4]
	elif pos == "ppron3":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]+":"+tags[4]
	elif pos == "praet":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "pact":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]+":"+tags[4]
	elif pos == "ppas":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]+":"+tags[4]
	elif pos == "winien":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "conj":
		morphsynTagReduced = pos
	elif pos == "comp":
		morphsynTagReduced = pos
	elif pos == "qub":
		morphsynTagReduced = pos
	elif pos == "brev":
		morphsynTagReduced = pos
	else:
		morphsynTagReduced = morphsynTag

	return(morphsynTagReduced)


def reducetags3(morphsynTag):
	tags = morphsynTag.split(":")
	pos = tags[0]

	if pos == "ger":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "num":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "numcol":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "ppron12":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "ppron3":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "praet":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "pact":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]+":"+tags[4]
	elif pos == "ppas":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]+":"+tags[4]
	elif pos == "winien":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "conj":
		morphsynTagReduced = pos
	elif pos == "comp":
		morphsynTagReduced = pos
	elif pos == "qub":
		morphsynTagReduced = pos
	elif pos == "brev":
		morphsynTagReduced = pos
	else:
		morphsynTagReduced = morphsynTag

	return(morphsynTagReduced)



def reducetags4(morphsynTag):
	tags = morphsynTag.split(":")
	pos = tags[0]

	for i in range(len(tags)): # iterate over tag to replace any occurence of m1/m2/m3 with m
		if tags[i] == "m1" or tags[i] == "m2" or tags[i] == "m3":
			tags[i] = "m"
	if pos == "ger":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "num":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "numcol":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "ppron12":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "ppron3":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "praet":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "pact":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]+":"+tags[4]
	elif pos == "ppas":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]+":"+tags[4]
	elif pos == "winien":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "conj":
		morphsynTagReduced = pos
	elif pos == "comp":
		morphsynTagReduced = pos
	elif pos == "qub":
		morphsynTagReduced = pos
	elif pos == "brev":
		morphsynTagReduced = pos
	else:
		morphsynTagReduced = ""
		for i in range(len(tags)):
			morphsynTagReduced += tags[i]+":"
		morphsynTagReduced = morphsynTagReduced.rstrip(":")
	return(morphsynTagReduced)



def reducetags5(morphsynTag):
	tags = morphsynTag.split(":")
	pos = tags[0]

	for i in range(len(tags)): # iterate over tag to replace any occurence of m1/m2/m3 with m
		if tags[i] == "m1" or tags[i] == "m2" or tags[i] == "m3":
			tags[i] = "m"
	if pos == "subst" or pos == "ger" or pos == "depr":
		pos = "noun"

	if pos == "noun":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "num":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "numcol":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]

	elif pos == "adv":
		if len(tags) > 1:
			if tags[1] == "pri" or tags[1] == "sec":
				morphsynTagReduced = pos
			else:
				morphsynTagReduced = morphsynTag
		else:
			morphsynTagReduced = morphsynTag
	elif pos == "ppron12":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "ppron3":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "praet":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "pact":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]+":"+tags[4]
	elif pos == "ppas":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]+":"+tags[4]
	elif pos == "winien":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "prep":
		morphsynTagReduced = pos+":"+tags[1]
	elif pos == "conj":
		morphsynTagReduced = pos
	elif pos == "comp":
		morphsynTagReduced = pos
	elif pos == "qub":
		morphsynTagReduced = pos
	elif pos == "brev":
		morphsynTagReduced = pos
	else:
		morphsynTagReduced = ""
		for i in range(len(tags)):
			morphsynTagReduced += tags[i]+":"
		morphsynTagReduced = morphsynTagReduced.rstrip(":")
	return(morphsynTagReduced)


def reducetags6(morphsynTag):
	tags = morphsynTag.split(":")
	pos = tags[0]

	for i in range(len(tags)): # iterate over tag to replace any occurence of m1/m2/m3 with m
		if tags[i] == "m1" or tags[i] == "m2" or tags[i] == "m3":
			tags[i] = "m"
	if pos == "subst" or pos == "ger" or pos == "depr":
		pos = "noun"

	if pos == "fin":
		if tags[3] == "imperf":
			tense = "pres"
		else:
			tense = "fut"
		morphsynTagReduced = "verbfin:"+tags[1]+":"+tags[2]+":"+tense+":"+tags[3] #+Modus
	elif pos == "bedzie":
		tense = "fut"
		morphsynTagReduced = "verbfin:"+tags[1]+":"+tags[2]+":"+tense+":"+tags[3] #+MODUS
	elif pos == "praet":
		tense = "past"
		morphsynTagReduced = "verbfin:"+tags[1]+":"+tags[2]+":"+tense+":"+tags[3]
	elif pos == "impt":
		mode = "imp"
		if tags[3] == "imperf":
			tense = "pres"
		else:
			tense = "fut"
		morphsynTagReduced = "verbfin:"+tags[1]+":"+tags[2]+":"+tense+":"+tags[3]+":"+mode
	elif pos == "noun":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "num":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "numcol":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "adv":
		if len(tags) > 1:
			if tags[1] == "pri" or tags[1] == "sec":
				morphsynTagReduced = pos
			else:
				morphsynTagReduced = morphsynTag
		else:
			morphsynTagReduced = morphsynTag
	elif pos == "ppron12":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "ppron3":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "praet":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "pact":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]+":"+tags[4]
	elif pos == "ppas":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]+":"+tags[4]
	elif pos == "winien":
		morphsynTagReduced = pos+":"+tags[1]+":"+tags[2]+":"+tags[3]
	elif pos == "prep":
		morphsynTagReduced = pos+":"+tags[1]
	elif pos == "conj":
		morphsynTagReduced = pos
	elif pos == "comp":
		morphsynTagReduced = pos
	elif pos == "qub":
		morphsynTagReduced = pos
	elif pos == "brev":
		morphsynTagReduced = pos
	else:
		morphsynTagReduced = ""
		for i in range(len(tags)):
			morphsynTagReduced += tags[i]+":"
		morphsynTagReduced = morphsynTagReduced.rstrip(":")
	return(morphsynTagReduced)




def reducetags7(morphsynTag):
	tags = morphsynTag.split(":")
	pos = tags[0]
	morphsynTagReduced = pos
	return(morphsynTagReduced)



if len(sys.argv) != 9:
    print ("Usage: python3 " + sys.argv[0] + " inputdir_xml outputdir_tab outputdir_tsv outputdir_txt par|sent addBlankLineInTxtAfterSent {yes|no} reductionstep removeblanks|keepblanks")
    exit(1)

indir = sys.argv[1]
outdirTab = sys.argv[2]
outdirTsv = sys.argv[3]
outdirTxt = sys.argv[4]
chunksplit = sys.argv[5]
if chunksplit == "par":
	chunksplit = "p"
else:
	chunksplit = "s"
blankline = sys.argv[6]
reductionlevel = sys.argv[7]
reductionfunctioncall = "reducetags"+reductionlevel+"(ctag)"
removeblanks = sys.argv[8]
#addfinalpunctuation = sys.argv[9]



unprocessed=[]

filelist = os.listdir(indir)
size = len(filelist)
print("\n\tProcessing %s XML-files"%(size))
counter = 1
for fl in filelist:
	xmlfile = indir+fl
	if os.path.exists(xmlfile):
		xml2tab(xmlfile)
		xml2tsv(xmlfile)
		xml2txt(xmlfile)
	else:
		unprocessed.append(xmlfile)
	progress = int((counter/size)*100)
	statusbar = int(progress/2)
	sys.stdout.write("\r")
	sys.stdout.write("\t["+"="*statusbar+" "*(50-statusbar)+"]"+"\t"+str(progress)+" %")
	counter +=1


unprocessedLog = open("logs/unprocessed.txt","w")
unprocessedLog.write(str(unprocessed))
unprocessedLog.close()
print("\n\n\tConversion of XML to Tags/Tab/Raw Completed!\n\n")
print("\t%s folders have not been processed.\n\tLog of unproccesed files saved to unprocessedLog.txt\n" %(len(unprocessed)))


#filename = "WilkWilczy.xml"
#ml2tab(filename)
