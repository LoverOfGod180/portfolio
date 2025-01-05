from django.core.mail import send_mail
from django.shortcuts import render, redirect
from.models import Projects
from django.utils import timezone
import random
import string

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
    """Generate a 6-digit verification code."""
    return str(random.randint(100000, 999999))

def index(request):
    if request.method == "POST":
        if "send_code" in request.POST:
            # Handle the "Send Verification Code" action
            email = request.POST.get("email")
            name = request.POST.get("name")
            message = request.POST.get("message")
            
            # Ensure all required fields are filled
            if not email or not name or not message:
                return render(request, "index.html", {"error": "All fields are required."})
            
            # Store the form data in session so it persists after page refresh
            request.session['email'] = email
            request.session['name'] = name
            request.session['message'] = message

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
            
            return render(request, "index.html", {
                "msg": "Verification code sent successfully!",
                "email": email,
                "name": name,
                "message_content": message
            })
        
        elif "submit_form" in request.POST:
            # Handle the form submission after verification code
            name = request.POST.get("name")
            email = request.POST.get("email")
            message = request.POST.get("message")
            verification_code = request.POST.get("verification_code")

            # Validate the verification code
            if email not in verification_codes or verification_codes[email] != verification_code:
                return render(request, "index.html", {"error": "Invalid verification code."})

            # Send the contact form submission email
            send_mail(
                f"Contact Form Submission from {name}",
                f"Message: {message}\nEmail: {email}",
                "danielebong180@gmail.com",
                ["danielebong180@gmail.com"],
            )

            # Remove the used verification code
            verification_codes.pop(email, None)

            # Clear session data after successful form submission
            request.session.pop('email', None)
            request.session.pop('name', None)
            request.session.pop('message', None)

            return render(request, "index.html", {
                "msg": "Message sent successfully!"
            })

    # Get session data to preserve input fields after refresh
    email = request.session.get('email', '')
    name = request.session.get('name', '')
    message_content = request.session.get('message', '')

    return render(request, "index.html", {
        "email": email,
        "name": name,
        "message_content": message_content
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
