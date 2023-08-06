# Extracts a part of the image specified by width and height from the given image file path using OpenCV.

## pip install getpartofimg 

#### Tested against Windows 10 / Python 3.10 / Anaconda 

Parameters:
-----------
image : Any
	The file path of the image from which a part will be extracted.

width : int
	The desired width of the extracted part.

height : int
	The desired height of the extracted part.

allow_resize : bool, optional (default=True)
	If True, allows resizing of the input image when the specified width or height is greater
	than the original image's dimensions.

Returns:
--------
numpy.ndarray
	The extracted part of the image as a NumPy array.

Raises:
-------
ValueError
	If the 'allow_resize' parameter is set to False and the specified width or height is greater than
	the original image's dimensions, a ValueError is raised with a message indicating that the image is too small.

Notes:
------
The function uses the 'cv2.imread_plus' function ( https://github.com/hansalemaos/a_cv_imwrite_imread_plus )
to read the image from the given file path. It then calculates
the possible ranges for extracting the desired part based on the image's dimensions and the specified width
and height. If the 'allow_resize' parameter is True, the function resizes the image using 'cv2.easy_resize_image'
( https://github.com/hansalemaos/a_cv2_easy_resize )
with the 'cv2.INTER_AREA' interpolation method to fit the desired part. Otherwise, it raises a ValueError.

Random starting coordinates within the allowable range are generated to extract the part of the image specified
by the given width and height.



```python
# Example usage:
import cv2
from getpartofimg import get_part_of_image
im = get_part_of_image(image=r"https://raw.githubusercontent.com/hansalemaos/screenshots/main/pic5.png", width=600, height=500, allow_resize=True)
cv2.imwrite('c:\\testimage.png', im)


```