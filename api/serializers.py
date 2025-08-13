from rest_framework import serializers
from .models import Note, NoteFile

# NEW: serializer for uploaded files
class NoteFileSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()

    class Meta:
        model = NoteFile
        fields = ["id", "file", "filename", "uploaded_at"]

    def get_filename(self, obj):
        return obj.file.name.split('/')[-1]

# UPDATE: NoteSerializer to include files
class NoteSerializer(serializers.ModelSerializer):
    files = NoteFileSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = ["id", "title", "body", "created", "updated", "files"]
