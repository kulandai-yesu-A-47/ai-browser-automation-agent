@echo off
cd /d %~dp0
call env\Scripts\activate
python -m uvicorn backend.main:app --reload
pause
