from django.urls import path
from . import views
from .views import NoteFileUploadView, NoteFileListView, NoteFileDeleteView

urlpatterns = [
    # your existing endpoints
    path('notes/', views.getNotes),
    path('notes/<str:pk>/', views.getNote),

    # NEW: file endpoints
    path('notes/<int:pk>/files/', NoteFileListView.as_view(), name='note-file-list'),
    path('notes/<int:pk>/files/upload/', NoteFileUploadView.as_view(), name='note-file-upload'),
    path('files/<int:file_id>/', NoteFileDeleteView.as_view(), name='note-file-delete'),
]
