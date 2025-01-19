!#/bin/zsh

for img in images-orig/*; do
  magick convert "$img" \
    -define webp:method=6 \
    -sampling-factor 4:2:0 \
    -strip \
    -quality 85 \
    -interlace Plane \
    -gaussian-blur 0.05 \
    "images/$(basename "${img%.*}").webp"
done
