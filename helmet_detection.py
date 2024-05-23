#!/usr/bin/env python
# coding: utf-8

# In[1]:


def predict(image_path):
    import numpy as np
    import os
    import cv2
    
    

    # # Data Viewing

    # In[2]:

    img0=image_path

    # for person on bike
    weights0_path = 'yolov3-obj_final.weights'
    configuration0_path = 'yolov3_pb.cfg'

    probability_minimum = 0.5
    threshold = 0.3

    # In[4]:

    network0 = cv2.dnn.readNetFromDarknet(configuration0_path, weights0_path)
    layers_names0_all = network0.getLayerNames()
    layers_names0_output = [layers_names0_all[i - 1] for i in network0.getUnconnectedOutLayers()]
    labels0 = open('coco.names').read().strip().split('\n')
    print(labels0)

    # In[5]:

    # for helmet
    weights1_path = 'yolov3-helmet.weights'
    configuration1_path = 'yolov3-helmet.cfg'

    # In[6]:

    network1 = cv2.dnn.readNetFromDarknet(configuration1_path, weights1_path)
    layers_names1_all = network1.getLayerNames()
    layers_names1_output = [layers_names1_all[i - 1] for i in network1.getUnconnectedOutLayers()]
    labels1 = open('helmet.names').read().strip().split('\n')
    print(labels1)

    # In[7]:

    image_input = cv2.imread(img0)
    blob = cv2.dnn.blobFromImage(image_input, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    blob_to_show = blob[0, :, :, :].transpose(1, 2, 0)
    network0.setInput(blob)
    network1.setInput(blob)
    output_from_network0 = network0.forward(layers_names0_output)
    output_from_network1 = network1.forward(layers_names1_output)
    np.random.seed(42)
    colours0 = np.random.randint(0, 255, size=(len(labels0), 3), dtype='uint8')
    colours1 = np.random.randint(0, 255, size=(len(labels1), 3), dtype='uint8')

    print(colours0)
    print(colours1)

    # In[8]:

    bounding_boxes0 = []
    confidences0 = []
    class_numbers0 = []

    bounding_boxes1 = []
    confidences1 = []
    class_numbers1 = []

    h, w = image_input.shape[:2]

    for result in output_from_network0:
        for detection in result:
            scores = detection[5:]
            class_current = np.argmax(scores)
            confidence_current = scores[class_current]
            if confidence_current > probability_minimum:
                box_current = detection[0:4] * np.array([w, h, w, h])
                x_center, y_center, box_width, box_height = box_current.astype('int')
                x_min = int(x_center - (box_width / 2))
                y_min = int(y_center - (box_height / 2))

                bounding_boxes0.append([x_min, y_min, int(box_width), int(box_height)])
                confidences0.append(float(confidence_current))
                class_numbers0.append(class_current)

    for result in output_from_network1:
        for detection in result:
            scores = detection[5:]
            class_current = np.argmax(scores)
            confidence_current = scores[class_current]
            if confidence_current > probability_minimum:
                box_current = detection[0:4] * np.array([w, h, w, h])
                x_center, y_center, box_width, box_height = box_current.astype('int')
                x_min = int(x_center - (box_width / 2))
                y_min = int(y_center - (box_height / 2))

                bounding_boxes1.append([x_min, y_min, int(box_width), int(box_height)])
                confidences1.append(float(confidence_current))
                class_numbers1.append(class_current)
    print(bounding_boxes0)
    print(bounding_boxes1)

    # In[9]:

    results0 = cv2.dnn.NMSBoxes(bounding_boxes0, confidences0, probability_minimum, threshold)
    # Here "cv2.dnn.NMSBoxes" this functions is used to get the non-maximum supression that means it will
    # choose that bounding box which has high confidense score.

    print("Bounding Box Paramters : ", bounding_boxes0, "\nConfindence Score :", confidences0,
          "\nProbability and threshhold value : ", probability_minimum, threshold)
    # print(results0.flattere())
    # Here "results0.flatten()" this functions is used to convert multidimentional array into 1D array.

    if len(results0) > 0:
        for i in range(len(bounding_boxes0)):
            #         print(bounding_boxes0[i][0],bounding_boxes0[i][1])
            x_min, y_min = bounding_boxes0[i][0], bounding_boxes0[i][1]
            box_width, box_height = bounding_boxes0[i][2], bounding_boxes0[i][3]
            colour_box_current = [int(j) for j in colours0[class_numbers0[i]]]
            cv2.rectangle(image_input, (x_min, y_min), (x_min + box_width, y_min + box_height), colour_box_current, 5)
            text_box_current0 = '{}: {:.4f}'.format(labels0[int(class_numbers0[i])], confidences0[i])
            cv2.putText(image_input, text_box_current0, (x_min, y_min - 7), cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                        colour_box_current, 5)

    # In[10]:

    results1 = cv2.dnn.NMSBoxes(bounding_boxes1, confidences1, probability_minimum, threshold)
    print(confidences1)
    a=""
    if (len(results1) == 0):
        a+="Person is not wearing a helmet"
    else:
        a+="Person is wearing a hemlet"
    if len(results1) > 0:
        for i in results1.flatten():
            x_min, y_min = bounding_boxes1[i][0], bounding_boxes1[i][1]
            box_width, box_height = bounding_boxes1[i][2], bounding_boxes1[i][3]
            colour_box_current = [int(j) for j in colours1[class_numbers1[i]]]
            cv2.rectangle(image_input, (x_min, y_min), (x_min + box_width, y_min + box_height), colour_box_current, 5)
            text_box_current1 = '{}: {:.4f}'.format(labels1[int(class_numbers1[i])], confidences1[i])
            cv2.putText(image_input, text_box_current1, (x_min, y_min - 7), cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                        colour_box_current, 5)

    # In[12]:

    
    image_rgb = cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB)

    
    return (image_rgb,a)






