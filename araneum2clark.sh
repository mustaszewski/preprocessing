#!/bin/sh
# Input: full Araneum corpus file 
# $ split --lines=55000000 -d pl_ar.full split/pl_ar

# Usage: $ araneum2clark.sh pl_ar.full pl_ar.clark

infile=$1
outfile=$2

cut -f 1 $infile | sed 's/<\/s>//' | sed '/^<.*>/d' | sed '/^[[:punct:]]/d' | awk ' { print tolower($0) } ' > $outfile
echo -e '\nPREPROCeSSING COMPLETED!\n'


