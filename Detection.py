from Messages import Messages
from Results import *
from ultralytics import YOLO
import cv2
from pytesseract import pytesseract

class Detection:
    
    _Model:str = None
    _Img:str = None
    
    def __init__(self,model,img) -> None:
        self._Model = model
        self._Img = img
    
    def __str__(self) -> str:
        return "Usage : Detection(model,img)"

    def detect(self,Save = False) -> IDataResult:
        context = list()
        try:
            model = YOLO(model=self._Model)
            img = cv2.imread(self._Img)
            results = model.predict(source=img,save=Save)
            
            for result in results:
                for box in result.boxes:
                    className = result.names[box.cls[0].item()]
                    cords = box.xyxy[0].tolist()
                    cords = [round(x) for x in cords]
                    conf = round(box.conf[0].item(), 2)
                    obj = {
                        "ObjectName":className,
                        "Coordinates":cords,
                        "Conf":int(conf * 100)
                    }
                    context.append(obj)
                    
        except Exception as err:
            return ErrorDataResult(message=err)
        if(len(context) == 0):
            return ErrorDataResult(message=Messages.DetectionError)
        return SuccessDataResult(data=context)

    def FindObjectIndexes(self, values:list) -> IDataResult:
        context = self.detect()
        if context.Success:
            indexes = { value: [] for value in values }
            for i, item in enumerate(context.Data):
                for value in values:
                    if item["ObjectName"] == value:
                        indexes[value].append(i)
            if len(indexes) != 0:
                return SuccessDataResult(data=indexes)
        return ErrorDataResult(Messages.DetectionError)
        
    def CropAndRecognize(self, img, cords):
        pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        x_min, y_min, x_max, y_max = cords
        roi = img[y_min:y_max, x_min:x_max]
        return pytesseract.image_to_string(roi, config="-c tessedit_char_whitelist=0123456789")
    
    def ProcessResults(self, indexes):
        image = cv2.imread(self._Img)
        recognized_text:str = None
        for index in indexes:
            cords = self.detect().Data[index]["Coordinates"]
            recognized_text = self.CropAndRecognize(image, cords)
        if recognized_text == ' ':
            return ErrorDataResult(Messages.RecognizedError)
        return SuccessDataResult(data = recognized_text)
    
    def Endex(self):
        indexesResult = self.FindObjectIndexes(["endex"])

        if indexesResult.Success:
            for value, indexes in indexesResult.Data.items():
                result = self.ProcessResults(indexes)
                if result.Success:
                    return SuccessDataResult(data = result.Data)
        return ErrorDataResult(result.Message)
    
    def Meter(self) -> IDataResult:
        indexesResult = self.FindObjectIndexes(["sayacNo"])

        if indexesResult.Success:
            for value, indexes in indexesResult.Data.items():
                result = self.ProcessResults(indexes)
                if(result.Success):
                    return SuccessDataResult(data = result.Data)
        return ErrorDataResult(result.Message)

    def Run(self):
        Endex = self.Endex().Data
        return SuccessDataResult(data = Endex)
Detect = Detection(model="detection.pt", img="ImagePath")
# Detect.Run()
print(Detect.Run().Data)
