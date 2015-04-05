#!/usr/bin/python
#Allows compatibility with any version of Python by checking for both versions of Tkinter
try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import base64


class UI(Tk):
    def initialize(self):
        #Handles setting up most of the GUI
        w = 500;#Window width
        h = 500;#Window height
        sw = self.winfo_screenwidth();#Gets screen width
        sh = self.winfo_screenheight();#Gets screen height
        x=(sw-w)/2;#Calculates the x position for the left side of the window that allows it to be placed in the center of the screen
        y =(sh-h)/2;#Calculates the y position for the top of the window that allows it to be placed in the center of the screen
        self.update();#Forces and update on the window
        self.geometry('%dx%d+%d+%d' % (w,h,x,y));#Sets the windows width, height and position
        self.minsize(int(w),int(h/2));#Sets the minimum size of the window
        
        self.columnconfigure(0,weight=1);#Configure all used columns to automaticly resize
        self.columnconfigure(1,weight=1);
        self.rowconfigure(1,weight=1);#Configures the row uesd for the text area to automaticly resize
        
        self.title("Decoder");#Sets the title
        self.grid();#Sets the layout to use grid
        
        Label(self,padx=2,text="Enter String").grid(row=0,column=0,sticky='E'+'W');#Setup and place the entry label
        self.entry = Entry(self);#Setup the entry box
        self.entry.grid(column=1,row=0,sticky='E'+'W');#Place the entry box


        self.configureOutput()
        self.setupButtons();
    def configureOutput(self):
        self.output = Text(self);#Setup the text area
        self.output.grid(column=0,row=1,sticky='E'+'W'+'N'+'S',columnspan=5);#Place the text area, spanning 4 columns
        self.output.insert('end',"Output\n");#Add some testing text to the text area
        self.output.configure(state='disabled');#Disable the text area
    def setupButtons(self):
        #Handles creating and setting up all the buttons
        calculateButton= Button(self, text="Decode", command=self.decode)
        calculateButton.grid(column=4,row=0,sticky='E'+'W')
    def decode(self):
        result = []
        entry = self.entry.get()
        entry = base64.b64decode(entry) #Uses pythons base64 module to decode the base64 string
        for byte in entry:
            bits = bin(byte)[2:] #Converts unicode to binary and removes the first 2 irrelevant .
            bits = '00000000'[len(bits):]+bits #8 emtpy bits for a byte, removes amount equal to the bits generated last line then appends those bits
            result.extend([int(b) for b in bits]) #Extends the array and adds each bit in the byte as a seperate array entry
        resultrev = []
        for i in range(len(result)): #Reverse the bits by starting at the end of result and appending to resultrev
            resultrev.append(result[ len(result)-i-1]) #Append the current bit from the results array to the end of the resultsrev array
        outputString = ""
        for byte in range(int(len(resultrev)/8)): #Working in bytes while the array is in bits so we need to divide the length of the array by 8
            Byte = resultrev[byte*8:(byte+1)*8] #Gets the current working byte
            unicode = 0
            for b in range(len(Byte)): #For each byte run thourgh 8 times
                unicode += int(Byte[len(Byte)-b-1]*pow(2,b)) #And convert each bit from right to left to a base 10 number
            outputString += (chr(unicode)) #Then convert the int generated to a character and append it to the string
        self.output.configure(state='normal')#Then output the final string to the python output after turning it on and clearing it
        self.output.delete(1.0,'end');
        self.output.insert('end', outputString)
        self.output.configure(state='disabled') #Final disable the output
    def __init__(self):
    #Handles the initial call to create a GUI
       parent = '';
       Tk.__init__(self,parent);#Parent constructor
       self.parent = parent;#Store the parent
       self.initialize();#Initilize the GUI
       self.mainloop();#Start the main loop

if __name__ == "__main__":
    import sys
    main = UI();
