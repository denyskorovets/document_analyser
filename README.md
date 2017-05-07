## Welcome to the Document Analysis Framework for Documents

This framework will classify the document type.
Currently only ".pdf" files are supported

## Instructions

In order to begin, clone the app and install requirements.txt
Then navigate to /admin, login:admin, pwd: administrator and create a new object of User to work with. You will need to know the id(primary_key) to trigger some functions (0-999999)

## How To Use 

You can easily retrive the data by going to a specific path

List of possible fucntions:

/documents_per_user/<user_primary_key> - displays all the documents per user
/documents_per_category/<category> -  displays all the documents with a certain category
/documents_with_errors_per_user/<user_primary_key> - displays documents that have validation errors per customer
/analyze/< user_primary_key>/< document_path>/< user_selected_document_type>/< document_name>/ - displays result of Analytics fucntion, 
An example of how path might look like to trigger Analyze - /analyze/1/sample3.pdf/Wage%20and%20Tax%20Statement/document1/