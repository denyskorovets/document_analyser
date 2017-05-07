from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from mainapp.models import Document, User, Error
from mainapp.serializers import DocumentSerializer
from rest_framework import status
from rest_framework.decorators import api_view


def index(request):
    response = "Possible routes to check:  /documents_per_user/<user_primary_key> - all the documents per user, " \
               "/documents_per_category/<category> -  all the documents with a certain category , " \
               "/documents_with_errors_per_user/<user_primary_key> - documents that have validation errors per customer" \
               ", /analyze/< user_primary_key>/< document_path>/< user_selected_document_type>/< document_name>/ - " \
               "displays result of Analytics fucntion, example of how path might look like to trigger it " \
               "/analyze/1/sample3.pdf/Wage%20and%20Tax%20Statement/document1/"
    return HttpResponse(response)


@api_view(['GET'])
def document_list(request, format=None):
    """
    List all documents.
    """
    try:
        document = Document.DocumentManager.all()
    except Document.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DocumentSerializer(document, many=True)
        # Might be substituted for JsonResponse(safe=False)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def document_detail(request, pk_document):
    """
    List a specific document by provided ID.
    """
    try:
        document = Document.DocumentManager.get(pk=pk_document)
    except Document.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DocumentSerializer(document, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def documents_per_user(request, pk_user):
    """
    List all documents per specific user.
    """
    user = __find_user(pk_user)
    if user is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        document = Document.DocumentManager.filter(user=user)
        serializer = DocumentSerializer(document, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def documents_per_category(request, category):
    """
    List all documents per specific user.
    """
    try:
        documents = Document.DocumentManager.filter(type_of_document=category)
    except Document.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def documents_with_errors_per_user(request, pk_user):
    """
    List all documents with errors for a specific user.
    """
    user = __find_user(pk_user)
    if user is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        all_documents = Document.DocumentManager.filter(user=user)
        list_of_error_documents = []
        for document in all_documents:
            errors = Error.objects.filter(document=document)
            for error in errors:
                if error.type_of_error is not "clean":
                    list_of_error_documents.append(document)
                else:
                    break
        serializer = DocumentSerializer(list_of_error_documents, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# I have made this function into an api_view format for testing purposes
@api_view(['GET'])
def analyze(request, pk_user, doc_path, user_selected_document_type, document_name):
    # Before we can begin the analysis we need to find the User object who submitted this document
    user = __find_user(pk_user)

    # If we didn't find an existing user in db, returns an error. Also, this can be extended to create a new User object
    if user is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        new_doc = __create_document(user, doc_path, document_name, user_selected_document_type)
        predicted_category = Document.DocumentManager.analyse_doc_type(new_doc)
        if "WARNING" in predicted_category:
            print("WARNING", predicted_category)
            return HttpResponse(predicted_category)
        else:
            document_to_save = __save_document(new_doc, predicted_category)
            return HttpResponse(document_to_save.type_of_document)


def __create_document(user, doc_path, document_name, user_selected_document_type):
    """
    Creates a new document instance with given parameters and returns the document object.
    """
    document = Document.DocumentManager.create_doc(user, doc_path, document_name, user_selected_document_type)
    return document


def __save_document(new_doc, predicted_category):
    document = Document.DocumentManager.update_document_type(new_doc, predicted_category)
    return document


def __find_user(user_pk):
    try:
        user = User.objects.filter(pk=user_pk).first()
        return user
    except Document.DoesNotExist:
        return False


