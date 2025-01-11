from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Person, Diary
from datetime import datetime, timedelta
from django.db.models import Count # Count function

def home(request):
  texts = Diary.objects.all().order_by('creation_date')[:3][::-1]
  persons = Person.objects.all()
  # names = [person.name for person in persons]
  # qtys = []
  # for person in persons:
  #   qty = Diary.objects.filter(persons=person).count()
  #   qtys.append(qty)
  persons_with_count = Person.objects.annotate(qty_diarys=Count('diary'))
  names = [person.name for person in persons_with_count]
  qtys = [person.qty_diarys for person in persons_with_count]
  return render(request, 'home.html', {'texts': texts, 'names': names, 'qtys': qtys})

def write(request):
  if request.method == 'GET':
    persons = Person.objects.all()
    for person in persons:
      print(person.name)
    return render(request, 'write.html', {'persons': persons})
  elif request.method == 'POST':
    entry_title = request.POST.get('entry-title')
    entry_tags = request.POST.getlist('entry-tags')
    entry_people = request.POST.getlist('entry-people')
    entry_text = request.POST.get('entry-text')
    if len(entry_title.strip()) == 0 or len(entry_text) == 0:
      # TODO: Add error messages
      return redirect('write')
    diary = Diary(
      title = entry_title,
      text = entry_text
    )
    diary.set_tags(entry_tags)
    diary.save()
    

    # Simple version:
    # for i in entry_people:
    #   person = Person.objects.get(i == id)
    #   diary.persons.add(person)
    # diary.save()
    # Advanced version:
    person_objs = Person.objects.filter(id__in=entry_people)
    diary.persons.add(*person_objs)
    diary.save()


    # TODO: Add success message
    return redirect('write')

def new_person(request):
  if request.method == 'GET':
    return render(request, 'person.html')
  elif request.method == 'POST':
    name = request.POST.get('name')
    photo = request.FILES.get('photo')
    person = Person(
      name = name,
      photo = photo,
    )
    person.save()
    return redirect('write')

def read(request):
    date = request.GET.get('date')
    formatted_date = datetime.strptime(date, '%Y-%m-%d')
    diarys = Diary.objects.filter(creation_date__gte=formatted_date).filter(creation_date__lte=formatted_date + timedelta(days=1))

    return render(request, 'read.html', {'diarys': diarys, 'total': diarys.count(), 'date': date})

def delete(request):
    day = datetime.strptime(request.GET.get('date'), '%Y-%m-%d')
    diarys = Diary.objects.filter(creation_date__gte=day).filter(creation_date__lte=day + timedelta(days=1))
    diarys.delete()
    # TODO: Show message
    return redirect('write')
