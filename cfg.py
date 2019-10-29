import cv2, os

PREFFERED_THEME = 'cleanlooks' #Предпочитаемая тема

IN_WIDTH, IN_HEIGHT = 426, 240
OUT_WIDTH, OUT_HEIGHT = 640, 360

SCALE_WIDTH = IN_WIDTH / OUT_WIDTH
SCALE_HEIGHT = IN_HEIGHT / OUT_HEIGHT

NOT_SELECTED_COLOR = (0, 255, 0)[::-1] #RGB to BGR
SELECTED_COLOR = (255, 140, 0)[::-1]

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__)) #Полный путь к данному скрипту


QUIZ_IMAGES_PATH = SCRIPT_PATH+'/static/quiz/' #Путь к изображениям викторины
FONT_PATH = SCRIPT_PATH+"/static/helvetica.ttf" #Путь к шрифту для Pillow

#Словарь всех сетей с путем к их весам
MODELS = { 'tiny_x' : SCRIPT_PATH+'/static/models/tiny_exception_0.60_48.hdf5',
 			'mini_x' : SCRIPT_PATH+'/static/models/mini_exception_0.00_64.hdf5',
 			'big_x' : SCRIPT_PATH+'/static/models/big_exception_0.66_48.hdf5',
 			'simpler_cnn' : SCRIPT_PATH+'/static/models/simpler_cnn_62_48.hdf5',
 			'simple_cnn' : SCRIPT_PATH+'/static/models/simple_cnn_0.60_48.hdf5',
 			'swish' : SCRIPT_PATH+'/static/models/swish_model.52-0.91.hdf5'
 		}

CURR_MODEL = 'big_x' #Использующаяся нейросеть
FRONTAL_FACE_DETECTOR = SCRIPT_PATH+'/static/models/haarcascade_frontalface_default.xml' #Путь к детектору лиц

#Конвертер названия кнопки в индекс
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
 "neutral"] #Эмоции
EMOTIONS_RUS = ["Злость" ,"Отвращение","Испуг", "Счастье", "Грусть", "Удивление",
 "Спокойствие"] #Эмоции на русском

font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 0.8
fontColor              = (255, 255, 255)[::-1]
bgColor                = (255, 0, 0)[::-1]
lineType               = cv2.LINE_AA

#Текст для лейблов в викторине
TOP_BAD_LABEL = '<html><head/><body><p align="center"><span style=" font-size:18pt;">Ответ </span><span style=" font-size:18pt; color:#ff0000;">%s</span><span style=" font-size:18pt;"> - неверен, правильный ответ - </span><span style=" font-size:18pt; color:#00dc00;">%s</span></p></body></html>'
TOP_GOOD_LABEL = '<html><head/><body><p align="center"><span style=" font-size:18pt;">Верно! </span><span style=" font-size:18pt; color:#00dc00;">%s</span><span style=" font-size:18pt;"> - правильный ответ</span></p></body></html>'
TOP_NEUTRAL_LABEL = '<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Какую эмоцию выражает лицо человека на изображении?</span></p></body></html>'
QUIZ_SCORE_LABEL = '<html><head/><body><p align=\"center\"><span style=\" font-size:28pt; color:#00dc00; vertical-align:sub;\">✓:%s</span></p><p align=\"center\"><span style=\" font-size:28pt; color:#ff0000; vertical-align:sub;\">✗:%s</span></p><p align=\"center\"><span style=\" font-size:28pt; color:#000000; vertical-align:sub;\">O:%s</span></p></body></html>'

