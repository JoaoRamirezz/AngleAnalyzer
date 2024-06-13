from .Functions import ImageFunctions

def run(path, good, ok, line, contour, center, adjust):
    findAngle = ImageFunctions()
    
    findAngle.make_contours(path, (6,8), contour)
    findAngle.find_center(center)
    findAngle.find_points()
    findAngle.show_image(good, ok, line, adjust)