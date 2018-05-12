# HQHelper
### Experimental Helper Script to solve HQ Trivia 
##### What is this ?
* This Script will watch for file has been created in the directory you specify and then use pytesseract to convert
the image to text and then search google for the question.. it will search the result and count how many time
does it find the answer... 

* This  made just for fun and right now I am manually have hard coded the value to crop the answers
and the question... to capture the screenshot am using an andriod device with ADB and running the following command
```adb shell screencap -p /sdcard/screencap.png && adb pull /sdcard/screencap.png```
* if you have developer mode and adb enabled on your andriod.. taking a screenshot should be simple as connecting 
your device to you PC and run that command.. if you have HQSolver running it will pick up the file and do the job 
##### How to use it:
* change the pixel in the script to make sure the crop being made right.(q,a1,a2,a3) and save the file
* run HQHelper on the path you will be saving the screenshot at 
``` python HQHelper.py ./ ```
* connect you andriod and use the adb to captupre the screenshots when the question appear 
```adb shell screencap -p /sdcard/screencap.png && adb pull /sdcard/screencap.png```

