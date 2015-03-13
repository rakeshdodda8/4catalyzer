# 4catalyzer
To run the project

    ./manage.py makemigrations dicom
    ./manage.py migrate
    ./manage.py runserver
    RESTful API to see a list of images that were uploaded
    url: /getdata
    Method: GET
    Input Parameter: None
    Sample Output: [ 
       { 
          "key_words":"test1",
          "uploaded_files_info":[ 
             { 
                "file_name":"IMG_1272.JPG",
                "size":"285560 Bytes"
             },
             { 
                "file_name":"test.jpg",
                "size":"764 Bytes"
             }
          ]
       } 
    ] 
    
