#!/bin/bash

FILE1="osVersion.txt"
FILE2="applicationList.txt"
if [ -f $FILE1 ] ; then
    rm $FILE1
fi

if [ -f $FILE2 ] ; then
    rm $FILE2
fi

cat lsb_release -a > osVersion.txt
cat apt list > applicationList.txt
