#!/bin/bash

echo "DONT RUN ME!!!"
return

echo "Setting up the directory for the Stegosploit Tutorial"
echo "Getting older firefox version (v37.0)"
wget https://ftp.mozilla.org/pub/firefox/releases/37.0/linux-x86_64/en-US/firefox-37.0.tar.bz2

if [ $? == 0 ]; then
	echo "Successfully got old firefox"
	echo "Extracting the tarball"
	tar -xf firefox-37.0.tar.bz2
else
	echo "Could not get the old version of firefox, download it manually from:"
	echo "https://ftp.mozilla.org/pub/firefox/releases/37.0/linux-x86_64/en-US/"
fi

echo "Getting the Stegosploit demo kit"
git clone https://github.com/Charmve/PyStegosploit.git

if [ $? == 0 ]; then
	echo "Successfully cloned the git repo"
else
	echo "Could not clone the git repo, do so manually from:"
	echo "https://github.com/Charmve/PyStegosploit"
fi

echo "Getting image to use"
wget https://upload.wikimedia.org/wikipedia/commons/5/56/Tux.jpg

if [ $? == 0 ]; then
	echo "Grabbed image successfully"
else
	echo "Unable to grab image, please download it manually from:"
	echo "https://commons.wikimedia.org/wiki/File:Tux.jpg"
fi

echo "Setting up for part 4"
wget https://media.giphy.com/media/26ufnauqqCbUhtdZu/source.gif

if [ $? == 0 ]; then
	echo "Grabbed gif successfully"
else
	echo "Unable to grab the gif. Either try again, or download your own gif to use"
fi

mkdir part4
mv source.gif part4/source.gif

touch part4/index.html
echo "<!DOCTYPE html>" >> part4/index.html
echo "<html>" >> part4/index.html
echo "<body>" >> part4/index.html
echo "<img src='source.gif'>" >> part4/index.html
echo "</body>" >> part4/index.html
echo "</html>" >> part4/index.html

echo "Done the initial set up for the tutorial"
echo "Read through to make sure everything executed properly"
echo "You will need to install hexedit if it isn't installed already"
echo "Run: sudo apt-get update"
echo "Then run: sudo apt-get install hexedit"
