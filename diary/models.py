from django.db import models

class Person(models.Model):
  name = models.CharField(max_length=100)
  photo = models.ImageField(upload_to='photo')

  def __str__(self):
    return self.name
    
class Diary(models.Model):
  tags_choices = (
    ('T', 'Travel'),
    ('W', 'Work')
  )

  title = models.CharField(max_length=100)
  tags = models.TextField()
  persons = models.ManyToManyField(Person, null=True, blank=True)
  text = models.TextField()
  creation_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title
  
  def get_tags(self):
    return self.tags.split(',') if self.tags else []

  def set_tags(self, list_of_tags, reset=False):
    if not reset:
      existing_tags = set(self.get_tags())
      list_of_tags = existing_tags.union(set(list_of_tags))
    self.tags = ','.join(list_of_tags)
