from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NoteSerializer
from .models import Note

# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting note'
        },
    ]
    return Response(routes)

@api_view(['GET'])
def getNotes(request):
    notes = Note.objects.all().order_by('-created')
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getNote(request, pk):
    note = Note.objects.get(id=pk)
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateNote(request, pk):
    note = Note.objects.get(id=pk)
    serializer = NoteSerializer(instance=note, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteNote(request, pk):
    note = Note.objects.get(id=pk)
    note.delete()
    return Response('Note was deleted!')

@api_view(['POST'])
def createNote(request):
    data = request.data
    note = Note.objects.create(
        body=data['body']
    )
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)
    # api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Note, NoteFile
from .serializers import NoteFileSerializer

class NoteFileUploadView(APIView):
    permission_classes = [permissions.AllowAny]  # match your existing policy

    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        files = request.FILES.getlist('files')
        created_files = []
        for f in files:
            nf = NoteFile.objects.create(note=note, file=f)
            created_files.append(nf)
        return Response(
            NoteFileSerializer(created_files, many=True).data,
            status=status.HTTP_201_CREATED
        )

class NoteFileListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        qs = note.files.order_by("-uploaded_at")
        return Response(NoteFileSerializer(qs, many=True).data)

class NoteFileDeleteView(APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request, file_id):
        nf = get_object_or_404(NoteFile, pk=file_id)
        nf.file.delete(save=False)  # delete from storage
        nf.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
