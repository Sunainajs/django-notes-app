from django.contrib import admin
from .models import Note, NoteFile

# Keep your original Note registration
class NoteFileInline(admin.TabularInline):
    model = NoteFile
    extra = 0

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created")
    inlines = [NoteFileInline]

@admin.register(NoteFile)
class NoteFileAdmin(admin.ModelAdmin):
    list_display = ("id", "note", "file", "uploaded_at")
