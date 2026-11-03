# MedRecord-JTA

Proyecto final de **Joel Tirado Aragon** que analiza expedientes clínicos PDF con **GPT-4o en Microsoft Foundry** mediante **Responses API**.

## Funciones
- Análisis automático del PDF por GPT-4o.
- Dashboard de medicamentos, alergias, estudios y completitud.
- Resumen, línea de tiempo, faltantes y alertas documentales.
- Chat basado exclusivamente en el expediente.
- Exportación JSON y PDF.
- Visor PDF e información del autor.

## Instalación
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```
En `.env`, reemplace solo `REEMPLAZA_AQUI_TU_API_KEY`. El endpoint debe terminar en `/openai/v1`, no en `/responses`.

```powershell
uvicorn app.main:app --reload
```
Abra http://127.0.0.1:8000.

## Autor
Joel Tirado Aragon  
joel203ti@gmail.com  
joel203ti-ia@labmx.ai

MedRecord-JTA no diagnostica, no prescribe y requiere validación clínica.
