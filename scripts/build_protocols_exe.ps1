param(
  [string]$Python = "python"
)

Write-Host "Installation de pyinstaller..."
& $Python -m pip install pyinstaller
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Build de l'exécutable Windows..."
& $Python -m PyInstaller --noconfirm --windowed --name ProtocolesSoins --add-data "data/protocols/protocols_seed.fr-CH.json;data/protocols" app_protocoles.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Terminé. Exécutable disponible dans dist/ProtocolesSoins/"
