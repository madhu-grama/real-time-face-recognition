# Platform as a Service - Image Recognition
Cloud application which provides Real-Time Face Recognition as a Service to the users by using the resources of the AWS cloud - Lambda, DynamoDB and S3.

## Group Members
Akash Dhananjaya - 1222347698
Madhu Grama Badarinarayan - 1219490987
Ullas Kalakappa Lagubagi - 1222611390

## Lambda Function - RTFaceRecognition
## S3 Bucket - image-frames-raspberry-pi
## DynamoDB Table - Student_Data

## Steps to Run the Code on Raspberry Pi
1. Install python3 on the Raspberry Pi
2. Use pip install to install cv2 and boto3 libraries
3. Execute the code rt_face_recognition.py by running the command - 'python3 rt_face_recognition.py'
4. The results of the recognized faces are displayed on the terminal

## Steps to Run the Code on Lambda
1. Include the handler.py, eval_face_recognition.py and the trained models while creating the docker image
2. Create a Lambda function using the docker image
3. Deploy the function

