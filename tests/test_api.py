from fastapi.testclient import TestClient
from app.main import app
c=TestClient(app)
def test_health(): assert c.get('/api/health').status_code==200
def test_reject_txt(): assert c.post('/api/analyze',files={'file':('x.txt',b'x','text/plain')}).status_code==415
