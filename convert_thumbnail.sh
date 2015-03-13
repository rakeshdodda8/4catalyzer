#!/bin/bash -ex
image_path=$1
image=$(basename $image_path)
dest_filename=$(echo $image |awk -F"." '{print $1}')
path=$(pwd)
mkdir -p $path/templates/media/thumbnails 
convert -resize 10% $image_path $path/templates/media/thumbnails/${dest_filename}.png
