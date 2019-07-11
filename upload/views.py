import io
from django.shortcuts import render, HttpResponse
import csv
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .models import Contact


@permission_required('admin.can_add_log_entry')
def contact_upload(request):
    template = "contact_upload.html"
    prompt = {
        'order': 'Order of csv should be first_name,last_name,email,ip_address,messsage'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'this is not a csv file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        if column:
            _, created = Contact.objects.update_or_create(
                first_name=column[0],
                last_name=column[1],
                email=column[2],
                ip_address=column[3],

            )
    context = {}
    return render(request, template, context)


@permission_required('admin.can_add_log_entry')
def contact_download(request):
    items = Contact.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contact.csv"'
    writer = csv.writer(response, delimiter=',')
    writer.writerow(['first_name', 'last_name', 'email', 'ip_address'])
    for obj in items:
        writer.writerow([obj.first_name, obj.last_name, obj.email, obj.ip_address])
    return response