from unittest import result
from django.shortcuts import render,HttpResponse
from dashboard.forms import *
from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
from dashboard.models import *
from django.db import transaction

# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')

@login_required()
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,title =request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f'Notes Added from {request.user.username} Successfully!')
    else:
        form = NotesForm()
    notes = Notes.objects.all()
    context = {'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

@login_required()
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')

class NotesDetailView(generic.DetailView):
    model = Notes

@login_required()
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request,f'Homework added from {request.user.username}')
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user = request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {'homeworks':homework,'homeworks_done':homework_done,'form':form}
        
    return render(request,'dashboard/homework.html',context)

@login_required()
def update_homework(request,pk=None):
    homework=Homework.objects.get(pk=pk)
    homework.is_finished = not homework.is_finished
    homework.save()
    return redirect('homework')

@login_required()
def delete_homework(request,pk=None):
   Homework.objects. get(id=pk).delete()
   return redirect("homework")

@login_required()
def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)  
        text = request.POST['text'] 
        video= VideosSearch(text,limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['descriptionSnippet']= desc
            result_list.append(result_dict)
            context ={
                'form':form,
                'results':result_list
            }
        return render(request,"dashboard/youtube.html",context)
    else:
        form = DashboardForm()
    return render(request,"dashboard/youtube.html",{'form':form})

@login_required()
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished 
            )
            todos.save()
            messages.success(request,f'Todo added from {request.user.username}')
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {'form':form,'todos':todo,'todos_done':todos_done}
    return render(request,'dashboard/todo.html',context)

@login_required()
def markcompleted(request,id):
    todo = Todo.objects.get(id=id)
    todo.is_finished = not todo.is_finished
    todo.save()
    return redirect('todo')

@login_required()
def edit(request,id):
    todo = Todo.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'dashboard/editt.html',{'todo':todo})
    else:
        ntitle = request.POST['title']
        todo.title = ntitle
        todo.save()
        return redirect('todo')
        
@login_required()
def delete_todo(request,id):
   Todo.objects.get(id=id).delete()
   return redirect('todo')

@login_required()
def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)  
        text = request.POST['text'] 
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)     
        answer = r.json() 
        result_list = [] 
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)
            context ={
                'form':form,
                'results':result_list
            }
        return render(request,"dashboard/books.html",context)
    else:
        form = DashboardForm()
    return render(request,"dashboard/books.html",{'form':form})

@login_required()
def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)  
        text = request.POST['text'] 
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)     
        answer = r.json() 
        result_list = [] 
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition=answer[0]['meanings'][0]['definitions'][0]['definition']
            example=answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms=answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context = {
                'form':form,
                'input':''
            }
        return render(request,"dashboard/dictionary.html",context)
    else:
        form = DashboardForm()
        context = {'form':form}
    return render(request,"dashboard/dictionary.html",context)

@login_required()
def wiki(request):
    if request.method == "POST":
        text = request.POST['text'] 
        form= DashboardForm(request.POST)
        search = wikipedia.page(text)
        context={
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,"dashboard/wiki.html",context)
    else:
        form= DashboardForm()
    return render(request,"dashboard/wiki.html",{'form':form})


@login_required()
def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST['measurement']== 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'

                    if first == 'meter' and second == 'foot':
                        answer = f'{input} meter = {int(input)/0.3048} foot'
                    if first == 'foot' and second == 'meter':
                        answer = f'{input} foot = {int(input)*0.3048} meter'

                    
                    if first == 'meter' and second == 'yard':
                        answer = f'{input} meter = {int(input)/0.9144} yard'
                    if first == 'yard' and second == 'meter':
                        answer = f'{input} yard = {int(input)*0.9144} meter'

                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
        if request.POST['measurement']== 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilograms'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)/0.453592} pounds'
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }

    else:
        form = ConversionForm()
        context = {
        'form':form,
        'input':False
         }
    return render(request,"dashboard/conversion.html",context)


@transaction.non_atomic_requests(using='None')
def stnotes(request):
    if request.method == "POST":
        category = request.POST.get("category")
        title = request.POST.get("title")
        description = request.POST.get("description")
        files = request.FILES.getlist("uploadfiles")
        for f in files:
            stNotes(category = category,title = title,description=description,files=files).save()
            return HttpResponse('Success')
    else:
        return render(request,"dashboard/viewnotes.html")

def noticehome(request):
    notices = notice.objects.all()
    return render(request,'home.html',{'notices':notices})       

def create_notice(request):
    if request.method == 'POST':
        form = noticeform(request.POST)
        notices = notice(title = request.POST['title'],description = request.POST['description'])
        notices.save()
        messages.success(request,'Notice added successfully')
        return redirect('home')
    else:
        form = noticeform()  
    context = {'form':form}
    return render(request,'dashboard/notices.html',context)

def delete_notice(request,id):
   notice.objects.get(id=id).delete()
   return redirect('home')

 