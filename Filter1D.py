import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import numpy as np

class Filter1D:

    def __init__(self, values):
        self.values_list = values
        self.fig, self.ax1 = plt.subplots()

    def filter(self, filter_name):
        """ Return low pass filter of values """

        if filter_name == "No Filter":
            return self.values_list

        values_padded = self.zeroPad(self.values_list)

        fft_values = np.fft.fft(values_padded)
        fft_values_shift = np.fft.fftshift(fft_values)


        filter1 = self.ramlak_Filter(len(fft_values_shift))


        filter_fft_values = fft_values_shift * filter1  # filter here

        filter_fft_values_ifftshift = np.fft.ifftshift(filter_fft_values)
        ifft_filtered_values = np.fft.ifft(filter_fft_values_ifftshift)

        magnitude_ifft = self.int_magnitude(ifft_filtered_values)
        magnitude_ifft_shorten = magnitude_ifft[0:len(self.values_list)]



        return magnitude_ifft_shorten

    def get1DFilteredBackprojection(self, filter_name, angle):
        """ Get a single backprojection """
        filtered_values = self.filter(filter_name)
        titleString = "Backprojection Filtered values for angle: " + str(angle) + "°"
        self.ax1.set_title(titleString)
        plt.plot(filtered_values)
        self.fig.savefig('backprojection_1D_plot.png')
        self.ax1.cla()


    def int_magnitude(self, complex_values):
        """Return magnitude of complex_values"""
        magnitude_values = []
        for complex_value in complex_values:
            magnitude = int(np.round(np.sqrt(np.power(np.real(complex_value), 2) + np.power(np.imag(complex_value), 2))))
            magnitude_values.append(magnitude)
        return magnitude_values

    def findLowestPowerOf2(self):
        """Return lowest power of 2 that covers the length of values_list"""
        log_of_length = np.log2(len(self.values_list))
        log_of_length_int = int(np.ceil(log_of_length))
        return log_of_length_int

    def zeroPad(self, values):
        """ Return list of zero padded values to next largest power of 2"""
        padded_list_length = np.power(2, self.findLowestPowerOf2())
        difference_in_length = padded_list_length - len(self.values_list)
        padded_list = list(self.values_list)
        for ii in range(difference_in_length):
            padded_list.append(0)
        return padded_list

    def ramlak_Filter(self, num_points):
        """ Return ramlak filter for numpoints """
        ramlak_filter = np.ones(num_points)
        evenly_spaced_values = np.linspace(-1, 1, num_points / 4)
        abs_evenly_spaced_values = abs(evenly_spaced_values)
        for ii in range(len(abs_evenly_spaced_values)):
            ramlak_filter[ii + np.int(np.round(3*num_points/8))] = abs_evenly_spaced_values[ii]
        return ramlak_filter


    def bias_filtered_values(self, filtered_values):
        """ DC Bias Filtered Values """
        maxValue = np.max(filtered_values)
        for ii in range(len(filtered_values)):
            filtered_values[ii] += maxValue/3
        return filtered_values


    def filter_with_Printing(self, filter_name):
        """ Return low pass filter of values """
        print("Values: ", self.values_list)
        print("Values length: ", len(self.values_list))
        values_padded = self.zeroPad(self.values_list)
        print("Values padded: ", values_padded)
        print("Values_padded Length: ", len(values_padded))
        fft_values = np.fft.fft(values_padded)
        print("fft_values Values: ", fft_values)
        print("fft_values length: ", len(fft_values))
        fft_values_shift = np.fft.fftshift(fft_values)
        print("fft_values_shift Values: ", fft_values_shift)
        print("fft_values_shift length: ", len(fft_values_shift))
        filter1 = self.ramlak_Filter(len(fft_values_shift))
        print("filter1 Values: ", filter1)
        print("filter1 length: ", len(filter1))
        filter_fft_values_shift = fft_values_shift * filter1  # filter here
        print("filter_fft_values_shift Values: ", filter_fft_values_shift)
        print("filter_fft_values_shift length: ", len(filter_fft_values_shift))
        filter_fft_values_shift_ifftshift = np.fft.ifftshift(filter_fft_values_shift)
        print("filter_fft_values_shift_ifftshift Values: ", filter_fft_values_shift_ifftshift)
        print("filter_fft_values_shift_ifftshift length: ", len(filter_fft_values_shift_ifftshift))
        filter_fft_values_shift_ifftshift_ifft = np.fft.ifft(filter_fft_values_shift_ifftshift)
        print("filter_fft_values_shift_ifftshift_ifft Values: ", filter_fft_values_shift_ifftshift_ifft)
        print("filter_fft_values_shift_ifftshift_ifft length: ", len(filter_fft_values_shift_ifftshift_ifft))
        magnitude_filter_fft_values_shift_ifftshift_ifft = self.int_magnitude(filter_fft_values_shift_ifftshift_ifft)
        print("magnitude_filter_fft_values_shift_ifftshift_ifft Values: ", magnitude_filter_fft_values_shift_ifftshift_ifft)
        print("magnitude_filter_fft_values_shift_ifftshift_ifft length: ", len(magnitude_filter_fft_values_shift_ifftshift_ifft))
        magnitude_filter_fft_values_shift_ifftshift_ifft_shorten = magnitude_filter_fft_values_shift_ifftshift_ifft[0:len(self.values_list)]
        print("magnitude_filter_fft_values_shift_ifftshift_ifft_shorten Values: ", magnitude_filter_fft_values_shift_ifftshift_ifft_shorten)
        print("magnitude_filter_fft_values_shift_ifftshift_ifft_shorten length: ", len(magnitude_filter_fft_values_shift_ifftshift_ifft_shorten))
        return magnitude_filter_fft_values_shift_ifftshift_ifft_shorten





