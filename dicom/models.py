from django.db import models

# Create your models here.

class DicomData(models.Model):
    key_words = models.CharField(max_length = 100)

class DicomFiles(models.Model):
	dicom_keywords = models.ForeignKey(DicomData)
	dicom_file = models.FileField(upload_to='./images')