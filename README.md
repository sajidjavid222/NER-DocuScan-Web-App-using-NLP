# NER-DocuScan-Web-App-using-NLP
Welcome to our Document Scanner Web App !!!
In this project we have developed a customized Named Entity Recognizer. The main idea of this project is to extract entities from the scanned documents like invoice, Business Card, Shipping Bill, Bill of Lading documents etc. However, for the sake of data privacy we have restricted our views to Business Card. But this framework can be used to all kinds of financial documents. Below given is the curriculum we have followed to develop this project. To develop this project we have used two main technologies of data science which are:

Computer Vision
Natural Language Processing
In Computer Vision, we have scanned the document, identified the location of text and finally extracted text from the image. Then in Natural language processing, we have extracted the entitles from the text and did necessary text cleaning and parse the entities form the text.

Python Libraries used in Computer Vision.

OpenCV
Numpy
Pytesseract
Python Libraries used in Natural Language Processing

SpaCy
Pandas
Regular Expression
String
For combining two major technologies to develop the project, we have divided architecture of this project into several stages of development.

Stage - 1 : Firstly, we have setup the project by doing the necessary installations and requirements.

Installed Python
Installed Dependencies

Stage - 2 : Secondly, we did all the data preparation. That is we have extracted the text from images using Pytesseract and also did necessary cleaning.

Gathered Images
Extracted Text from all Image
Cleaned and Prepared text

Stage - 3 : Thirdly, we have labelled the NER data using BIO tagging.

We have done labelling manually with BIO technique.
B - Beginning
I - Inside
O - Outside

Stage - 4 : Fourthly, we have further cleaned the text and preprocessed the data ( conversion from pickle format to spacy format ) for to train machine learning.
Prepared Training Data for Spacy
Converted data into spacy format

Stage - 5 : Fifthly, after preprocessing the data we have trained the Named Entity Recognition model.
Configured NER Model
Trained the model

Stage - 6 : Finally, we have predicted the entitles using NER and model and created data pipeline for parsing text.
Loaded Model
Rendered and Serve with Displacy
Drew Bounding Box on Image
Parsed Entitles from Text

Finally, we have put all together and developed the Document Scanner App
