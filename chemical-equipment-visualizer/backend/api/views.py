import io
import os
import pandas as pd
from django.http import FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors

from .models import Dataset
from .serializers import DatasetSerializer


def _compute_summary(df: pd.DataFrame):
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    required = ["Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")

    numeric_cols = ["Flowrate", "Pressure", "Temperature"]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    total_count = len(df)
    averages = {c: float(df[c].mean(skipna=True)) for c in numeric_cols}

    type_counts = df["Type"].fillna("Unknown").value_counts().sort_index()
    type_distribution = [{"type": str(t), "count": int(v)} for t, v in type_counts.items()]

    preview = df.head(20).fillna("").to_dict(orient="records")

    return {
        "total_count": total_count,
        "averages": averages,
        "type_distribution": type_distribution
    }, list(df.columns), preview


def _enforce_last_five():
    ids = list(Dataset.objects.order_by("-created_at").values_list("id", flat=True))
    for old_id in ids[5:]:
        try:
            obj = Dataset.objects.get(pk=old_id)
            if obj.csv_file and os.path.exists(obj.csv_file.path):
                os.remove(obj.csv_file.path)
            obj.delete()
        except:
            pass


@csrf_exempt
@api_view(["POST"])
def upload_csv(request):
    file = request.FILES.get("file")
    if not file:
        return Response({"detail": "No file uploaded."}, status=400)

    try:
        df = pd.read_csv(file, encoding="utf-8")
        df.columns = df.columns.str.strip()
        summary, columns, preview = _compute_summary(df)

    except Exception as e:
        print("\n\n### CSV ERROR ###")
        print(e)
        print("#################\n\n")
        return Response({"detail": f"Failed to parse CSV: {e}"}, status=400)

    file.seek(0)
    dataset = Dataset.objects.create(
        csv_file=file,
        original_filename=file.name,
        summary_json=summary,
        preview_rows=preview,
        columns=columns,
    )

    _enforce_last_five()

    return Response({
        "id": dataset.id,
        "summary": summary,
        "columns": columns,
        "preview_rows": preview,
        "message": "Upload successful"
    }, status=201)


@api_view(["GET"])
def history(request):
    qs = Dataset.objects.order_by("-created_at")[:5]
    return Response(DatasetSerializer(qs, many=True).data)


@api_view(["GET"])
def summary(request, pk: int):
    try:
        ds = Dataset.objects.get(pk=pk)
    except Dataset.DoesNotExist:
        raise Http404("Dataset not found")

    return Response({
        "id": ds.id,
        "original_filename": ds.original_filename,
        "summary": ds.summary_json,
        "columns": ds.columns,
        "preview_rows": ds.preview_rows,
    })


@api_view(["GET"])
def report_pdf(request, pk: int):
    try:
        ds = Dataset.objects.get(pk=pk)
    except Dataset.DoesNotExist:
        raise Http404("Dataset not found")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=40)
    styles = getSampleStyleSheet()
    story = []

    # Center Title
    title_style = styles["Title"]
    title_style.alignment = 1
    story.append(Paragraph("Chemical Equipment Parameter Report", title_style))
    story.append(Spacer(1, 20))

    # Dataset Info (Left-aligned)
    info_style = styles["Normal"]
    info_style.alignment = 0
    story.append(Paragraph(f"<b>Dataset ID:</b> {ds.id}", info_style))
    story.append(Paragraph(f"<b>File:</b> {ds.original_filename}", info_style))
    story.append(Spacer(1, 18))

    # Summary Table
    s = ds.summary_json
    table_data = [
        ["Total Count", s["total_count"]],
        ["Avg Flowrate", f"{s['averages']['Flowrate']:.2f}"],
        ["Avg Pressure", f"{s['averages']['Pressure']:.2f}"],
        ["Avg Temperature", f"{s['averages']['Temperature']:.2f}"],
    ]

    tbl = Table(table_data, colWidths=[130, 130])
    tbl.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.7, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("ALIGN", (0,0), (-1,-1), 'CENTER'),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica")
    ]))
    story.append(tbl)
    story.append(Spacer(1, 30))

    # Chart Title
    chart_title = styles["Heading2"]
    chart_title.alignment = 1
    story.append(Paragraph("Equipment Type Distribution", chart_title))
    story.append(Spacer(1, 10))

    # Generate Chart
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import tempfile

        dist = s["type_distribution"]
        types = [t["type"] for t in dist]
        counts = [t["count"] for t in dist]

        fig, ax = plt.subplots(figsize=(5.5, 3.5))
        ax.bar(types, counts, color="skyblue")
        ax.set_ylabel("Count")
        ax.set_xlabel("Type")
        fig.tight_layout()

        tmp = tempfile.gettempdir()
        chart_path = os.path.join(tmp, f"chart_{ds.id}.png")
        fig.savefig(chart_path, dpi=200)
        plt.close(fig)

        story.append(Image(chart_path, width=420, height=250))
    except Exception as e:
        story.append(Paragraph(f"(Chart could not be generated: {e})", styles["Italic"]))

    doc.build(story)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"report_{ds.id}.pdf")