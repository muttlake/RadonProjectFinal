from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
from PIL import Image, ImageTk
from PIL import *
import cv2
import numpy as np
from RadonTransform import RadonTransform
from Scanner2DSKI import Scanner2DSKI
from BackprojectRadon import BackprojectRadon


class RadonProject_UI:

    # cv2 images
    inputImage = None
    inverse_radon_Image = None

    # gui labels
    inputImageLabel = None
    radon_1D_ImageLabel = None
    radon_2D_ImageLabel = None
    scikit_radon_iradon_ImageLabel = None
    backprojection_2D_ImageLabel = None
    backprojection_Difference_ImageLabel = None

    # gui entries
    number_angles_Entry = None

    mainframe = None

    currentFilterName = ""

    # file names
    outFileInitialName = ""
    currentOutFileName = ""
    outputImage = None

    # radon variables
    radon_angles_array = None
    current_angle_index = None
    current_radon_transform = []
    N = None

    # inverse radon variables
    radon_transform_complete = False
    backprojection_matrix = []
    backprojection_image = None
    backprojectionFilter = None

    # reset for radon
    reset_for_radon = False

    # image sizes
    IMAGE_SIZE = (300, 300)
    IMAGE_SIZE_SMALL = (300, 225)
    IMAGE_SIZE_LONG = (400, 300)

    def __init__(self, master): # master means root or main window

        master.configure(background="gainsboro")

        ## ****** Main Menu ******
        menu = Menu(master)

        master.config(menu=menu)
        subMenu = Menu(menu)

        menu.add_cascade(label="File", menu=subMenu)
        subMenu.add_command(label="Exit", command=quit)

        ## ****** Set Font ******
        myLargeFont = Font(family="Arial", size=24)
        mySmallFont = Font(family="Arial", size=12)
        myStatusFont = Font(family="Courier", size=16)

        ## ****** Top Toolbar ******
        toolbar = Frame(master, bg="slate gray")

        getImageButton = Button(toolbar, text="Get Image", command=self.getInputImage)
        getImageButton.pack(side=LEFT, padx=20, pady=20)

        projectNameLabel = Label(toolbar, text = "CT Scan / Radon Project", font=myLargeFont, bg="slate gray")
        projectNameLabel.pack(side=LEFT, padx=10, pady=20)

        quitButton = Button(toolbar, text="Quit", command=quit)
        quitButton.pack(side=RIGHT, padx=20, pady=20)

        fullRadonButton = Button(toolbar, text="Run Full Scan", command=self.fullRadon)
        fullRadonButton.pack(side=RIGHT, padx=20, pady=20)

        ## ****** Number of Additional Angles between 0 and 180 Widget ******

        buttonCommitNumAngles = Button(toolbar, text="Set Angles", command=self.makeRadonAnglesArray)
        buttonCommitNumAngles.pack(side=RIGHT, padx=20, pady=20)

        self.number_angles_Entry = Entry(toolbar)
        self.number_angles_Entry.pack(side=RIGHT, padx=10, pady=20)
        self.number_angles_Entry.insert(0, '10')

        num_Angles_Label = Label(toolbar, text="Enter number angles from 0° to 180°:", font=myStatusFont, bg="slate gray")
        num_Angles_Label.pack(side=RIGHT, padx=0, pady=20)

        toolbar.pack(side=TOP, fill=X)



        ## ****** Status Bar ******
        self.statusLabel = Label(root, text="Started Project GUI", bd=1, relief=SUNKEN, anchor=W, font=myStatusFont, fg="maroon")
        self.statusLabel.pack(side=BOTTOM, fill=X)

        ## ****** Main Window Frame ******
        self.mainframe = Frame(root, bg="gainsboro")  # frame is a blank widget
        self.mainframe.pack()

        self.mainframe.columnconfigure(1, weight=1)

        ## ****** Make Right Side Arrows ******
        self.makeRightSideArrows(90) # column 0, rows 0 through 3

        ## ****** Input Image ******
        self.inputImageLabel = Label(self.mainframe)
        self.inputImageLabel.grid(row=0, column=1, columnspan=4, rowspan=4, sticky=W, padx=10, pady=30)

        ### ****** Step Radon Transform Button ******
        step_radon_Button = Button(self.mainframe, text="Transform", bd=0, highlightthickness=0, relief='ridge',
                                   command=self.stepRadon)
        step_radon_Button.grid(row=0, column=5, columnspan=1, rowspan=4, sticky=W, padx=0, pady=0)

        buttonImage = cv2.imread("greenArrow.png")
        buttonImageDisplay = self.makeDisplayImage(buttonImage, (40, 40))
        step_radon_Button.configure(image=buttonImageDisplay)
        step_radon_Button.image = buttonImageDisplay


        ## ****** Radon 1D Image ******
        self.radon_1D_ImageLabel = Label(self.mainframe)
        self.radon_1D_ImageLabel.grid(row=0, column=6, columnspan=4, rowspan=3, sticky=W, padx=50, pady=30)

        ## ****** Radon 2D Image ******
        self.radon_2D_ImageLabel = Label(self.mainframe)
        self.radon_2D_ImageLabel.grid(row=0, column=10, columnspan=4, rowspan=4, sticky=W, padx=50, pady=30)

        ## ****** Scikit Radon/Iradon Image ******
        self.scikit_radon_iradon_ImageLabel = Label(self.mainframe)
        self.scikit_radon_iradon_ImageLabel.grid(row=5, column=10, columnspan=4, rowspan=4, sticky=W, padx=50, pady=30)

        ## ****** Backprojection 2D Image ******
        self.backprojection_2D_ImageLabel = Label(self.mainframe)
        self.backprojection_2D_ImageLabel.grid(row=5, column=6, columnspan=4, rowspan=4, sticky=W, padx=50, pady=30)

        ## ****** Backprojection Difference Image ******
        self.backprojection_Difference_ImageLabel = Label(self.mainframe)
        self.backprojection_Difference_ImageLabel.grid(row=5, column=1, columnspan=4, rowspan=4, sticky=W, padx=30, pady=30)



        ## ****** Put Empty Image in Image Labels ******
        empty_image = cv2.imread("empty_image.jpg")
        empty_image_display = self.makeDisplayImage(empty_image, self.IMAGE_SIZE)

        empty_image_display_long = self.makeDisplayImage(empty_image, self.IMAGE_SIZE_LONG)

        empty_image_display_small = self.makeDisplayImage(empty_image, self.IMAGE_SIZE_SMALL)

        self.inputImageLabel.configure(image=empty_image_display)
        self.inputImageLabel.image = empty_image_display

        self.radon_1D_ImageLabel.configure(image=empty_image_display_small)
        self.radon_1D_ImageLabel.image = empty_image_display_small

        self.radon_2D_ImageLabel.configure(image=empty_image_display_long)
        self.radon_2D_ImageLabel.image = empty_image_display_long

        self.scikit_radon_iradon_ImageLabel.configure(image=empty_image_display_long)
        self.scikit_radon_iradon_ImageLabel.image = empty_image_display_long

        self.backprojection_2D_ImageLabel.configure(image=empty_image_display)
        self.backprojection_2D_ImageLabel.image = empty_image_display

        self.backprojection_Difference_ImageLabel.configure(image=empty_image_display)
        self.backprojection_Difference_ImageLabel.image = empty_image_display


        ### ****** Step IRadon Transform Button ******
        step_iradon_Button = Button(self.mainframe, text="Transform", bd=0, highlightthickness=0, relief='ridge',
                                   command=self.stepBackprojection)
        step_iradon_Button.grid(row=3, column=8, columnspan=1, rowspan=1, sticky=W, padx=0, pady=0)

        buttonImageDown = cv2.imread("greenArrowDown.png")
        buttonImageDownDisplay = self.makeDisplayImage(buttonImageDown, (40, 40))
        step_iradon_Button.configure(image=buttonImageDownDisplay)
        step_iradon_Button.image = buttonImageDownDisplay

        ## ****** Bottom Toolbar ******
        toolbarBottom = Frame(master, bg="slate gray")

        differenceButton = Button(toolbarBottom, text="Difference: Input - Backprojection",
                                  command=self.input_and_backprojection_Image_Difference)
        differenceButton.pack(side=LEFT, padx=20, pady=20)

        saveButton = Button(toolbarBottom, text="Save BP",
                                                 command=self.file_save)
        saveButton.pack(side=LEFT, padx=20, pady=20)

        postProcessBackprojectionButton = Button(toolbarBottom, text="Post-Process BP",
                                                 command=self.postProcessBackprojection)
        postProcessBackprojectionButton.pack(side=LEFT, padx=20, pady=20)

        full_backprojection_Button = Button(toolbarBottom, text="All Backprojections", command=self.allBackprojections)
        full_backprojection_Button.pack(side=LEFT, padx=20, pady=20)

        self.backprojectionFilter = StringVar(toolbarBottom)
        self.backprojectionFilter.set("Filter for Backprojections");

        backprojectionPullDown = OptionMenu(toolbarBottom, self.backprojectionFilter, "No Filter", "Ram-Lak")
        backprojectionPullDown.pack(side=LEFT, padx=20, pady=20)

        backprojectorSKIButton = Button(toolbarBottom, text="IRadon Scikit Full", command=self.getIRadonSciKit)
        backprojectorSKIButton.pack(side=RIGHT, padx=20, pady=20)

        ctScanSKIButton = Button(toolbarBottom, text="CT Scan Scikit Full", command=self.getRadonSciKit)
        ctScanSKIButton.pack(side=RIGHT, padx=20, pady=20)

        toolbarBottom.pack(side=BOTTOM, fill=X)

        # Set angles array and current Angles Index
        self.radon_angles_array = [0.0, 18.0, 36.0, 54.0, 72.0, 90.0, 108.0, 126.0, 144.0, 162.0, 180.0]
        self.current_angle_index = 0


    def getInputImage(self):
        filename = filedialog.askopenfilename()
        if filename is None:
            self.setStatus("No input image chosen")
            return

        self.outFileInitialName = self.getInitialOutputFilename(filename)

        self.inputImage = cv2.imread(filename)
        self.inputImage = cv2.cvtColor(self.inputImage, cv2.COLOR_RGB2GRAY)

        (self.N, M) = self.inputImage.shape

        self.displayImageOnLabel(self.inputImageLabel, self.inputImage, self.IMAGE_SIZE)
        self.reset_for_radon = True
        self.setStatus("Loaded input image: " + filename)



    def getInitialOutputFilename(self, filenameWithPath):
        """ Return initial output file name """
        splitString = filenameWithPath.split("/")
        lastName = splitString[len(splitString) - 1]
        fileSplitString = lastName.split(".")
        fileString = fileSplitString[0]
        if fileString == "":
            fileString = "UnknownFile"
        fileString = fileString.replace(" ", "_")
        return fileString


    def file_save(self):
        self.currentOutFileName = self.currentOutFileName.replace(".", "p")
        #print(self.currentOutFileName)
        outFileName = filedialog.asksaveasfilename(title=("Save Output Image"), initialfile=self.currentOutFileName,
                                                   defaultextension=".png")
        if outFileName is None:
            self.setStatus("No save file chosen.")
            return

        cv2.imwrite(outFileName, self.outputImage)

    def retrieveNumAngles(self):
        num_additional_angles_string = self.number_angles_Entry.get()
        num_additional_angles = 10
        angle_increment = np.float(180)/np.float(num_additional_angles)
        try:
            num_additional_angles = float(num_additional_angles_string)
            angle_increment = np.float(180)/np.float(num_additional_angles)
            self.setStatus("Setting the radon transform angle increment to " + str(angle_increment) + "°")
        except ValueError:
            self.setStatus("Setting the default radon transform angle increment to " + str(angle_increment) + "°")
        return num_additional_angles



    def setStatus(self, statusString):
        self.statusLabel.configure(text=statusString)
        self.statusLabel.text = statusString


    def displayImageOnLabel(self, label, image, image_size):
        """ Display input image on input label"""
        displayImage = self.makeDisplayImage(image, image_size)

        label.configure(image=displayImage)
        label.image = displayImage


    def makeDisplayImage(self, cv2_image, shape):
        disp_im = Image.fromarray(cv2_image)
        disp_im = disp_im.resize(shape, Image.ANTIALIAS)
        return ImageTk.PhotoImage(disp_im)


    def doNothing(self):
        print("Not implemented yet.")

    # stepwise Radon

    def stepRadon(self):
        """ Step Radon """
        if self.inputImage is None:
            self.setStatus("Please choose an input image.")
            return

        if self.reset_for_radon:
            self.current_angle_index = 0

        if self.current_angle_index == 0:
            self.current_radon_transform = np.zeros((self.N, len(self.radon_angles_array)), np.float32)
            self.radon_transform_complete = False

        CTScanner = RadonTransform(self.inputImage, self.radon_angles_array, self.current_radon_transform)

        CTScanner.get1DSinogram(self.current_angle_index)
        sinogram1DImage= cv2.imread("scanner_plot.png")
        sinogram1DImage = cv2.cvtColor(sinogram1DImage, cv2.COLOR_RGB2GRAY)

        self.current_radon_transform = CTScanner.stepwiseRadon2D(self.current_angle_index)
        radon_transf_image = CTScanner.getRadonImage()

        self.displayImageOnLabel(self.radon_1D_ImageLabel, sinogram1DImage, self.IMAGE_SIZE_SMALL)
        self.displayImageOnLabel(self.radon_2D_ImageLabel, radon_transf_image, self.IMAGE_SIZE_LONG)

        if self.current_angle_index == len(self.radon_angles_array) - 1:
            self.radon_transform_complete = True


        self.current_angle_index = (self.current_angle_index + 1) % len(self.radon_angles_array)

        if self.reset_for_radon:
            self.reset_for_radon = False

        statusString = "Ran 1D CT Scan at angle  " + str(self.radon_angles_array[self.current_angle_index - 1]) + "°"
        self.setStatus(statusString)

        self.makeRightSideArrows(self.radon_angles_array[self.current_angle_index - 1])

    # full Radon 2D

    def fullRadon(self):
        """ Step Radon """
        if self.inputImage is None:
            self.setStatus("Please choose an input image.")
            return

        if self.radon_transform_complete:
            self.setStatus("Radon Transform already complete.")
            return

        self.current_radon_transform = np.zeros((self.N, len(self.radon_angles_array)), np.float32)

        CTScanner = RadonTransform(self.inputImage, self.radon_angles_array, self.current_radon_transform)

        CTScanner.get1DSinogram(len(self.radon_angles_array) - 1)
        sinogram1DImage= cv2.imread("scanner_plot.png")
        sinogram1DImage = cv2.cvtColor(sinogram1DImage, cv2.COLOR_RGB2GRAY)

        self.current_radon_transform = CTScanner.full_Radon2D()
        radon_transf_image = CTScanner.getRadonImage()

        self.displayImageOnLabel(self.radon_1D_ImageLabel, sinogram1DImage, self.IMAGE_SIZE_SMALL)
        self.displayImageOnLabel(self.radon_2D_ImageLabel, radon_transf_image, self.IMAGE_SIZE_LONG)

        self.radon_transform_complete = True
        self.reset_for_radon = True
        self.current_angle_index = 0

        statusString = "Ran Radon for all angles."
        self.setStatus(statusString)

        self.makeRightSideArrows(self.radon_angles_array[self.current_angle_index - 1])

    # stepwise Backprojection

    def stepBackprojection(self):
        """ Step Backprojector """
        if self.inputImage is None:
            self.setStatus("Please choose an input image.")
            return

        if not self.radon_transform_complete:
            self.setStatus("Cannot backproject. Radon transform not complete.")
            return



        filterName = self.backprojectionFilter.get()
        if filterName == "Filter for Backprojections":
            filterName = "No Filter"

        if self.currentFilterName != filterName:
            self.current_angle_index = 0

        if self.current_angle_index == 0:
            (N, M) = self.inputImage.shape
            self.backProjectionMatrix = np.zeros((N * 2, M * 2), np.float32)

        Backprojector = BackprojectRadon(self.inputImage, self.radon_angles_array,
                                          self.current_radon_transform, self.backProjectionMatrix)

        backprojection1Dimage = Backprojector.get1DBackprojectionImage(self.current_angle_index, filterName)

        #self.backProjectionMatrix = Backprojector.stepwiseBackprojection(self.current_angle_index)
        self.backProjectionMatrix = Backprojector.stepwiseBackprojectionFiltered(self.current_angle_index,
                                                                                 filterName)
        self.backprojection_image = Backprojector.getBackprojectionImage()

        self.displayImageOnLabel(self.radon_1D_ImageLabel, backprojection1Dimage, self.IMAGE_SIZE_SMALL)
        self.displayImageOnLabel(self.backprojection_2D_ImageLabel, self.backprojection_image, self.IMAGE_SIZE)

        self.outputImage = self.backprojection_image
        self.currentOutFileName = self.outFileInitialName + "_StepBackProjection_filterName_AngleCount_" \
                                + str(len(self.radon_angles_array)) + " _ angleIndex_" + str(self.current_angle_index)

        self.current_angle_index = (self.current_angle_index + 1) % len(self.radon_angles_array)

        statusString = "Ran backprojection for angle  " + str(self.radon_angles_array[self.current_angle_index - 1]) + \
                       "° with filter: " + filterName
        self.setStatus(statusString)

        self.currentFilterName = filterName

        self.makeRightSideArrows(self.radon_angles_array[self.current_angle_index - 1])

    # all Backprojections

    def allBackprojections(self):
        """ Step Backprojector """
        if self.inputImage is None:
            self.setStatus("Please choose an input image.")
            return

        if not self.radon_transform_complete:
            self.setStatus("Cannot backproject. Radon transform not complete.")
            return

        if self.current_angle_index == 0:
            (N, M) = self.inputImage.shape
            self.backProjectionMatrix = np.zeros((N * 2, M * 2), np.float32)

        filterName = self.backprojectionFilter.get()
        if filterName == "Filter for Backprojections":
            filterName = "No Filter"

        Backprojector = BackprojectRadon(self.inputImage, self.radon_angles_array,
                                          self.current_radon_transform, self.backProjectionMatrix)
        self.backProjectionMatrix = Backprojector.fullBackprojectionFiltered(filterName)
        self.backprojection_image = Backprojector.getBackprojectionImage()
        self.displayImageOnLabel(self.backprojection_2D_ImageLabel, self.backprojection_image, self.IMAGE_SIZE)
        self.outputImage = self.backprojection_image

        self.current_angle_index = 0

        statusString = "Ran backprojections for all angles with filter " + filterName + " ."
        self.setStatus(statusString)

        self.currentOutFileName = self.outFileInitialName + "_FullBackProjection_" + filterName + "_AngleCount_" \
                                  + str(len(self.radon_angles_array))

        self.makeRightSideArrows(self.radon_angles_array[self.current_angle_index - 1])


    def postProcessBackprojection(self):
        """ Step Backprojector """
        if self.backprojection_image is None:
            self.setStatus("Cannot post-process image. No backprojections are complete.")
        Backprojector = BackprojectRadon(self.inputImage, self.radon_angles_array,
                                          self.current_radon_transform, self.backProjectionMatrix)
        self.backprojection_image = Backprojector.getPostProcessedBackprojectionImage(self.backprojection_image)
        self.displayImageOnLabel(self.backprojection_2D_ImageLabel, self.backprojection_image, self.IMAGE_SIZE)

        statusString = "Post-processed backprojection image."
        self.setStatus(statusString)

        self.currentOutFileName = self.currentOutFileName + "_postProcessed"

    def input_and_backprojection_Image_Difference(self):
        """ Difference between input image and backprojection image """
        if self.inputImage is None:
            self.setStatus("Please choose an input image.")
            return

        if self.backprojection_image is None:
            self.setStatus("Please do backprojections before running difference.")

        (N, M) = self.inputImage.shape
        image_diff = np.zeros((N , M), np.uint8)
        for ii in range(N):
            for jj in range(M):
                diff_value = np.abs(self.inputImage[ii][jj] - self.backprojection_image[ii][jj])
                if diff_value < 0:
                    diff_value = 0
                elif diff_value > 255:
                    diff_value = 255
                image_diff[ii][jj] = diff_value
        self.displayImageOnLabel(self.backprojection_Difference_ImageLabel, image_diff, self.IMAGE_SIZE)
        self.setStatus("Ran image difference: Input Image - Backprojection Image")

    # Scikit Radon

    def getRadonSciKit(self):
        """ Get Radon Using Scikit python radon class"""
        if self.inputImage is None:
            self.setStatus("Please choose an input image.")
            return

        Scanner2 = Scanner2DSKI(self.inputImage, self.radon_angles_array)
        Scanner2.radon2D()
        Scanner2.saveRadon2DImage()

        radon_transf = cv2.imread("radon2D_Image.png")
        radon_transf = cv2.cvtColor(radon_transf, cv2.COLOR_RGB2GRAY)
        self.displayImageOnLabel(self.scikit_radon_iradon_ImageLabel, radon_transf, self.IMAGE_SIZE_LONG)
        self.setStatus("Ran SciKit CT Scan for all Angles")

    def getIRadonSciKit(self):
        """ Get IRadon Using Scikit python radon class"""
        if self.inputImage is None:
            self.setStatus("Please choose an input image.")
            return

        Scanner2 = Scanner2DSKI(self.inputImage, self.radon_angles_array)
        Scanner2.radon2D()
        Scanner2.iRadon2D()
        Scanner2.saveIRadon2DImage()

        iradon = cv2.imread("iradon2D_Image.png")
        iradon = cv2.cvtColor(iradon, cv2.COLOR_RGB2GRAY)
        self.displayImageOnLabel(self.scikit_radon_iradon_ImageLabel, iradon, self.IMAGE_SIZE_LONG)
        self.setStatus("Ran SciKit Inverse Radon for all angles.")

    # make Angles array to pass to Radon objects

    def makeRadonAnglesArray(self):
        """output the angle increment as a float over 180°"""
        self.radon_angles_array = []
        num_angles_entered = self.retrieveNumAngles()
        self.radon_transform_complete = False

        if num_angles_entered > 0:
            angleIncrement = np.float(180)/np.float(num_angles_entered)
            currentAngle = 0.00
            while currentAngle <= 180:
                self.radon_angles_array.append(currentAngle)
                currentAngle += angleIncrement
        self.reset_for_radon = True
        print(self.radon_angles_array)


    # Below methods are for making arrows that show direction of Radon

    def rotateVector(self, vector, angle):
        angleRad = np.deg2rad(angle)
        RotationMatrix = np.matrix([[np.cos(angleRad), -1 * np.sin(angleRad)], [np.sin(angleRad), np.cos(angleRad)]])
        outputVectorDouble = RotationMatrix * vector
        (N, M) = outputVectorDouble.shape
        outputVector = np.zeros((N, M), np.int)
        for i in range(N):
            for j in range(M):
                outputVector[i][j] = np.round(outputVectorDouble[i][j])
        return outputVector

    def makeRightSideArrows(self, angle):
        vector = [[0], [15]]  ## angle 0 vector always points up
        rotated_vector = self.rotateVector(vector, angle*-1)
        newStartPointX = 25 + rotated_vector[0][0]
        newStartPointY = 25 + rotated_vector[1][0]
        newEndPointX = 25 - rotated_vector[0][0]
        newEndPointY = 25 - rotated_vector[1][0]
        for rowIndex in range(4):
            canvasA1 = Canvas(self.mainframe, width=50, height=50, bg="gainsboro", bd=0, highlightthickness=0, relief='ridge')
            canvasA1.grid(row=rowIndex, column=0, columnspan=1, rowspan=1, sticky=W, padx=0, pady=20)
            blackLine = canvasA1.create_line(newStartPointX, newStartPointY, newEndPointX, newEndPointY, tags=("line",),
                                         arrow="last", fill="black")



# start Project GUI
root = Tk()

p = RadonProject_UI(root)

root.mainloop()

