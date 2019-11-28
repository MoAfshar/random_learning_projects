import cv2
import numpy as np

## Load YOLO
network = cv2.dnn.readNet('C:\\Users\\945970\\Desktop\\YOLO\\yolov3-tiny.weights', 'C:\\Users\\945970\\Desktop\\YOLO\\yolov3-tiny.cfg')
classes = []
with open('C:\\Users\\945970\\Desktop\\YOLO\\coco.names', 'r') as f:
    ## Our object classifcation - 80 in total
    classes = [line.strip() for line in f.readlines()]

layer_names = network.getLayerNames()
## Final results of the object - with the output layers we can get the detection of the objects
output_layers = [layer_names[i[0] - 1] for i in network.getUnconnectedOutLayers()]
colours = np.random.uniform(0, 255, size=(len(classes), 3))

## Load video
## First webcam
cap = cv2.VideoCapture(0)
## Frames in real time
while True:
    _, frame = cap.read()
    height, width, channels = frame.shape

    ## Detecting objects, to be able to extreact features from this image
    blob = cv2.dnn.blobFromImage(image=frame, size=(320,320), scalefactor=(0.00392), mean=(0,0,0), swapRB=True, crop=False)
    network.setInput(blob)
    outs = network.forward(output_layers)

    ## Showing the information on the screen
    bounding_box, confidences, class_ids = [], [], []
    for out in outs:
        for detection in out:
            ## Detect the confidence
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.4:
                ## Object detected
                centre_x = int(detection[0] * width)
                centre_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                #cv2.circle(img, (centre_x, centre_y), 10, (0, 255, 0), 2)
                ## Rectangle coordinates
                x = int(centre_x - w / 2)
                y = int(centre_y - h / 2)
                #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
                bounding_box.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    num_objects_detected = len(bounding_box)
    font = cv2.FONT_HERSHEY_PLAIN
    indexes = cv2.dnn.NMSBoxes(bounding_box, confidences, 0.5, 0.4)
    for object in range(num_objects_detected):
        if object in indexes:
            x, y, w, h = bounding_box[object]
            label = str(classes[class_ids[object]])
            colour = colours[object]
            cv2.rectangle(frame, (x, y), (x+w, y+h), colour, 1)
            cv2.putText(frame, label, (x, y + 50), font, 1, colour, 2)
    ## blob for red, green, blue
    # for b in blob:
    #     for n, im in enumerate(b):
    #         cv2.imshow(str(n), im)

    cv2.imshow('Image', frame)
    ## 1 waits (1 millisecond and loop starts again)
    key = cv2.waitKey(1)
    ## Escape character
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
