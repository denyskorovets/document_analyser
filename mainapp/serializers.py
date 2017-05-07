from rest_framework import serializers
from mainapp.models import Document, Error


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'document_text', 'type_of_document')

    def create(self, validated_data):
        """
        Create and return a new `Document` instance, given the validated data.
        """
        return Document.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Document` instance, given the validated data.
        """
        instance.document_text = validated_data.get('document_text', instance.document_text)
        instance.type_of_document = validated_data.get('type_of_document', instance.type_of_document)
        instance.save()
        return instance


class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Error
        fields = ('id', 'type_of_error')

    def create(self, validated_data):
        """
        Create and return a new `Error` instance, given the validated data.
        """
        return Error.objects.create(**validated_data)
