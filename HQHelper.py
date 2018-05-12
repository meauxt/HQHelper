import sys
import time
import xmltodict
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import cv2
import numpy as np
import pytesseract
from PIL import Image
from googlesearch.googlesearch import GoogleSearch
import unicodedata
import lxml
import re
import time
import operator

###########################################################################################################################
# This Script will watch for file has been created in the directory you specify and then use pytesseract to convert       #
# the image to text and then search google for the question.. it will search the result and count how many time           #
# does it find the answer...                                                                                              #
#                                                                                                                         #
# This script made just for fun and right now I am manually have hard coded the value to crop the answers                 #
# and the question... to capture the screenshot am using an andriod device with ADB and running the following command     #
#           adb shell screencap -p /sdcard/screencap.png && adb pull /sdcard/screencap.png                                #
#  if you have developer mode and adb enabled on your andriod.. taking a screenshot should be simple as connecting        #
# your device to you PC and run that command.. if you have HQHelper running it will pick up the file and do the job       #
###########################################################################################################################

class HQHelper(PatternMatchingEventHandler):

    def on_created(self, event):
        self.process(event)
    def process(self, event):
            
        print("Processing....")
        print(event.src_path)
        start = time.time()
        image = Image.open( event.src_path )
        #q
        left, top, right, bottom = 56, 400, 1300, 960
        q = image.crop( ( left, top, right, bottom ) )
        #a
        left, top, right, bottom = 170, 980, 1300, 1168
        a1 = image.crop( ( left, top, right, bottom ) )
        #a2
        left, top, right, bottom = 170, 1200, 1300, 1400
        a2 = image.crop( ( left, top, right, bottom ) )
        #a3
        left, top, right, bottom = 170, 1424, 1300, 1608
        a3 = image.crop( ( left, top, right, bottom ) )

        # q.show()
        # a1.show()
        # a2.show()
        # a3.show()

        # Read image with opencv
        img = cv2.cvtColor(np.array(a3), cv2.COLOR_RGB2BGR)
        #img = cv2.imread(img_path)

        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)

        # Recognize text with tesseract for python

        q = pytesseract.image_to_string(q)
        a1 = pytesseract.image_to_string(a1)
        a2 = pytesseract.image_to_string(a2)
        a3 = pytesseract.image_to_string(a3)

        t = time.time() - start
            
        answers = [a1,a2,a3]

        text= unicodedata.normalize('NFKD', q).encode('ascii','ignore')

        print q
        start1 = time.time()
        counter = {}
        try:
            response = GoogleSearch().search(text,num_results=3)
            t = time.time() - start1
            # print("Took {} seconds to get Responds").format(t)
            start1 = time.time()

          
            for result in response.results:
                text = result.getText()
                for x in answers:
                    # for x in a.split(" "):
                    if len(x) > 1 :
                        if(x.capitalize() in text or x.lower() in text):
                            if x  in counter:
                                counter[x]= counter[x]+1
                            else:
                                counter[x]=1

                    print("**************")
                    print(dict(sorted(counter.iteritems(), key=operator.itemgetter(1), reverse=True)[:2]))
                    print("**************")
            t = time.time() - start1

        except Exception as e:

            pass

        print "------ Done -------"




if __name__=='__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(HQHelper(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
