import requests
from datetime import datetime
import time
import cv2
import numpy as np
import base64


RADAR_IMG = "https://weather.bangkok.go.th/Images/Radar/radar.jpg"
IMG_PATH = "radar_img/"


REFRESH_INTERVAL = 5

RADAR_INTENSITY_LOW  = {"min": [40, 100, 100], "max": [70, 255, 255]}  #Colour intensity for 9.5 - 29.0 dBz
RADAR_INTENSITY_MID  = {"min": [16, 100, 100], "max": [39, 255, 255]}  #Colour intensity for 29.0 - 44.0 dBz
RADAR_INTENSITY_HIGH  = {"min": [140, 100, 100], "max": [15, 255, 255]}  #Colour intensity for 9.5 - 29.0 dBz

start_x = 240
end_x = start_x+300
start_y = 360
end_y = start_y+200

last_notify_time = None
last_notify_percent = None


def get_radar_image():
    response = requests.get(RADAR_IMG)
    now = datetime.now() # current date and time
    filename = now.strftime("radar_%Y_%m_%d_%H_%M_%S")
    # open(f"{IMG_PATH}{filename}.jpg", "wb").write(response.content)
    arr = np.asarray(bytearray(response.content), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)

    return img

def get_dbz_mask(img, radar_intensity):
    # It converts the BGR color space of image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
      
    # Threshold in HSV space
        
    if (radar_intensity["min"][0] > radar_intensity["max"][0]):
        lower_1 = np.array(radar_intensity["min"])
        upper_1 = np.array([180, radar_intensity["max"][1], radar_intensity["max"][2]])
        mask_1 = cv2.inRange(hsv, lower_1, upper_1)
        
        lower_2 = np.array([0, radar_intensity["min"][1], radar_intensity["min"][2]])
        upper_2 = np.array(radar_intensity["max"])
        
        mask_2 = cv2.inRange(hsv, lower_2, upper_2)
        mask = mask_1 + mask_2   

    else:
        lower_1 = np.array(radar_intensity["min"])
        upper_1 = np.array(radar_intensity["max"])
        mask = cv2.inRange(hsv, lower_1, upper_1)
 


    # cv2.imshow('result', result)

    return mask
      
def get_white_percentage(image):
    width, height = image.shape
    size = width*height
    white_area = cv2.countNonZero(image)
    print(f"w area = {white_area}")

    return (white_area/size) *100


def get_clouds_percentage(save_image = True):

    img = get_radar_image()
    # img = cv2.imread('radar_img/radar_2023_07_27_00_45_53.jpg')

    mask = get_dbz_mask(img, RADAR_INTENSITY_LOW)
    mask += get_dbz_mask(img, RADAR_INTENSITY_MID)
    mask += get_dbz_mask(img, RADAR_INTENSITY_HIGH)
    clouds_area = cv2.bitwise_and(img, img, mask = mask)

    mask_cropped = mask[start_y:end_y, start_x:end_x] #Cropped area


    clouds_percent = get_white_percentage(mask_cropped)
    print(f"Clouds percentage = {clouds_percent:.1f}%")

    img = cv2.rectangle(img, (start_x,start_y), (end_x,end_y), (0,255,0), 2)
    img = cv2.putText(img, f"Clouds = {clouds_percent:.1f}%",(400,50), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    # cv2.imshow('frame', img)
    # cv2.imshow('clouds_area', clouds_area)
    # cv2.waitKey(0)
    cv2.imwrite(f"radar_tmp.jpg", img)

    if (save_image):
        now = datetime.now() # current date and time
        filename = now.strftime("radar_%Y_%m_%d_%H_%M_%S")
        cv2.imwrite(f"{IMG_PATH}{filename}_radar.jpg", img)
        cv2.imwrite(f"{IMG_PATH}{filename}_segmented.jpg",clouds_area)

    return clouds_percent


if __name__ == "__main__":
    get_clouds_percentage()

# while(1):
#     get_clouds_percentage()
#     time.sleep(60*REFRESH_INTERVAL)
