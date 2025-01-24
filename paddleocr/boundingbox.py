import cv2
import numpy as np

def draw_bounding_boxes(image_path, boxes, output_path="output_image.png"):
    
    # Load the image
    image = cv2.imread(image_path)
    
    if image is None:
        print("Error: Image not found at", image_path)
        return
    
    # Iterate through the boxes and draw them
    for box, (label, score) in boxes:
        points = [(int(x), int(y)) for x, y in box]  # Convert points to integers
        
        # Draw the bounding box
        cv2.polylines(image, [np.array(points)], isClosed=True, color=(0, 255, 0), thickness=5)
        
        # Add the label and score
        if label:
            text = f"{label} ({score:.2f})"
            cv2.putText(image, text, (points[0][0], points[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    
    # Save the image
    cv2.imwrite(output_path, image)
    print("Output saved at", output_path)

# Example usage
image_path = "C:\\PES MATERIALS\\SimTech internship\\images\\page_1.png"
boxes = [
[[[172.0, 663.0], [298.0, 663.0], [298.0, 719.0], [172.0, 719.0]], ('PES', 0.9924824833869934)],
[[[189.0, 716.0], [398.0, 716.0], [398.0, 758.0], [189.0, 758.0]], ('UNIVERSITY', 0.998112678527832)],
[[[497.0, 716.0], [1163.0, 716.0], [1163.0, 789.0], [497.0, 789.0]], ('CERTIFICATE', 0.9957283139228821)],
[[[652.0, 826.0], [1038.0, 826.0], [1038.0, 867.0], [652.0, 867.0]], ('OFPARTICIPATION', 0.9936647415161133)],
[[[701.0, 931.0], [949.0, 923.0], [950.0, 964.0], [702.0, 973.0]], ('presented to', 0.9588038325309753)],
[[[676.0, 1045.0], [831.0, 1045.0], [831.0, 1089.0], [676.0, 1089.0]], ('Aditi M', 0.9596536755561829)],
[[[344.0, 1206.0], [1395.0, 1206.0], [1395.0, 1255.0], [344.0, 1255.0]], ('for his/her participation in the event "Youngicles"', 0.980847179889679)],
[[[352.0, 1269.0], [1392.0, 1267.0], [1392.0, 1316.0], [352.0, 1318.0]], ('organized by The Collegiate Social Responsibility', 0.9677744507789612)],
[[[450.0, 1325.0], [1279.0, 1328.0], [1279.0, 1377.0], [450.0, 1374.0]], ('Club of PES University,conducted from', 0.978171706199646)],
[[[590.0, 1396.0], [1146.0, 1396.0], [1146.0, 1430.0], [590.0, 1430.0]], ('29/01/2022-31/01/2022', 0.9882071614265442)],
[[[1138.0, 1503.0], [1292.0, 1509.0], [1290.0, 1553.0], [1136.0, 1547.0]], ('V.Krishna', 0.9919010996818542)],
[[[224.0, 1601.0], [573.0, 1601.0], [573.0, 1635.0], [224.0, 1635.0]], ('Dr.Vijendra Kumar SK', 0.9556004405021667)],
[[[1141.0, 1601.0], [1355.0, 1601.0], [1355.0, 1635.0], [1141.0, 1635.0]], ('Dr.V.Krishna', 0.9894821643829346)],
[[[276.0, 1649.0], [519.0, 1649.0], [519.0, 1681.0], [276.0, 1681.0]], ('Faculty Coordinator', 0.9865628480911255)],
[[[1117.0, 1649.0], [1380.0, 1649.0], [1380.0, 1681.0], [1117.0, 1681.0]], ('Dean of Student Affairs', 0.9908396005630493)],
[[[342.0, 1684.0], [455.0, 1684.0], [455.0, 1710.0], [342.0, 1710.0]], ('CSR Club', 0.9216868877410889)],
[[[1169.0, 1678.0], [1329.0, 1684.0], [1328.0, 1716.0], [1168.0, 1710.0]], ('PES University', 0.9596668481826782)],

    # Add more bounding boxes here
]
output_path = "C:\\PES MATERIALS\\SimTech internship\\output_image.png"

draw_bounding_boxes(image_path, boxes, output_path)
 