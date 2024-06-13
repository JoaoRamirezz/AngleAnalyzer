import cv2
import numpy as np
from PIL import Image
from Backend.ConfigJson import ConfigJson
import ast

#region AUXILIAR FUNCTIONS

def find_final_point(significant_point, centerPoint, image):
    vector = np.array(significant_point) - np.array(centerPoint)
    vector = vector / np.linalg.norm(vector)

    height, width = image.shape[:2]
    if abs(vector[0]) > abs(vector[1]):
        end_x = width if vector[0] > 0 else 0
        end_y = centerPoint[1] + int((end_x - centerPoint[0]) * vector[1] / vector[0])
    else:
        end_y = height if vector[1] > 0 else 0
        end_x = centerPoint[0] + int((end_y - centerPoint[1]) * vector[0] / vector[1])

    end_point = (end_x, end_y)
    return end_point

def mid_point(point1, point2):
    x_mid = (point1[0] + point2[0]) / 2
    y_mid = (point1[1] + point2[1]) / 2
    return (int(x_mid), int(y_mid))

def are_points_close(point, all):
    for p in all:
        if euclidean_distance(p, point) < 20:
            all.remove(p)
            return all
        
    all.append(point)
    return all

def euclidean_distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

def find_furthest_points(points):
    max_distance = 0
    furthest_pair = (None, None)
    
    # Calcular a distância entre cada par de pontos
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = euclidean_distance(points[i], points[j])
            if distance > max_distance:
                max_distance = distance
                furthest_pair = (points[i], points[j])
    
    return furthest_pair

def find_nearest_point(points, point, couples):
    min_distance = 10000000
    nearest_points = (None, None)
    onCouple = False
    
    for p in points:
        for c in couples:
            if point in c:
                onCouple = True
        
        if onCouple:
            continue
            
        if p == point:
            continue
        
        distance = euclidean_distance(point, p)
        if distance < min_distance:
            min_distance = distance
            nearest_points = (point, p)
    
    couples.append(nearest_points)
    
    return couples

def detect_significant_deviation(contour, threshold=3):
    deviations = []
    for i in range(1, len(contour)):
        prev_point = contour[i - 1][0]
        curr_point = contour[i][0]
        
        # Calcular a diferença entre os pontos
        diff = np.linalg.norm(curr_point - prev_point)
        
        # Verificar se a diferença é maior que o threshold
        if diff > threshold:
            deviations.append((tuple(prev_point), tuple(curr_point)))
    return deviations

def calculate_angle(line1, line2):
   
    vector1 = (line1[1][0] - line1[0][0], line1[1][1] - line1[0][1])
    vector2 = (line2[1][0] - line2[0][0], line2[1][1] - line2[0][1])
    
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    
    magnitude1 = np.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
    magnitude2 = np.sqrt(vector2[0] ** 2 + vector2[1] ** 2)
    
    cos_theta = dot_product / (magnitude1 * magnitude2)
    
    angle_radians = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    angle_degrees = np.degrees(angle_radians)
    
    return round(angle_degrees,1)
#endregion

class ImageFunctions():
    def __init__(self):
        self.centerPoint = None
        self.finalPoints = None
        self.couplePoints = []
        self.contours = None
        self.image = None
        self.selected_point = None
        self.good = None
        self.ok = None
        self.showLine = False
        self.backupImage = None
        self.firstTime = True
        self.adjust = False


    def make_contours(self, img, kernelValue, showBorder = False):
        im = cv2.imread(img)
        image = cv2.resize(im, (598,510))

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, binary = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

        kernel = np.ones(kernelValue, np.uint8)

        eroded = cv2.erode(binary, kernel, iterations=1)

        edges = cv2.Canny(eroded, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if showBorder:
            json = ConfigJson()
            values = json.read()
            color = values["Borders Color"]
            color = ast.literal_eval(color)
            width = values["Borders Width"]
        
            for c in contours:
                cv2.drawContours(image, c, -1, color, width)
        
        self.image = image
        self.contours = contours
        
        
    def find_center(self, showCenterCircle = False):
        all_points = np.vstack([contour.reshape(-1, 2) for contour in self.contours])
        mean_center = np.mean(all_points, axis=0).astype(int)
        self.centerPoint = tuple(mean_center)
        
        if showCenterCircle:
            json = ConfigJson()
            values = json.read()
            color = values["Center Color"]
            color = ast.literal_eval(color)
            width = values["Center Width"]*3
            
            cv2.circle(self.image, self.centerPoint, width, color, -1)


    def find_points(self):
        final_points = []
        
        for contour in self.contours:
            deviations = detect_significant_deviation(contour)
            actual_dev = []
            
            if deviations:
                for significant_point, _ in deviations:
                    
                    end_point = find_final_point(significant_point, self.centerPoint, self.image)
                    actual_dev.append(end_point)
                    
                if actual_dev:
                    if len(actual_dev) < 2:
                        cv2.line(self.image, self.centerPoint, actual_dev[0], (0, 255, 0), 2)
                        continue
                
                    point1, point2 = find_furthest_points(actual_dev)
                    
                    final_points = are_points_close(point1, final_points)
                    final_points = are_points_close(point2, final_points)
        
        imgHeight, imgWidth, _ = self.image.shape
        
        i = 0
        for point in final_points:
            if 0 <= point[0] < imgWidth and 0 <= point[1] < imgHeight:
                x_new = min(max(point[0], 0), imgWidth - 1)
                y_new = min(max(point[1], 0), imgHeight - 1)
                adjusted_point = (x_new, y_new)
                final_points[i] = adjusted_point
            i += 1
            
        self.finalPoints = final_points
        
        
    def find_couples(self):
        self.couplePoints = []
        for final in self.finalPoints:      
            self.couplePoints = find_nearest_point(self.finalPoints, final, self.couplePoints)
        
        
    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            for i, point in enumerate(self.finalPoints):
                if point != None:
                    mid = mid_point(self.centerPoint, point)
                    if np.linalg.norm(np.array([x, y]) - np.array(mid)) < 10:
                        self.selected_point = i
                        break
        elif event == cv2.EVENT_MOUSEMOVE and self.selected_point is not None:
            self.finalPoints[self.selected_point] = find_final_point((x, y), self.centerPoint, self.image)
            self.redraw_image(self.good, self.ok, self.showLine, self.adjust)
        elif event == cv2.EVENT_LBUTTONUP:
            self.selected_point = None
        

    def redraw_image(self, good, ok, showLines = False, showAdjust = False):
        image_copy = self.image.copy()
        
        json = ConfigJson()
        values = json.read()
        color = values["Lines Color"]
        linecolor = ast.literal_eval(color)
        linewidth = values["Lines Width"]
        color = values["Adjust Color"]
        adjustcolor = ast.literal_eval(color)
        adjustwidth = values["Adjust Width"]*3
        
        self.adjust = showAdjust
        self.showLine = showLines
        self.good = good
        self.ok = ok
        
        if self.adjust:
            for point in self.finalPoints:
                mid = mid_point(self.centerPoint, point)
                cv2.circle(image_copy, mid, adjustwidth, adjustcolor, -1)
            
        self.find_couples()
        
        for couple in self.couplePoints:
            lines = []
            
            for point in couple:
                if point == None:
                    continue
                
                if self.showLine:
                    cv2.line(image_copy, self.centerPoint, point, linecolor, linewidth)
                    
                lines.append((self.centerPoint, point))
            
            if lines:
                angle = calculate_angle(lines[0],lines[1])
                
                if angle >= self.good:
                    cv2.putText(image_copy, str(angle), mid_point(mid_point(lines[0][0], lines[0][1]), mid_point(lines[1][0], lines[1][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0 , 255, 0), 1)
                    continue
                
                if angle >= self.ok:
                    cv2.putText(image_copy, str(angle), mid_point(mid_point(lines[0][0], lines[0][1]), mid_point(lines[1][0], lines[1][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 1)
                    continue
                
                
                cv2.putText(image_copy, str(angle), mid_point(mid_point(lines[0][0], lines[0][1]), mid_point(lines[1][0], lines[1][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
       
        
        cv2.imshow('Image', image_copy)


    def show_image(self, good, ok, line, adjust):
        if adjust:
            cv2.namedWindow('Image')
            cv2.setMouseCallback('Image', self.mouse_callback)
        
        self.redraw_image(float(good), float(ok), line, adjust)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()