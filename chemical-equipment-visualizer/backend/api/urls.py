from django.urls import path
from .views import upload_csv, history, summary, report_pdf

urlpatterns = [
    path("upload/", upload_csv, name="upload"),
    path("history/", history, name="history"),
    path("summary/<int:pk>/", summary, name="summary"),
    path("report/<int:pk>/", report_pdf, name="report"),
]
