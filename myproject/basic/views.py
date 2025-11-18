from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from basic.models import Student
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
        print(result)

        
        return JsonResponse({"status":"ok","data":result},status=200)
        data=json.loads(request.body)
        ref_age=data.get("age")
        results=list(Student.objects.filter(age__gte=ref_age).values())
        return JsonResponse({"status":"ok","data":results},status=200)
    
        data=json.loads(request.body)
        ref_age=data.get("age")
        results=list(Student.objects.filter(age__lte=ref_age).values())
        return JsonResponse({"status":"ok","data":results},status=200)
        
        # order by name
        results=list(Student.objects.order_by('name').values())
        return JsonResponse({"status":"ok","data":results},status=200)

        # get unique ages
        results=list(Student.objects.values("age").distinct())
        return JsonResponse({"status":"ok","data":results},status=200)

        # count total students
        results=Student.objects.count()
        return JsonResponse({"status":"ok","data":results},status=200)



    
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


def job1(request):
   return JsonResponse({"message":"u have successfully applied for job1"},status=200)
def job2(request):
   return JsonResponse({"message":"u have successfully applied for jo "})

