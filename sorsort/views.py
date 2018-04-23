from django.shortcuts import render
import openpyxl
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UploadFileForm, UploadFileForm2, UploadFileForm3
import csv
from wsgiref.util import FileWrapper
import os, io, re





def home(request):
	if request.method == 'POST':
		file_path = io.open('./sorsort/temp.csv','rb')
		response = HttpResponse(file_path, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename='+ str('greektemplate.csv')
		return(response)
	else:
		return render(request, 'sorsort/home.html', {})


#First system request forms
def first(request):
	print('in upload', request)
	if request.method == 'POST':
		print(request.content_params)
		form = UploadFileForm(request.POST, request.FILES)
		print('new form')
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			result = greekday()
			if not result:
				# redirect to error
				return render(request, 'sorsort/rush.html', {'form': form, 'error':'Excel not compatible! Check formatting standards and save as CSV!'})
			file_path = io.open('./results/CHART.csv','rb')
			response = HttpResponse(file_path, content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename='+ str('greekdayseating.csv')
			return(response)

	else:
		form = UploadFileForm()
		return render(request, 'sorsort/rush.html', {'form': form})


#File upload handling
def handle_uploaded_file(f):
	#csvRegex = re.compile(r'.csv$')
	#mo = csvRegex.search(str(f))
	#print(mo[0])
	with open('./dataToProcess/user.csv', 'wb+') as destination:
	    for chunk in f.chunks():
	    	#print('here', chunk)
	    	destination.write(chunk)





#Logic behind greekday sort
def greekday():
	csv_fileh = open("./dataToProcess/user.csv","r",encoding='utf-8', errors='ignore')
	try:
		dialect = csv.Sniffer().sniff(csv_fileh.read(1024))
		csv_fileh.seek(0)
	except csv.Error:
		return False


	rush = list(csv.DictReader(open("./dataToProcess/user.csv","r",encoding='utf-8', errors='ignore')))

	commands = ['ID','Last Name', 'First Name',	'Legacy', 'Group #', 'Total', 'State']
	keys = rush[0].keys()
	for c in commands:
		if c not in keys:
			return False


	for row in rush:
		print(row)
		print(row["Total"])
		row["Total"] = int(row["Total"])
		if row["Legacy"] == 'Yes':
			row["Total"] += 50
	rush = sorted(rush, key= lambda x: x['Total'], reverse=True)

	groups = [[] for x in range(12)]
	for row in rush:
		groups[int(row['Group #'])-1].append(row)
	print(groups)

	myFile = open('./results/CHART.csv', 'w')
	with myFile:
		writer = csv.writer(myFile, delimiter=",", dialect="excel", lineterminator="\n")
		writer.writerow(["Table","Seat", "Name","Group #"])

		for x in groups:
			count = 0
			writer.writerow("\n")
			number = 1
			table = 1
			for y in x:
				writer.writerow([(count//8)+1]+[number]+[y['First Name'] + " " + y['Last Name']+ " "+ y['State']] +[y['Group #']])
				if number != 8:
					number += 1
				else:
					number = 1
				count += 1

	return True





#Philanthropy round starts below ------------------------------------------------------------------


def second(request):
	print('in upload', request)
	if request.method == 'POST':
		form2 = UploadFileForm2(request.POST, request.FILES)
		print('new form')
		if form2.is_valid():
			handle_uploaded_file2(request.FILES['file2'])
			phil()
			file_path = io.open('./results/philCHART.csv','rb')
			response = HttpResponse(file_path, content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename='+ str('phildayseating.csv')
			return(response)
	else:
		form2 = UploadFileForm2()
		return render(request, 'sorsort/phil.html', {'form2': form2})



def handle_uploaded_file2(f2):
	with open('./dataToProcess/userp.csv', 'wb+') as destination:
	    for chunk in f2.chunks():
	    	#print('here', chunk)
	    	destination.write(chunk)



def phil():
	
	rush = list(csv.DictReader(open('./dataToProcess/userp.csv',"r",encoding='utf-8', errors='ignore')))
	rush = sorted(rush, key= lambda x: float(x['Total score']), reverse=True)

	groups = [[] for x in range(12)]
	for row in rush:
		groups[int(row['Group #'])-1].append(row)
	print(groups)
	# Create output excel file of sorted women
	myFile = open('./results/philCHART.csv', 'w')
	with myFile:
		writer = csv.writer(myFile, delimiter=",", dialect="excel", lineterminator="\n")
		writer.writerow(["Table","Seat", "Name","Group #"])
		for x in groups:
			count = 0
			writer.writerow("\n")
			number = 1
			table = 1
			for y in x:
				writer.writerow([(count//8)+1]+[number]+[y['First Name'] + " " + y['Last Name']] +[y['Group #']])
				if number != 8:
					number += 1
				else:
					number = 1
				count += 1














#Sisterhood round starts below ------------------------------------------------------------------


def third(request):
	print('in upload', request)
	if request.method == 'POST':
		form3 = UploadFileForm3(request.POST, request.FILES)
		print('new form')
		if form3.is_valid():
			handle_uploaded_file3(request.FILES['file3'])
			sister()
			file_path = io.open('./results/sisCHART.csv','rb')
			response = HttpResponse(file_path, content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename='+ str('sisseating.csv')
			return(response)
	else:
		form3 = UploadFileForm3()
		return render(request, 'sorsort/sister.html', {'form3': form3})



def handle_uploaded_file3(f3):
	with open('./dataToProcess/userssp.csv', 'wb+') as destination:
	    for chunk in f3.chunks():
	    	#print('here', chunk)
	    	destination.write(chunk)



def sister():
	rush = list(csv.DictReader(open('./dataToProcess/userssp.csv',"r",encoding='utf-8', errors='ignore')))
	rush = sorted(rush, key= lambda x: float(x['Total score']), reverse=True)

	groups = [[] for x in range(12)]
	for row in rush:
		groups[int(row['Group #'])-1].append(row)
	print(groups)
	# Create output excel file of sorted women
	myFile = open('./results/sisCHART.csv', 'w')
	with myFile:
		writer = csv.writer(myFile, delimiter=",", dialect="excel", lineterminator="\n")
		writer.writerow(["Table","Seat", "Name","Group #"])
		for x in groups:
			count = 0
			writer.writerow("\n")
			number = 1
			table = 1
			for y in x:
				writer.writerow([(count//4)+1]+[number]+[y['First Name'] + " " + y['Last Name']] +[y['Group #']])
				if number != 4:
					number += 1
				else:
					number = 1
				count += 1
