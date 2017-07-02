@echo off

:parse
IF "%~1"=="" (
   GOTO param_missing
) ELSE (
   GOTO launch
)

:launch
python manage.py runserver 0.0.0.0:%~1
GOTO end

:param_missing
echo Missing parameter : port
GOTO end

:end
echo End

pause
