from tkinter import image_types
import cv2
import os
import time
import boto3
import base64
import threading
import json
import sys


input_s3_bucket = 'image-frames-raspberry-pi'

s3_bucket = boto3.client('s3', region_name='us-east-1', aws_access_key_id= 'XXXXXXXXXXXXXXXXXXXXXXX', aws_secret_access_key= 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
lambda_client = boto3.client('lambda', region_name='us-east-1', aws_access_key_id= 'XXXXXXXXXXXXXXXXXXXXXXX', aws_secret_access_key= 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

time_array = []
image_array = []

def video_to_frames(image_limit):
    directory = r'/home/pi/Pictures/Frames/'
    os.chdir(directory)
    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 30.0, (640,480))
    image_counter=0
    frame_counter=0

    while(cap.isOpened()):
        ret, frame = cap.read()

        # This condition prevents from infinite looping
        # incase video ends.
        if ret == False or image_counter >= image_limit:
            break

        #write the frame into the video
        out.write(frame)
        if(frame_counter % 15 == 0):
            frame = frame[80:560, 0:480]
            frame = cv2.resize(frame, (160,160))
            image_name = 'Frame'+str(image_counter+1)+'.png'
            image_array.append(image_name)
            cv2.imwrite(image_name, frame)
            image_counter += 1
        frame_counter += 1
        if cv2.waitKey(1) & 0xFF==27:
            break
    cap.release()
    cv2.destroyAllWindows()
    s3_bucket.upload_file('/home/pi/Pictures/Frames/output.avi', input_s3_bucket, 'output.avi')

def lambda_helper():
    count = 0
    ut = []
    while(1):
        if(len(image_array) > 4):
            count = 0
            for k in range(5):
                name = image_array.pop(0)
                ut.append(threading.Thread(target=lambda_helper_thread, args=(name,)))
                ut[k].start()
            for k in range(5):
                ut[k].join()
            ut = []
        else:
            count += 1
            time.sleep(3)
        if(count == 3):
            break


def lambda_helper_thread(name):
    if(name != ''):
        with open(name, "rb") as image2string:
            converted_string = base64.b64encode(image2string.read()).decode('utf-8')
        input = {
            'name': name,
            'byte' : converted_string
        }
        start_time = time.time()
        response = lambda_client.invoke(FunctionName= 'RTFaceRecognition',
                    InvocationType='RequestResponse',
                    Payload= json.dumps(input))
                
        t = response['Payload'].read().decode('utf-8').replace(']','')
        t = t.replace(',', '", "')
        person_num = name.replace('Frame','')
        person_num = person_num.replace('.png','')
        end_time = time.time() - start_time
        print('\nPerson: '+person_num+'\n'+t.replace('[','')+'\n Latency: '+str("{:.2f}".format(end_time))+' seconds')


if __name__ == "__main__":
    # creating thread
    t1 = threading.Thread(target=video_to_frames, args=(int(sys.argv[1]),))
    
    # starting thread 1
    t1.start()
    
    lambda_helper()
    
    # wait until thread 1 is completely executed
    t1.join()
    
    print("Done!")