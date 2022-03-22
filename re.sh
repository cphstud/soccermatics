#!/bin/bash

# script to be executed in folder where jsonfiles are located
# it inserts match_id in each record
# all files must  be  imported again

ls *json | cut -d\.  -f1 > idlist
cat idlist | while read x;
do
  #sed -e '/_id/a\'$'\n''' 9.json
  sed -i '' -e '/_id/a\'$'\n'"\"match_id\":$x," $x.json
done

