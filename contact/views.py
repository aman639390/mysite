from django.shortcuts import render
from .forms import ContactForm
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone

def contact_view(request):
    sent = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()

            # Plain text fallback
            text_message = f"""
New Contact Form Message:

Name: {msg.name}
Email: {msg.email}
Subject: {msg.subject}
Message:
{msg.message}
            """

            # Professional HTML Email
            html_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background:#f4f6fa; padding:20px;">
                <div style="max-width:600px; margin:auto; background:white; padding:25px; border-radius:10px;
                            box-shadow:0 4px 12px rgba(0,0,0,0.15);">

                    <h2 style="color:#0077ff; text-align:center; margin-top:0;">
                        ✨ New Contact Message
                    </h2>

                    <p style="font-size:15px; color:#333;">
                        You received a new message from your portfolio contact form.
                    </p>

                    <hr style="border:0; height:1px; background:#ddd; margin:15px 0;">

                    <p><strong>Name:</strong> {msg.name}</p>
                    <p><strong>Email:</strong> {msg.email}</p>
                    <p><strong>Subject:</strong> {msg.subject}</p>

                    <p style="margin-top:15px;"><strong>Message:</strong></p>
                    <div style="background:#f0f7ff; padding:12px; border-left:4px solid #0077ff; border-radius:6px;">
                        {msg.message}
                    </div>

                    <p style="font-size:13px; color:#777; margin-top:20px; text-align:right;">
                        Received on {timezone.now().strftime("%d %B %Y • %I:%M %p")}
                    </p>

                </div>
            </body>
            </html>
            """

            email = EmailMultiAlternatives(
                subject=f"New Contact Message from {msg.name}",
                body=text_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[settings.EMAIL_HOST_USER]
            )
            email.attach_alternative(html_message, "text/html")
            email.send()

            sent = True
            form = ContactForm()

    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form, "sent": sent})
