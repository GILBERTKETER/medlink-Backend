from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Timelines
from django.utils.dateparse import parse_time

@csrf_exempt
def set_reminder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            patient_email = data.get('patient_email')
            date = data.get('date')
            time_str = data.get('time')  
            long_description = data.get('long_description')
            description = data.get('description')
            patient_name = data.get('patient_name')

            time = parse_time(time_str)
            if time is None:
                return JsonResponse({'status': 'error', 'message': 'Invalid time format. Use HH:MM format.'}, status=400)

            existing_reminder = Timelines.objects.filter(patient_email=patient_email, date=date, time=time).first()
            if existing_reminder:
                return JsonResponse({'status': 'error', 'message': 'You already have a reminder at this time.'}, status=403)

            Timelines.objects.create(
                patient_email=patient_email,
                patient_name=patient_name,
                description=description,
                date=date,
                time=time,
                long_description=long_description
            )
            return JsonResponse({'status': 'success', 'message': 'You have successfully added a timeline. You will be reminded!'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid Data'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'}, status=500)

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def get_reminders(request, email):
    if request.method == 'GET':
        reminders = Timelines.objects.filter(patient_email=email) 
        reminders_list = list(reminders.values('date', 'time', 'description', 'patient_name', 'patient_email', 'long_description'))
        return JsonResponse(reminders_list, safe=False)