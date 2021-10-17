import sys, boto3, json, cv2
import urllib.parse

AWS_KEY = urllib.parse.unquote(sys.argv[1])
capture_image = None

keys_file = "keys.json"
with open(keys_file) as file:
    var_keys = json.load(file)

s3_resource = boto3.resource('s3',aws_access_key_id=var_keys['aws_access_key_id'],aws_secret_access_key=var_keys['aws_secret_access_key'])

capture_image = None

# define a video capture object
vid = cv2.VideoCapture(0)

# Upscale the image
vid.set(cv2.CAP_PROP_BUFFERSIZE,1)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
  
def show_stream():
    global capture_image
  
    while(True):
        
        # Capture the video frame
        # by frame
        frame = vid.read()[1]

        cv2.line(frame, (419, 0), (419, 1080), (0, 255, 0), 1)
        cv2.line(frame, (1500, 0), (1500, 1080), (0, 255, 0), 1)
    
        # Display the resulting frame
        cv2.imshow('frame', frame)

        test_key = cv2.waitKeyEx(1) & 0xFF

        # if escape key pressed cancel upload
        if test_key == 27:
            sys.stdout.write("cancelled")
            exit()
        
        # If spacebar pressed capture image, show and upload to aws
        if test_key == 32:
            capture_image = frame
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

show_stream()

if capture_image is not None:
    capture_image = capture_image[0:1080,420:1500]
    capture_to_img = cv2.imencode('.jpg', capture_image)[1].tobytes()

    # Confirm Capture
    cancel_capture = False
    while True:
        # Show image for user confirmation
        cv2.putText(capture_image,"[ SPACE ] = CONTINUE / [ ESC ] = EXIT", (200,100), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
        cv2.imshow('frame', capture_image)
        
        test_key = cv2.waitKeyEx(1) & 0xFF

        # if escape key pressed cancel upload
        if test_key == 27:
            cancel_capture = True
            sys.stdout.write("cancelled")
            exit()
        
        # If spacebar pressed capture image, show and upload to aws
        if test_key == 32:
            break

    # Destroy all the windows
    cv2.destroyAllWindows()
    
    # Save image to aws using key
    s3_resource.Bucket(var_keys['bucket']).put_object(Key=AWS_KEY+".jpg", Body=capture_to_img, ACL='public-read',ContentType="image/jpeg")
    
else:
    sys.stdout.write("cancelled")
    exit()

sys.stdout.write("finished")