# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from models import DicomData, DicomFiles
import json
import zipfile
import os
import subprocess

class JSONResponse(HttpResponse):

	def __init__(self, *args, **kwargs):
		super(JSONResponse, self).__init__(args, kwargs)
		self.status_code = 200
		self['Content-Type'] = 'application/json'

def view_files(request):

	dicom_objs = DicomData.objects.all()
	all_files = []
	for dicom_obj in dicom_objs:
		dicom_files = DicomFiles.objects.filter(dicom_keywords=dicom_obj)
		thumbnail = ''
		if len(dicom_files) > 0:
			tmp_thumbnail_path = dicom_files[0].dicom_file.path
			thumbnail = 'media/thumbnails/' + \
							dicom_files[0].dicom_file.name.split('/')[1].split('.')[0]+".png"
			try:
				subprocess.call("./convert_thumbnail.sh"+" "+tmp_thumbnail_path, 
								shell=True)
			except:
				print "Exception in generating thumbnail"

		tmp = [
				{'file_name': obj.dicom_file.name.split('/')[1], 'size': str(obj.dicom_file.size) + " Bytes"} 
				for obj in dicom_files
				]
		all_files.append(
						{'id': dicom_obj.id, 'key_words': dicom_obj.key_words, 'thumbnail': thumbnail, 'uploaded_files_info': tmp}
						)
	return render_to_response("view.html", {'info': all_files}, 
								context_instance=RequestContext(request))

def upload(request):

	if request.method == 'POST':
		try:
			obj = DicomData(key_words=request.POST.get('keywords'))
			obj.save()
			
			files_names = request.FILES.getlist('files')
			for temp_file in files_names:
				dicomObj = DicomFiles(dicom_keywords=obj, dicom_file=temp_file)
				dicomObj.save()

			return HttpResponseRedirect(reverse('view_files'),)
		except Exception, e:
			return HttpResponseRedirect(reverse('view_files'),)

def download_zip(request):

	obj = DicomData.objects.get(id=request.GET.get('id'))
	dicom_files = DicomFiles.objects.filter(dicom_keywords=obj)

	zip_name = obj.key_words.split()[0] + "_" + str(obj.id)
	zip_path = './templates/media/images/%s.zip' %(zip_name)
	zipf = zipfile.ZipFile(zip_path, 'w')

	from os.path import basename
	for dicom_file in dicom_files:
		zipf.write(dicom_file.dicom_file.path,basename(dicom_file.dicom_file.path))
	zipf.close()

	from django.core.servers.basehttp import FileWrapper
	filename = zip_path
	wrapper = FileWrapper(file(filename))
	response = HttpResponse(wrapper, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=%s' %(filename.split("/")[-1])
	response['Content-Length'] = os.path.getsize(filename)
	os.remove(filename)
	return response

# Api to get all uploaded files

def view_data_api(request):

	all_files = []
	for dicom_obj in DicomData.objects.all():
		dicom_files = DicomFiles.objects.filter(dicom_keywords=dicom_obj)
		thumbnail = 'media/thumbnails/' + \
							dicom_files[0].dicom_file.name.split('/')[1].split('.')[0]+".png"
		tmp = [ 
				{'file_name': obj.dicom_file.name.split('/')[1], 'size': str(obj.dicom_file.size) + " Bytes"} 
				for obj in dicom_files 
				]
		all_files.append({'key_words': dicom_obj.key_words, 'thumbnail': thumbnail,
							'uploaded_files_info': tmp})

	return JSONResponse(json.dumps(all_files))
