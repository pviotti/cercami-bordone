#!/bin/bash
# Script to cut initial and ending part of a set of mp3 files.

start_timestamp=17
end_margin=7

OIFS="$IFS"
IFS=$'\n'
for f in $(ls ./episodes-original)
do
    src_path="./episodes-original/$f"
    dst_path="./episodes-cut/$f"
    echo "Processing: $src_path --> $dst_path"
    end_timestamp=$(($(mp3info -p "%S\n" "$src_path") -$end_margin))
    ffmpeg -i "$src_path" -vn -acodec copy -ss 00:00:$start_timestamp -to $end_timestamp "$dst_path" 2>&1 > /dev/null
done
IFS="$OIFS"