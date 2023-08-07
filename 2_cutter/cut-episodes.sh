#!/bin/bash
# Script to cut initial and ending part of a set of mp3 files.

INPUT_PATH="../output/episodes-original"
OUTPUT_PATH="../output/episodes-cut"

start_timestamp=17
end_margin=7

OIFS="$IFS"
IFS=$'\n'
for f in $(ls $INPUT_PATH)
do
    src_path="$INPUT_PATH/$f"
    dst_path="$OUTPUT_PATH/$f"
    if [ ! -f $dst_path ]; then
        echo "Processing: $src_path --> $dst_path"
        end_timestamp=$(($(mp3info -p "%S\n" "$src_path") -$end_margin))
        ffmpeg -i "$src_path" -vn -acodec copy -ss 00:00:$start_timestamp -to $end_timestamp "$dst_path" 2>&1 > /dev/null
    fi
done
IFS="$OIFS"