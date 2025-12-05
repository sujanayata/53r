from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from basic.models import Student
from basic.models import Users
from django.contrib.auth.hashers import make_password,check_password
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# Create your views here.
def sample(request):
    return HttpResponse('hello world')

def sample1(request):
    return HttpResponse('welcome to django')

def sampleInfo(request):
    # data={"name":"suppu","age":23}
    data={"result":[4,6,8,9]}
    return JsonResponse(data)

def dynamicresponse(request):
    name=request.GET.get("name","kiran")
    city=request.GET.get("city","hyd")
    return HttpResponse(f"hello {name} from {city}")

# to test databse connection
def health(request):
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
        return JsonResponse({"status":"ok","db":"connected"})    
    except Exception as e:
        return JsonResponse({"status":"error","db":str(e)})
    


@csrf_exempt
def addStudent(request):  
    print(request.method)
    if request.method=='POST':
        data=json.loads(request.body)
        student=Student.objects.create(
            name=data.get('name'),
            age=data.get('age'),
            email=data.get('email')
            )
        return JsonResponse({"status":"success","id":student.id},status=200)
    elif request.method=="GET":
        result=list(Student.objects.all().values())
        print(result)
        result=Student.objects.get(id=3)
        data = {
            "id": result.id,
            "name": result.name,
            "age": result.age
        }
        return JsonResponse(data)
        # print(result)

        
        
    
    elif request.method=="PUT":
        data=json.loads(request.body)
        ref_id=data.get("id")
        new_email=data.get("email")
        existing_student=Student.objects.get(id=ref_id)
        # print(existing_student)
        existing_student.email=new_email  
        existing_student.save()
        updated_data=Student.objects.filter(id=ref_id).values().first()
        return JsonResponse({"req":"data updated successfully","updated_data":updated_data},status=200)
    elif request.method=="DELETE":
         data=json.loads(request.body)
         ref_id=data.get("id")
         get_deleted_data=list(Student.objects.filter(id=ref_id).values())
         to_be_deleted=delete_data=Student.objects.get(id=ref_id)
         to_be_deleted.delete()
         return JsonResponse({"status":"success","message":"student details deleted successfully","deleted_data":get_deleted_data},status=200)
    elif request.method == 'POST':
        data = json.loads(request.body)
        student = Student.objects.create(
            name=data.get('name'),
            age=data.get('age'),
            email=data.get('email')
        )
        return JsonResponse({"status": "success", "id": student.id}, status=200)



    # elif request.method=="GET":
    #     data=json.loads(request.body)
    #     ref_id=data.get("id")
    #     result=Student.objects.filter(id=ref_id).values().first()
    #     print(result)
    #     return JsonResponse({"status":"success","data":result})





    return JsonResponse({"error":"use post method"},status=400)  

from .models import Post

@csrf_exempt
def addPost(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post = Post.objects.create(
                post_name=data.get('post_name'),
                post_type=data.get('post_type'),
                post_date=data.get('post_date'),
                post_description=data.get('post_description')
            )
            return JsonResponse({"status": "success", "id": post.id}, status=201)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"error": "Use POST method"}, status=405)


# def get_all_students(request):
#     students = Student.objects.all()
#     data = list(students.values())
#     return JsonResponse(data, safe=False)




# def get_student_by_id(request, student_id=None):
#     if student_id is not None:
#         try:
#             student = Student.objects.get(id=student_id)
#             return JsonResponse({
#                 'id': student.id,
#                 'name': student.name,
#                 'age': student.age,
#                 'city': student.city
#             })
#         except Student.DoesNotExist:
#             return JsonResponse({'error': 'Student not found'}, status=404)
#     else:
#         students = Student.objects.all().values()
#         return JsonResponse(list(students), safe=False)
    

# def filter_age_gte_20(request):
#     students = Student.objects.filter(age__gte=20)
#     data = list(students.values())
#     return JsonResponse(data, safe=False)


# def filter_age_lte_25(request):
#     students = Student.objects.filter(age__lte=25)
#     data = list(students.values())
#     return JsonResponse(data, safe=False)

# def order_by_name(request):
#     students = Student.objects.order_by('name')
#     data = list(students.values())
#     return JsonResponse(data, safe=False)    
# def get_unique_ages(request):
#     ages = Student.objects.values_list('age', flat=True).distinct()
#     return JsonResponse({'unique_ages': list(ages)})

# def count_students(request):
#     total = Student.objects.count()
#     return JsonResponse({'total_students': total})'''


# def job1(request):
#    return JsonResponse({"message":"u have successfully applied for job1"},status=200)
# def job2(request):
#    return JsonResponse({"message":"u have successfully applied for jo "})


@csrf_exempt
def signUp(request):
    if request.method=='POST':
        data = json.loads(request.body)
        print(data)
        user=Users.objects.create(
            username=data.get('username'),
            email=data.get('email'),
            password=make_password(data.get('password'))
            )
    return JsonResponse({"status":"success"},status=200)    


@csrf_exempt
def login(request):
    if request.method=="POST":
        data=request.POST
        print(data)
        username=data.get('username')
        password=data.get("password")        
        try:
            user=Users.objects.get(username=username)
            issued_time=datetime.now(ZoneInfo("Asia/kolkata"))
            expired_time=issued_time+timedelta(minutes=30)
    
            if check_password(password,user.password):
                    # token="a json web token"
                    payload={"username":username,"email":user.email,"id":user.id,"exp":expired_time}
                    token=jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")
                    return JsonResponse({"status":'successfully loggedin','token':token,"issued_at":issued_time,"expired_at":issued_time,"expired_in":int((expired_time-issued_time).total_seconds()/60)},status=200)
            else:
                    return JsonResponse({"status":'failure','message':'invalid password'},status=400)
        except Users.DoesNotExist:
            return JsonResponse({"status":'failure','message':'user not found'},status=400)
        




@csrf_exempt
def check(request):
    hashed="pbkdf2_sha256$870000$16lqSTM85dDYNKjEtL27RW$3K7iXJHC80KdB6EXIWEVGPZoItvb7sC3TDisNnZXwrY="
    ipdata=request.POST
    print(ipdata) 
    # hashed=make_password(ipdata.get("ip"))
    x=check_password(ipdata.get("ip"),hashed)
    print(x)
    return JsonResponse({"status":"success","data":x},status=200) 
@csrf_exempt
def hash_all_passwords(request):
    if request.method == "GET":   # or POST
        users = Users.objects.all()
        for user in users:
            if not user.password.startswith("pbkdf2_sha256"):
                user.password = make_password(user.password)
                user.save()

        return JsonResponse({"status": "success", "message": "All passwords hashed"}, status=200)


@csrf_exempt
def getAllusers(request):
    if request.method == "GET":
        users = list(Users.objects.values()) # returns list of dicts
        print(request.token_data,"token data in view") 
        print(request.token_data.get("username"),"username from token") 
        print(users,"userslist")
        # return JsonResponse(list(users), safe=False)
        for user in users:
            print(user["username"],"username from users list")
            if  user["username"] == request.token_data.get("username"):
                return JsonResponse({"status":"success","loggedin_user":request.token_data,"data":users},status=200)
        else:   
                return JsonResponse({"error":"unauthorized access"},status=401)
            



def homerequest(request):
    return render(request,"home.html")


def aboutus(request):
    return render(request,"about.html")


def welcome(request):
    return render(request,"welcome.html")


def contact(request):
    return render(request,"contact.html")

def services(request):
    return render(request,"services.html")

def projects(request):
    return render(request,"projects.html")
