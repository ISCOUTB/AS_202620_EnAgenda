#Evidencias de Corte Vertical 


## Intalacion de Dependencias
```text
PS C:\Users\Jeimy Mendez A\Documents\Uni\Arq_Software\AS_202620_EnAgenda> python -m pip install -r requerimiento.txt
Requirement already satisfied: pytest<9.0,>=8.0 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from -r requerimiento.txt (line 1)) (8.4.2)
Requirement already satisfied: Flask==3.1.3 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from -r requerimiento.txt (line 2)) (3.1.3)
Requirement already satisfied: blinker>=1.9.0 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from Flask==3.1.3->-r requerimiento.txt (line 2)) (1.9.0)
Requirement already satisfied: click>=8.1.3 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from Flask==3.1.3->-r requerimiento.txt (line 2)) (8.5.0)
Requirement already satisfied: itsdangerous>=2.2.0 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from Flask==3.1.3->-r requerimiento.txt (line 2)) (2.2.0)
Requirement already satisfied: jinja2>=3.1.2 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from Flask==3.1.3->-r requerimiento.txt (line 2)) (3.1.6)
Requirement already satisfied: markupsafe>=2.1.1 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from Flask==3.1.3->-r requerimiento.txt (line 2)) (3.0.3)
Requirement already satisfied: werkzeug>=3.1.0 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from Flask==3.1.3->-r requerimiento.txt (line 2)) (3.1.8)
Requirement already satisfied: colorama>=0.4 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from pytest<9.0,>=8.0->-r requerimiento.txt (line 1)) (0.4.6)
Requirement already satisfied: iniconfig>=1 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from pytest<9.0,>=8.0->-r requerimiento.txt (line 1)) (2.3.0)
Requirement already satisfied: packaging>=20 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from pytest<9.0,>=8.0->-r requerimiento.txt (line 1)) (26.3)
Requirement already satisfied: pluggy<2,>=1.5 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from pytest<9.0,>=8.0->-r requerimiento.txt (line 1)) (1.6.0)
Requirement already satisfied: pygments>=2.7.2 in C:\Users\Jeimy Mendez A\AppData\Local\Programs\Python\Python313\Lib\site-packages (from pytest<9.0,>=8.0->-r requerimiento.txt (line 1)) (2.21.0)
```


## Puebas ejecutables desde el terminal
```text
PS C:\Users\Jeimy Mendez A\Documents\Uni\Arq_Software\AS_202620_EnAgenda> pytest -q
......                                                                                                                              [100%]
6 passed in 0.16s
```

## Ejecucion de Aplicacion
```text
PS C:\Users\Jeimy Mendez A\Documents\Uni\Arq_Software\AS_202620_EnAgenda> python app\web.py
 * Serving Flask app 'web'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 144-640-716
 ```