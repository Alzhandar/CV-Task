from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    share_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'message', 'attachment', 'created_at', 'share_url']
        read_only_fields = ['created_at', 'share_url']

    def get_share_url(self, obj):
        request = self.context.get('request')
        if request and obj.id:
            return request.build_absolute_uri(f'/contact/share/{obj.id}/')
        return None