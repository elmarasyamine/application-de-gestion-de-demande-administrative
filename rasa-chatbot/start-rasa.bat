@echo off
echo ========================================
echo    Demarrage du Chatbot Rasa
echo ========================================
echo.

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

echo [1/2] Demarrage du serveur d'actions Rasa (port 5055)...
start "Rasa Actions" cmd /k "venv\Scripts\activate.bat && rasa run actions --port 5055"

echo [2/2] Demarrage du serveur Rasa (port 5005)...
timeout /t 5 /nobreak
start "Rasa Server" cmd /k "venv\Scripts\activate.bat && rasa run --enable-api --cors * --port 5005"

echo.
echo ========================================
echo    Chatbot Rasa demarre !
echo ========================================
echo.
echo  - Serveur Rasa     : http://localhost:5005
echo  - Serveur Actions  : http://localhost:5055
echo  - API REST Webhook : http://localhost:5005/webhooks/rest/webhook
echo.
echo Pour tester en ligne de commande : rasa shell
echo.
pause
