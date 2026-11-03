# Subir a GitHub
```powershell
git init
git branch -M main
git add .
git commit -m "feat: version final MedRecord-JTA"
git remote add origin https://github.com/TU_USUARIO/MedRecord-JTA.git
git push -u origin main
```
Verifique con `git status` que `.env` no aparezca. Nunca publique claves ni expedientes reales.
