@echo off
cd /d %~dp0
call env\Scripts\activate
streamlit run frontend\app.py
pause
