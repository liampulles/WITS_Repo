# brain_undither

Requires Python 3. Please make sure your system has 8 GB of RAM or more, or I can't guarantee safe functioning.

Note that I have truncated the dataset for uploading purposes.

To train a new network, run python brain.py while in the code folder. This won't interfere with the final network, so there's no risk running it.

To undither an image, for example one in the given dataset, run while in the code folder:
python predict.py ./data/dither/2.gif

This will output the result image to ./data/dither/2.gif-out.png

Please note that this program is in a semi-finsihed state and I don't plan to develop it further.
