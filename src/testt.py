import mss
import numpy as np
from PIL import Image
from time import perf_counter

with mss.mss() as sct:
    start_time = perf_counter()
    # Define the regions of interest for each monitor
    monitor1 = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    monitor2 = {"top": 0, "left": 1920, "width": 1280, "height": 1080}

    # Calculate the capture region for the combined image
    capture_left = 0
    capture_top = 0
    capture_width = 2500
    capture_height = 1080

    # Capture the region of interest for each monitor
    img1 = np.array(sct.grab(monitor1))
    img2 = np.array(sct.grab(monitor2))

    # Crop the captured images to the region of interest
    img1_crop = img1[capture_top:capture_top+capture_height, capture_left:capture_left+monitor1['width']]
    img2_crop = img2[capture_top:capture_top+capture_height, :capture_width-monitor1['width']]
    
    # Combine the images into a single screenshot
    combined_img = np.concatenate((img1_crop, img2_crop), axis=1)
    print(f"Time taken: {perf_counter() - start_time}")

    # Convert the numpy array to a PIL image and save it to a file
    Image.fromarray(combined_img).save("combined_screenshot.png")

