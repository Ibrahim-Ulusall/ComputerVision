class IResult:
    Message:str
    Success:bool
    
class IDataResult(IResult):
    Data = None

class Result(IResult):
    
    def __init__(self,message,success):
        self.Message = message
        self.Success = success

class DataResult(IDataResult,Result):
    
    def __init__(self, message, success, data):
        self.Data = data
        super().__init__(message, success)

class SuccessResult(Result):
    
    def __init__(self,message = None):
        super().__init__(message,True)
        
class ErrorResult(Result):
    
    def __init__(self,message = None):
        super().__init__(message,False)
        
class SuccessDataResult(DataResult):
    def __init__(self,message=None,data=None):
        super().__init__(message,True,data)
        
class ErrorDataResult(DataResult):
    
    def __init__(self,message = None,data = None):
        super().__init__(message,False,data)