from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Person, Dream
from datetime import datetime, timedelta
from django.db.models import Count # Count function

def home(request):
  texts = Dream.objects.all().order_by('creation_date')[:3][::-1]
  persons = Person.objects.all()
  persons_with_count = Person.objects.annotate(qty_dreams=Count('dream'))
  names = [person.name for person in persons_with_count]
  qtys = [person.qty_dreams for person in persons_with_count]
  return render(request, 'home.html', {'texts': texts, 'names': names, 'qtys': qtys})

def write(request):
  if request.method == 'GET':
    persons = Person.objects.all()
    return render(request, 'write.html', {'persons': persons})
  elif request.method == 'POST':
    title = request.POST.get('title')
    tags = request.POST.getlist('tags')
    persons = request.POST.getlist('persons')
    text = request.POST.get('text')
    if len(title.strip()) == 0 or len(text) == 0:
      # TODO: Add error messages
      return redirect('write')
    dream = Dream(
      title = title,
      text = text
    )
    dream.set_tags(tags)
    dream.save()
    

    # Simple version:
    # for i in persons:
    #   person = Person.objects.get(i == id)
    #   dream.persons.add(person)
    # dream.save()
    # Advanced version:
    person_objs = Person.objects.filter(id__in=persons)
    dream.persons.add(*person_objs)
    dream.save()


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
    dreams = Dream.objects.filter(creation_date__gte=formatted_date).filter(creation_date__lte=formatted_date + timedelta(days=1))
    return render(request, 'read.html', {'dreams': dreams, 'total': dreams.count(), 'date': date})

def delete(request):
    day = datetime.strptime(request.GET.get('date'), '%Y-%m-%d')
    dreams = Dream.objects.filter(creation_date__gte=day).filter(creation_date__lte=day + timedelta(days=1))
    dreams.delete()
    # TODO: Show message
    return redirect('write')
