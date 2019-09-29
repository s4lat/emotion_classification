import cv2

PREFFERED_THEME = 'cleanlooks'

IN_WIDTH, IN_HEIGHT = 426, 240

NOT_SELECTED_COLOR = (0, 255, 0)[::-1] #RGB to BGR
SELECTED_COLOR = (255, 140, 0)[::-1]

QUIZ_IMAGES_PATH = 'static/quiz/'

MODELS = { 'tiny_x' : 'static/models/tiny_exception_0.60_48.hdf5',
 			'mini_x' : 'static/models/mini_exception_0.00_64.hdf5',
 			'big_x' : 'static/models/big_exception_0.66_48.hdf5',
 			'simpler_cnn' : 'static/models/simpler_cnn_62_48.hdf5',
 			'simple_cnn' : 'static/models/simple_cnn_0.60_48.hdf5',
 			'swish' : 'static/models/swish_model.52-0.91.hdf5'
 		}
CURR_MODEL = 'swish'
FRONTAL_FACE_DETECTOR = 'static/models/haarcascade_frontalface_default.xml'

BUTTON_TO_EMOTION = {
	'angryBtn' : 0,
	'disgustBtn' : 1,
	'scaredBtn' : 2,
	'happyBtn' : 3,
	'sadBtn' : 4,
	'surprisedBtn' : 5,
	'neutralBtn' : 6,
}

EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised",
 "neutral"]
EMOTIONS_RUS = ["Злость" ,"Отвращение","Испуг", "Счастье", "Грусть", "Удивление",
 "Спокойствие"]

font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 0.5
fontColor              = (255, 255, 255)[::-1]
bgColor                = (255, 0, 0)[::-1]
lineType               = cv2.LINE_AA

TOP_BAD_LABEL = '<html><head/><body><p align="center"><span style=" font-size:18pt;">Ответ </span><span style=" font-size:18pt; color:#ff0000;">%s</span><span style=" font-size:18pt;"> - неверен, правильный ответ - </span><span style=" font-size:18pt; color:#00dc00;">%s</span></p></body></html>'
TOP_GOOD_LABEL = '<html><head/><body><p align="center"><span style=" font-size:18pt;">Верно! </span><span style=" font-size:18pt; color:#00dc00;">%s</span><span style=" font-size:18pt;"> - правильный ответ</span></p></body></html>'
TOP_NEUTRAL_LABEL = '<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Какую эмоцию выражает лицо человека на изображении?</span></p></body></html>'
QUIZ_SCORE_LABEL = '<html><head/><body><p align=\"center\"><span style=\" font-size:28pt; color:#00dc00; vertical-align:sub;\">✓:%s</span></p><p align=\"center\"><span style=\" font-size:28pt; color:#ff0000; vertical-align:sub;\">✗:%s</span></p><p align=\"center\"><span style=\" font-size:28pt; color:#000000; vertical-align:sub;\">O:%s</span></p></body></html>'

