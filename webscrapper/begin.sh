#!/bin/bash

FILE1="newpages.txt"
FILE2="go.txt"

if [ -f $FILE1 ] ; then
    rm $FILE1
fi

if [ -f $FILE2 ] ; then
    rm $FILE2
fi

scrapy crawl quotes
scrapy crawl quotes
