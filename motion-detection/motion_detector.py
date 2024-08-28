import cv2 as cv
import numpy as np
import argparse
from draw_bounding_box import getBoundingBox

def sharpenFrame(cur_frame):

   # From colour images creating a gray frame 

    gray_image = cv.cvtColor(cur_frame, cv.COLOR_BGR2GRAY)

    # Apply sharpening filter
    if(mode == 3 or mode == 4):
        kernel = np.array([[-1, -1, -1],
                        [-1, 9, -1],
                        [-1, -1, -1]])
        
        gray_image = cv.filter2D(gray_image, -1, kernel)

    # Apply blur filter

    if(mode == 2):
        gray_image = cv.GaussianBlur(gray_image, (11, 11), 0)    

    return gray_image





# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Motion detection")

# Add command-line arguments with help messages
parser.add_argument(
    '-v',
    '--video_path',
    type=str,
    default="",
    help="Path to the video file"
)
parser.add_argument(
    '-m',
    '--mode',
    type=int,
    default=3,
    help="modes: 1 -> plain , 2-> apply blur kernel, 3-> apply sharpen kernel, 4 -> sharp + blur, default: 3"
)

parser.add_argument(
    '-th',
    '--threshold',
    type=int,
    default=60,
    help="Threshold for frame difference"
)
# Parse the command-line arguments
args = parser.parse_args()

# Access the values of the arguments
video_path = args.video_path
mode = args.mode
threshold = args.threshold

# Now you have the user's string and integer arguments
print("Video path:", video_path)

x1, y1, x2, y2 = -1, -1, -1, -1

initialState = None  

# LEARNING_RATE = -1   
# fgbg = cv.createBackgroundSubtractorMOG2()


# Read other frames and compare to the initial state
no_of_video_loop = 4

loop_count = 0

while(loop_count < no_of_video_loop):
    video = cv.VideoCapture(video_path)
    _,first_frame = video.read()
    # first_frame = first_frame[2:55, 1153:1230]
    initialState = sharpenFrame(first_frame) 
    var_motion = 0
    print(loop_count)
    loop_count = loop_count + 1

    if(x1 == -1):
        x1, y1, x2, y2 = getBoundingBox(first_frame)
        print("final coordinates: ",x1,y1,x2,y2)
        
    initialState = initialState[y1:y2, x1:x2]
    while True:
        

        check,cur_frame = video.read()


        # Check if the frame was successfully read
        if not check:
            print("End of video")
            video.release()
            break

        # Check if the frame is empty or invalid
        if cur_frame is None:
            print("Invalid frame")
            continue

        cut_frame = cur_frame[y1:y2, x1:x2]
        gray_image = sharpenFrame(cut_frame)
       
        differ_frame = cv.absdiff(initialState, gray_image)  
        thresh_frame = cv.threshold(differ_frame, threshold, 255, cv.THRESH_BINARY)[1]  
        thresh_frame = cv.dilate(thresh_frame, None, iterations = 2)  

        # motion_mask = fgbg.apply(gray_image, LEARNING_RATE)
        #Get background
        # background = fgbg.getBackgroundImage()
        cont,_ = cv.findContours(thresh_frame.copy(),cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  

    
        # Get bounding box co-ordinates of the contour around vibration

        for cur in cont:  

            if cv.contourArea(cur) < 500:  

                continue             

            (cur_x, cur_y,cur_w, cur_h) = cv.boundingRect(cur)  

            # cv.rectangle(cut_frame, (cur_x+1153, cur_y+2), (cur_x + 1153 + cur_w , cur_y + cur_h + 2 ), (0, 255, 0), 3)  
            cv.rectangle(cur_frame, (cur_x + x1, cur_y + y1), (cur_x + x1 + cur_w , cur_y + y1 + cur_h), (0, 255, 0), 3)  

    
        # Gray scale image
        # cv.imshow("The image captured in the Gray Frame is shown below: ", gray_image)  

    

        # To display the difference between inital static frame and the current frame 

        cv.imshow("Difference b/w first frame(background) and the current frame", differ_frame)  

        # Motion mask  

        cv.imshow("Threshold mask / Motion mask: ", thresh_frame)  

        cv.imshow("Current frame:", cur_frame)  

    # Creating a key to wait  

        wait_key = cv.waitKey(1)  

        if wait_key == ord('m'):   # m key stops the loop

            video.release()
            break 
  
# Releasing the video   
video.release()  
cv.destroyAllWindows()




   



       
    