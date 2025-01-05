from django.core.mail import send_mail
from django.shortcuts import render, redirect
from.models import Projects
from django.utils import timezone
import random

# Temporary storage for verification codes
from django.shortcuts import render
from django.core.mail import send_mail
import random

# A dictionary to temporarily store verification codes
import random
import string
from django.core.mail import send_mail
from django.shortcuts import render

# A dictionary to store verification codes (can also use session or database)
import random
import string
from django.core.mail import send_mail
from django.shortcuts import render

verification_codes = {}

# Function to generate a random verification code
def generate_code():
    # Generates a 6-digit random verification code
    return ''.join(random.choices(string.digits, k=6))

def index(request):
    if request.method == "POST":
        if "send_code" in request.POST:
            # Handle the "Send Verification Code" action
            email = request.POST.get("email")
            if not email:
                return render(request, "index.html", {"error": "Email is required."})

            # Generate and store the verification code
            code = generate_code()
            verification_codes[email] = code

            # Send the verification code via email
            send_mail(
                "Your Verification Code",
                f"Your verification code is: {code}",
                "danielebong180@gmail.com",
                [email],
            )

            # Store the email in session to keep it after refresh
            request.session['email'] = email

            return render(request, "index.html", {
                "info_message": "Verification code sent successfully!",  # Use a different key
                "email": email
            })
        
        elif "submit_form" in request.POST:
            # Handle the form submission
            name = request.POST.get("name")
            email = request.POST.get("email")
            message = request.POST.get("message")
            verification_code = request.POST.get("verification_code")

            # Validate the verification code
            if email not in verification_codes or verification_codes[email] != verification_code:
                return render(request, "index.html", {"error": "Invalid verification code."})

            # Send the contact email
            send_mail(
                f"Contact Form Submission from {name}",
                f"Message: {message}\nEmail: {email}",
                "danielebong180@gmail.com",
                ["danielebong180@gmail.com"],
            )

            # Remove the used verification code
            verification_codes.pop(email, None)

            # Clear the session data after the form is submitted successfully
            request.session.flush()

            # Store the name, email, and message in the session to show them in the template
            request.session['name'] = name
            request.session['email'] = email
            request.session['user_message'] = message

            return render(request, "index.html", {
                "success_message": "Message sent successfully!",  # Use a different key
                "name": name,
                "email": email,
                "message": message
            })
    
    # If GET request or after form submission, retrieve the session data
    name = request.session.get('name', '')
    email = request.session.get('email', '')
    message = request.session.get('user_message', '')  # Use 'user_message' for the user's input

    return render(request, "index.html", {
        "name": name,
        "email": email,
        "message": message
    })






def projects(request):
    # Get the search query from the request
    search_name = request.GET.get('search_name', '')
    search_price = request.GET.get('search_price', '')

    # Filter the projects based on the search query
    projects = Projects.objects.all()

    if search_name:
        projects = projects.filter(name__icontains=search_name)  # Case-insensitive search for name

    if search_price:
        try:
            search_price = float(search_price)
            projects = projects.filter(price=search_price)  # Exact match for price
        except ValueError:
            pass  # If price can't be converted to float, do not apply price filter

    # Sort the projects by date (optional)
    projects = projects.order_by('-created_at')

    return render(request, 'projects.html', {'projects': projects, 'search_name': search_name, 'search_price': search_price})


