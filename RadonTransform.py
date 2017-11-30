import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import numpy as np
from CTScan import CTScan


class RadonTransform:
    """ Do Radon Transform """

    def __init__(self, image, angles_array, current_radon_transform):
        self.inputImage = image # cv2 image
        self.fig, self.ax1 = plt.subplots()

        self.radon_angles_array = angles_array
        self.radonOutput = current_radon_transform

        angleCount = len(self.radon_angles_array)
        (N, M) = self.inputImage.shape
        self.radonImage = np.zeros((N, angleCount), np.uint8)


    def get1DSinogram(self, angleIndex):
        """ Get a single sinogram for CT """
        ctScan = CTScan(self.inputImage)
        angle = self.radon_angles_array[angleIndex]
        values = ctScan.onePassRadon(angle)
        titleString = "1D Sinogram at Angle: " + str(angle) + "°"
        self.ax1.set_title(titleString)
        plt.plot(values)
        self.fig.savefig('scanner_plot.png')
        self.ax1.cla()


    # stepwise 2D Radon

    def stepwiseRadon2D(self, angleIndex):
        """ Do one pass of radon , return list of 1D values """
        CT = CTScan(self.inputImage)
        angle = self.radon_angles_array[angleIndex]
        values = CT.onePassRadon(angle)
        valueIndex = 0
        valueCount = len(values)
        for value in values:
            self.radonOutput[valueCount - valueIndex - 1][angleIndex] = values[valueIndex]
            valueIndex += 1
        #print("The size of the current 2D Radon Transform: ", self.radonOutput.shape)
        return self.radonOutput

    # full 2D Radon

    def full_Radon2D(self):
        """ Do one pass of radon , return list of 1D values """
        angle_index = 0
        CT = CTScan(self.inputImage)
        for angle in self.radon_angles_array:
            values = CT.onePassRadon(angle)
            valueIndex = 0
            valueCount = len(values)
            for value in values:
                self.radonOutput[valueCount - valueIndex - 1][angle_index] = values[valueIndex]
                valueIndex += 1
            angle_index += 1
        #print("Ran full radon2D. The size of the current 2D Radon Transform: ", self.radonOutput.shape)
        return self.radonOutput


    # functions for getting the radon image
    def getRadonImage(self):
        """ return uint8 radon image"""
        maxValue = self.getMaxRadonValue(self.radonOutput)
        (N, M) = self.radonOutput.shape
        for row in range(N):
            for col in range(M):
                image_value = self.radonOutput[row][col]/maxValue * 255
                self.radonImage[row][col] = np.round(image_value)
        return self.radonImage


    def getMaxRadonValue(self, current_radon_transform):
        """ Get Max Radon Value for image scaling """
        maxValue = -1
        (N, M) = current_radon_transform.shape
        for row in range(N):
            for col in range(M):
                if current_radon_transform[row][col] > maxValue:
                    maxValue = current_radon_transform[row][col]
        return maxValue