from io import BytesIO
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.config import settings
from app.schemas import Question, ReportRequest
from app.services.document import extract_pdf_text
from app.services.llm import summarize, answer
app=FastAPI(title="MedRecord AI",version="2.0.0")
app.mount('/static',StaticFiles(directory='web'),name='static')
@app.get('/')
def root(): return FileResponse('web/index.html')
@app.get('/api/health')
def health(): return {'status':'ok','model':settings.azure_foundry_model,'configured':bool(settings.azure_foundry_api_key)}
@app.post('/api/analyze')
async def analyze(file:UploadFile=File(...)):
    if file.content_type!='application/pdf': raise HTTPException(415,'Solo se aceptan archivos PDF')
    data=await file.read()
    if len(data)>settings.max_upload_mb*1024*1024: raise HTTPException(413,f'El PDF supera {settings.max_upload_mb} MB')
    try: text=extract_pdf_text(data)
    except Exception as e: raise HTTPException(422,f'PDF no legible: {e}')
    if len(text.strip())<30: raise HTTPException(422,'No se extrajo texto suficiente. Use un PDF con texto seleccionable.')
    try: result=summarize(text)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(502,f"La IA no pudo completar el análisis: {repr(e)}")
    return {'filename':file.filename,'text':text,'summary':result}
@app.post('/api/ask')
def ask(q:Question):
    try: return {'answer':answer(q.question,q.document_text)}
    except Exception as e: raise HTTPException(502,f'La IA no pudo responder: {e}')
@app.post('/api/report')
def report(req:ReportRequest):
    b=BytesIO(); c=canvas.Canvas(b,pagesize=letter); width,height=letter; y=height-50
    c.setFont('Helvetica-Bold',18); c.drawString(45,y,'MedRecord AI - Informe Documental'); y-=30
    c.setFont('Helvetica',9); c.drawString(45,y,'No es diagnóstico. Requiere validación de personal clínico.'); y-=28
    for title,key in [('Resumen ejecutivo','executive_summary'),('Motivo de consulta','motivo_consulta'),('Antecedentes','antecedentes'),('Alergias','alergias'),('Medicamentos','medicamentos'),('Hallazgos','hallazgos'),('Estudios','estudios'),('Plan documentado','plan_documentado'),('Faltantes','faltantes'),('Alertas','alertas_documentales')]:
        c.setFont('Helvetica-Bold',11); c.drawString(45,y,title); y-=15
        value=req.summary.get(key,[])
        lines=[value] if isinstance(value,str) else [f'• {x}' for x in value]
        c.setFont('Helvetica',9)
        for raw in lines or ['No documentado']:
            for line in [raw[i:i+95] for i in range(0,len(raw),95)]:
                if y<55: c.showPage(); y=height-50; c.setFont('Helvetica',9)
                c.drawString(55,y,line); y-=12
        y-=9
    c.save(); b.seek(0)
    headers={'Content-Disposition':'attachment; filename=medrecord_informe.pdf'}
    return StreamingResponse(b,media_type='application/pdf',headers=headers)
