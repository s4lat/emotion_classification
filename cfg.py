import cv2

PREFFERED_THEME = 'cleanlooks'

SCALE_FACTOR = 1.5
OUT_WIDTH, OUT_HEIGHT = 640, 360
IN_WIDTH, IN_HEIGHT = OUT_WIDTH // SCALE_FACTOR, OUT_HEIGHT // SCALE_FACTOR
IN_WIDTH, IN_HEIGHT = int(IN_WIDTH), int(IN_HEIGHT)

NOT_SELECTED_COLOR = (0, 255, 0)[::-1] #RGB to BGR
SELECTED_COLOR = (255, 140, 0)[::-1]

MODELS = { 'tiny_x' : 'tiny_exception_0.60_48.hdf5',
 			'mini_x' : 'mini_exception_0.00_64.hdf5',
 			'big_x' : 'big_exception_0.66_48.hdf5',
 			'simpler_cnn' : 'simpler_cnn_62_48.hdf5',
 			'simple_cnn' : 'simple_cnn_0.60_48.hdf5'
 		}
CURR_MODEL = 'mini_x'
EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised",
 "neutral"]
EMOTIONS_RUS = ["Злость" ,"Отвращение","Испуг", "Счастье", "Грусть", "Удивление",
 "Спокойствие"]

USE_HOG = False

font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 0.5
fontColor              = (255, 255, 255)[::-1]
bgColor                = (255, 0, 0)[::-1]
lineType               = cv2.LINE_AA

