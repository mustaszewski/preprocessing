#!/bin/sh
# Recursively converts all splits of the original Araneum file into the brown input format:
# Input: folder containing the full Araneum corpus split into smaller files
# $ split --lines=55000000 -d pl_ar.full split/pl_ar

# Usage: $ recursive-araneum2brown.sh split/ araneum4brown/ pl_ar.brown

indir=$1
outdir=$2
finalname=$3
for infile in $indir*
do
	infilename=$(basename "$infile")
	outfilename="$outdir/${infilename%.*}.brown"
	cut -f 1 $infile | sed 's/<\/s>//' | sed '/^<.*>/d' | sed '/^[[:punct:]]/d' | paste -sd ' ' | sed 's/  /\n/g' > $outfilename
done
echo -e '\nCleaning of corpus files and converting to oneline format completed.\nNext, sentences of less then 90% lowercase characters will be removed\n'
java -jar /home_cluster/ragerri/javacode/ixa-pipe-convert/target/ixa-pipe-convert-0.2.0.jar --brownClean $outdir
echo -e '\nPreprocesing completed!\nNow concatenating all single files to one large file!\n'
cat $outdir*.clean > $finalname
echo -e '\nPREPROCeSSING COMPLETED!\n'
