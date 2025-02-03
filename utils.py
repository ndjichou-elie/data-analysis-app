import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from django.core.mail import send_mail

def send_notification_email(subject, message, recipient_email):
    try:
        send_mail(
            subject,
            message,
            'your-email@gmail.com',  # Sender's email
            [recipient_email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")


def generate_visualizations(data):
    """
    Generate visualizations for the uploaded data.
    Returns a dictionary of base64-encoded images.
    """
    visualizations = {}

    # Example: Correlation Heatmap
    if not data.empty and data.select_dtypes(include=['number']).shape[1] > 1:
        corr = data.corr()
        plt.figure(figsize=(8, 6))
        plt.imshow(corr, cmap='coolwarm', interpolation='none')
        plt.colorbar()
        plt.title("Correlation Heatmap")
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        visualizations['correlation_heatmap'] = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

    # Add more visualizations as needed (e.g., bar charts, pie charts)
    return visualizations
