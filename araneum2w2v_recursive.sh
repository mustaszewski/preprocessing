#!/bin/sh
# Recursively converts all splits of the original Araneum file into the brown input format:
# Input: folder containing the full Araneum corpus split into smaller files
# $ split --lines=55000000 -d pl_ar.full split/pl_ar

# Usage: $ recursive-araneum2w2v.sh split/ araneum4w2v pl_ar.w2v

indir=$1
outdir=$2
finalname=$3
for infile in $indir*
do
	infilename=$(basename "$infile")
	outfilename="$outdir/${infilename%.*}.w2v"
	cut -f 1 $infile | sed 's/<\/s>//' | sed '/^<.*>/d' | sed '/^[[:punct:]]/d' | awk ' { print tolower($0) } ' | perl -pe 's/\n/ /g' > $outfilename
done

echo -e '\nPreprocesing completed!\nNow concatenating all single files to one large file!\n'
cat $outdir*.w2v | tr -s '[:space:]' > $finalname
echo -e '\nPREPROCeSSING COMPLETED!\n'
