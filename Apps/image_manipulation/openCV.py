import cv2
import numpy as np

# image = cv2.imread('../img/image1.png')
# image2 = cv2.imread('../img/image2.png')
# image3 = cv2.imread('../img/image3.png')

def showImage(title = "Original Image", img = 0):
  cv2.imshow(title,img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def grayscale(image):
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # showImage("Gryscale Image", gray_image)
  return gray_image

def sepia(image, filter_degre = [[0.272, 0.534, 0.131],[0.349, 0.686, 0.168],[0.393, 0.769, 0.189]]):
  sepia_filter = np.array(filter_degre)
  sepia_image = cv2.transform(image,sepia_filter)
  sepia_image = np.clip(sepia_image,0,255)
  # showImage("Sepia Image",sepia_image.astype('uint8'))
  return sepia_image

def blur(image,size=(15,15)):
  blurred_image = cv2.GaussianBlur(image,(15,15),0)
  # showImage("Blur effect",blurred_image)
  return blurred_image

def invert(image):
  inverted_image = cv2.bitwise_not(image)
  # showImage("Invert effect",inverted_image)
  return inverted_image

def pixelation(image,pixel_size = 10):
  small = cv2.resize(image,(image.shape[1]//pixel_size,image.shape[0]//pixel_size),interpolation=cv2.INTER_LINEAR)
  pixeled_image = cv2.resize(small,(image.shape[1],image.shape[0]),interpolation=cv2.INTER_NEAREST)
  # showImage("Pixelation effect",pixeled_image)
  return pixeled_image

def edge_detection(image,threshold = [50,150]):
  edges = cv2.Canny(image,threshold[0],threshold[1])
  # showImage("Edge detection effect",edges)
  return edges

def emboss(image,kernel = [[ -2, -1,  0],[ -1,  1,  1],[  0,  1,  2]]):
  kernel = np.array(kernel)
  embossed_image = cv2.filter2D(image,-1,kernel)
  # showImage("Emboss effect",embossed_image)
  return embossed_image

def cartoon(image):
  gray = grayscale(image)
  # showImage("gray",gray)
  blurred = cv2.medianBlur(gray,7)
  edges = cv2.adaptiveThreshold(blurred,255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)
  color = cv2.bilateralFilter(image,9,300,300)
  cart = cv2.bitwise_and(color,color,mask=edges)
  # showImage("Cartoon effect",cart)
  return cart

def oil_painting(image):
  oil_paint = cv2.xphoto.oilPainting(image,7,1)
  # showImage('Oil painting effect',image)
  return oil_paint