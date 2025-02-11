from django.db import models

class Person(models.Model):
  name = models.CharField(max_length=100)
  photo = models.ImageField(upload_to='photo')

  def __str__(self):
    return self.name
    
class Dream(models.Model):
  tags_choices = (
    ('R', 'Realistic'),
    ('N', 'Nightmare')
  )

  # Removed title field
  # title = models.CharField(max_length=100)
  creation_date = models.DateField(auto_now_add=True)   # Changed DateTimeField to DateField
  description = models.TextField()
  persons = models.ManyToManyField(Person, null=True, blank=True)
  tags = models.TextField()

  def __str__(self):  
    return self.title
  
  def get_tags(self):
    return self.tags.split(',') if self.tags else []

  def set_tags(self, list_of_tags, reset=False):
    if not reset:
      existing_tags = set(self.get_tags())
      list_of_tags = existing_tags.union(set(list_of_tags))
    self.tags = ','.join(list_of_tags)
