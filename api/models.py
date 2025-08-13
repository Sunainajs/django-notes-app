from django.db import models

# Create your models here.

class Note(models.Model):
    body = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.body[0:69]
        
        class NoteFile(models.Model):
    note = models.ForeignKey('Note', on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='note_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name.split('/')[-1]
