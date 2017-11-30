import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from skimage.transform import radon
from skimage.transform import iradon

class Scanner2DSKI:
    inputImage = None
    radonOutput = None
    iRadonOutput = None
    anglesArray = []
    fig = None
    ax1 = None


    def __init__(self, image, angArray):
        """ Make angles array and initialize radon output matrix"""
        self.inputImage = image

        self.anglesArray = angArray

        (N, M) = self.inputImage.shape
        self.radonOutput = np.zeros((N, len(self.anglesArray)), np.float32)

        self.fig, self.ax1 = plt.subplots()


    def radon2D(self):
        """ Do one pass of radon , return list of 1D values """
        (N, M) = self.inputImage.shape
        self.cleanRadonMatrix()

        angleIndex = 0
        for angle in self.anglesArray:
            theta = np.linspace(angle, angle, 1, endpoint=True)
            sinogram = radon(self.inputImage, theta=theta, circle=True)
            for pixel in range(N):
                self.radonOutput[pixel][angleIndex] = sinogram[pixel]
            angleIndex += 1
        print("The size of the radonOutputSKI: ", self.radonOutput.shape)



    def iRadon2D(self):
        """ Do one pass of radon , return list of 1D values """
        theta = np.linspace(0, 180, len(self.anglesArray), endpoint=True)
        self.iRadonOutput = iradon(self.radonOutput, theta=theta, circle=True)


    def cleanRadonMatrix(self):
        """clean radon matrix"""
        (N, M) = self.inputImage.shape
        self.radonOutput = np.zeros((N, len(self.anglesArray)), np.float32)


    def stepwiseRadon2D(self, angle):
        """ Do one pass of radon , return list of 1D values """
        theta = np.linspace(angle, angle, 1, endpoint=True)
        sinogram = radon(self.inputImage, theta=theta, circle=True)

        for pixel in range(N):
            self.radonOutput[pixel][int(angle)] = sinogram[pixel]


    def convertPassesToAngleArray(self):
        """output the angle increment as a float over 180°"""
        self.anglesArray = []
        if self.numAngles <= 0:
            self.numAngles = 1
        self.anglesArray = np.linspace(0, 180, self.numAngles, endpoint=True)


    def getAnglesArray(self):
        """return angles array"""
        return self.anglesArray


    def saveRadon2DImage(self):
        """ Save radon 2D image to file"""
        self.ax1.set_title("Radon transform\n(Sinogram)")
        self.ax1.set_xlabel("Projection angle (deg)")
        self.ax1.set_ylabel("Projection position (pixels)")
        self.ax1.imshow(self.radonOutput, cmap=plt.cm.Greys_r, extent=(0, 180, 0, self.radonOutput.shape[0]), aspect='auto')
        self.fig.savefig('radon2D_Image.png')
        self.ax1.cla()

    def saveIRadon2DImage(self):
        """ Save radon 2D image to file"""
        self.ax1.set_title("Reconstruction\nFiltered back projection")
        self.ax1.imshow(self.iRadonOutput, cmap=plt.cm.Greys_r)
        self.fig.savefig('iradon2D_Image.png')
        self.ax1.cla()