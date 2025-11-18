from django.http import JsonResponse
import re,json
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

