# Arquitectura
Navegador -> FastAPI -> extracción PyPDF -> Microsoft Foundry Responses API (deployment gpt-4o) -> JSON -> dashboard. La clave solo vive en `.env` del servidor. El PDF no se persiste. Para PDFs escaneados se propone incorporar Azure AI Document Intelligence cuando la política de la suscripción lo permita.
