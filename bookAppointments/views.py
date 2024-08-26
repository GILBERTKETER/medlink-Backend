from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Appointment
import json

@csrf_exempt
def book_appointment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extract data from the request
            doctor_name = data.get('doctorName')
            speciality = data.get('speciality')
            date = data.get('date')
            time = data.get('time')
            period = data.get('period')
            consultation_type = data.get('consultationType')
            problem_description = data.get('problemDescription')
            patient_name = data.get('patientName')
            patient_email = data.get('patientEmail')
            doctor_image = data.get('doctor_image')
            # Check if the patient has already booked an appointment with the same doctor at the same time
            existing_appointment = Appointment.objects.filter(
                doctor_name=doctor_name,
                date=date,
                time=time,
                patient_email=patient_email
            ).first()

            if existing_appointment:
                return JsonResponse({
                    'status': 'error',
                    'message': 'You already have an appointment with this doctor at this time.'
                }, status=400)

            # Check if the doctor is already booked for that time
            doctor_appointment = Appointment.objects.filter(
                doctor_name=doctor_name,
                date=date,
                time=time
            ).exists()

            if doctor_appointment:
                return JsonResponse({
                    'status': 'error',
                    'message': 'The doctor is not available at this time. Please choose another time slot.'
                }, status=400)

            # Save the new appointment to the database
            appointment = Appointment.objects.create(
                doctor_name=doctor_name,
                speciality=speciality,
                date=date,
                time=time,
                period=period,
                consultation_type=consultation_type,
                problem_description=problem_description,
                patient_name=patient_name,
                patient_email=patient_email,
                doctor_image=doctor_image
            )

            return JsonResponse({
                'status': 'success',
                'appointment_id': appointment.id,
                'message':'You have successfully booked an appointment!'
            })

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def fetch_appointments(request, email):
    if request.method == 'GET':
        appointments = Appointment.objects.filter(patient_email=email) 
        appointments_list = list(appointments.values('doctor_name', 'date', 'time', 'doctor_image', 'speciality', 'problem_description', 'patient_email'))
        return JsonResponse(appointments_list, safe=False)
@csrf_exempt
def delete_appointment(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)

            # Extract data from the request to identify the appointment
            doctor_name = data.get('doctor_name')
            email = data.get('email')
            date = data.get('date')
            time = data.get('time')

            # Find and delete the specific appointment
            appointment = Appointment.objects.filter(
                doctor_name=doctor_name,
                patient_email=email,
                date=date,
                time=time
            ).first()

            if appointment:
                appointment.delete()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Appointment deleted successfully.'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Appointment not found.'
                }, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def edit_appointment(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)

            # Extract data to identify and update the appointment
            doctor_name = data.get('doctor_name')
            email = data.get('email')
            date = data.get('date')
            time = data.get('time')

            # New data for updating the appointment
            new_date = data.get('new_date')
            new_time = data.get('new_time')
            new_problem_description = data.get('problem_description')

            # Find the appointment
            appointment = Appointment.objects.filter(
                doctor_name=doctor_name,
                patient_email=email,
                date=date,
                # time=time
            ).first()

            if appointment:
                # Update the appointment details
                appointment.date = new_date or appointment.date
                appointment.time = new_time or appointment.time
                appointment.problem_description = new_problem_description or appointment.problem_description
                appointment.save()

                return JsonResponse({
                    'status': 'success',
                    'message': 'Appointment updated successfully.'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Appointment not found.'
                }, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)