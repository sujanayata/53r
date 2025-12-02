from django.http import JsonResponse
import re,json
import jwt
from django.conf import settings
from basic.models import Users
class basicMiddleware:
    def __init__(self, get_response):  #automatically give the response #start the server then it is run

        self.get_response=get_response

    def __call__(self,request): #start when pass request
        print(request,"hello")
        if(request.path=="/add/"):
            print(request.method,"method")
            print(request.path)
        elif(request.path=="/greet/"):
            print(request.method,"method")
            print(request.path)
        elif(request.path=="/info/"):
            print(request.method,"method")
            print(request.path)
        elif(request.path=="/post/"):
            print(request.method,"method")
            print(request.path)
        response= self.get_response(request)
        return response

# class basicMiddleware: #class in camel case
#     def init(self,get_response):
#         self.get_response=get_response
#     def call   (self,request):
#         data=json.loads(request.body)
#         username=data.get("username") 
#         email=data.get("email")
#         dob=data.get("dob")
#         password=data.get("pswd")
        # check the username rules with regex
        # check the email rules with regex
        # check dob rules with regex
        # check the password with regex


class sscMiddleware:
    def __init__(self,get_response):  
        self.get_response=get_response
    def __call__(self,request):
        if(request.path in ["/job1/","/job2/"]):
            ssc_result=request.GET.get("ssc")
            if(ssc_result!='True'):
                return JsonResponse({
                   "error":"u should qualify atleast ssc for applying this job"
               },status=400)
        return self.get_response(request)


class MedicalFitMiddleware:
    def __init__(self,get_response):  
        self.get_response=get_response
    def __call__(self,request):
        if(request.path=="/job1/"):
            medical_fit_result=request.GET.get("medically_fit")
            if(medical_fit_result !='True'):
                 return JsonResponse({
                   "error":"medically unfit for this job"
               },status=400)
        return self.get_response(request)
        
        

class AgeMiddleware:
    def __init__(self,get_response):  
        self.get_response=get_response
    def __call__(self,request):
        if(request.path in ["/job1/","/job2/"]):
            age_checker=int(request.GET.get("age",17))
            if not (18 <= age_checker <= 25):
                return JsonResponse({"error":"age must be in between 18 and 25"},status=400)
        return self.get_response(request)
    


class UsernameMiddleware:
    def __init__(self,get_response):  
        self.get_response=get_response
    def __call__(self,request): 
        if(request.path=="/signup/")  :
            data=json.loads(request.body)
            username=data.get("username") 
            # checks username is empty or not
            if not username:
                return JsonResponse({"error":"username is required"},status=400)
            # checks lenght
            if len(username)<3 or len(username)>20:
                return JsonResponse({"error":"username should cntain 3 to 20 characters"},status=200)
            # checks starting and ending
            if username[0] in "._" or username[-1] in "._":
                return JsonResponse({"error":"username should not starts or ends with . or _"},status=400)
            # check allowed charcater
            if not re.match(r"^[a-zA-Z0-9._]+$",username):
                return JsonResponse({"error":"username should not contain letters,numbers,dot,underscore"},status=400)
            if ".." in  username or "__" in username:
                return JsonResponse({"error":"cannot have .. or __"},status=400)
        return self.get_response(request)    
    

#email should not be empty
# basic email pattern
# if duplicate email found-->email already exists 


class EmailMiddleware:
    def __init__(self,get_response):  
        self.get_response=get_response
    def __call__(self,request): 
        if(request.path=="/signup/") :
            data=json.loads(request.body)
            email=data.get("email")
            if not email:
                return JsonResponse({"error":"email should not be empty"},status=400)
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$',email):
                return JsonResponse({"error":"invalid email format"},status=400)
            if Users.objects.filter(email=email):
                return JsonResponse({"error":"Email already exists"},status=400)
        return self.get_response(request)    


class PasswordMiddleware:
    def __init__(self,get_response):  
        self.get_response=get_response
    def __call__(self,request): 
        if(request.path=="/signup/") :
            data=json.loads(request.body)
            Password=data.get("password")
            if not Password:
                return JsonResponse({"error":"password should not empty"},status=400)
            if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^\w\s]).{8,}$',Password):
                return JsonResponse({"error":"Password must contain at least 8 characters including uppercase, lowercase, number and special character"}, status=400)
            
        return self.get_response(request)                              
    


class authenticate_middleware():
    def __init__(self,get_response):
            self.get_response=get_response
    def __call__(self,request):
        if request.path=="/users/":
            token=request.headers.get("Authorization","")
            print(token,"token")
            if not token:
                return JsonResponse({"error":"authorization token is missing"},status=200)
            token_value=token.split(" ")[1]
            print(token_value,"token_value")
            try:
                decoded_data=jwt.decode(token_value,settings.SECRET_KEY,algorithms=["HS256"])
                print(decoded_data,"decoded_data")
                request.token_data=decoded_data  
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error":"token has expired,please login again"},status=401)    
            except jwt.exceptions.InvalidSignatureError:
                return JsonResponse({"error":"invalid token signature"},status=401)  
        return self.get_response(request)    