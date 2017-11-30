CT Scan / Radon Project
Timothy Shepard
1519265

Summary
	The Radon transform computes the integral along rays through an image.  To implement this in a straightforward way, I rotated the image through different angles and summed along columns.  For back-projecting the Radon transform sinogram, I added the values of each radon transform to a blank image cumulatively, rotating the image each time.  Simple back-projection caused a blurred image.  Filtering the image took out low frequencies but left a dark image.
	The Radon transform simulates a CT Scan by simulating the parallel x-rays passing through a phantom.  In testing my own implementation of the Radon transform and back-projections, I found that one must include angles ranging from 0° to 180° and that more angle gives a better back-projection image.  Another finding is that the filter before back-projection is important to take out blurring by simple-backprojections.


References
http://biomedicalsignalandimage.blogspot.com/2016/02/matlab-code-to-perform-tomographic.html

