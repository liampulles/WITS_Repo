#!/bin/bash

# Arguments:
# %1: Video file 

rm -r frames
mkdir frames
ffmpeg -i "$1" -vf "format=gray" frames/out-%03d.jpg & \
ffprobe -show_frames -print_format csv -f lavfi "movie=$1,select=gt(scene\,0.3)" > timecodes.txt

#rm -r frames-scaled
#mkdir frames-scaled
#for f in frames/*
#do
#  b=$(basename "$f")
#  convert "$f" -colorspace Gray -resize 64x64\! frames-scaled/"$b".gif
#done

rm frames.txt
fps=$(ffprobe -v 0 -of compact=p=0 -select_streams 0 -show_entries stream=r_frame_rate "$1" | cut -d "=" -f 2)
while read p; do
  b=$(echo "$p" | cut -d "," -f 6)
  echo "($b * ($fps)) / 1" | bc >> frames.txt
done <timecodes.txt

echo "Done!"