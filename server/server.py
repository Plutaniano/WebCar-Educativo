import requests

from flask import Flask, render_template, request
from flask_api import status

app = Flask(__name__)

# ===============
#    back-end
# ===============
arduino_addr = '127.0.0.1'
arduino_port = 50

@app.route('/conectar')
def conectar():
    arduino_addr = request.args.get('addr')
    arduino_port = request.args.get('port')

    if arduino_port != None and arduino_addr != None:
        print(f'[ERRO]\t WebCar tentou conectar sem IP e porta.')
        return 'erro'

    print(f'WebCar conectado. [{arduino_addr}:{arduino_port}]')
    return 'ok', status.HTTP_200_OK

@app.route('/buzzer')
def buzzer():
    try:
        freq = int(request.args.get('freq'))
        sec = int(request.args.get('sec'))
        if (freq == None and sec == None) or\
            not (0 <= freq <= 5000) or\
            sec > 10:
            raise ValueError
    except:
        return "Frequência e/ou tempo invalido(s).", status.HTTP_400_BAD_REQUEST        

    r = requests.get(f'{arduino_addr}:{arduino_port}/buzzer?freq={freq}&sec={sec}')
    return r.status_code

@app.route('/led')
def led():
    action = request.args.get('action')
    value = request.args.get('value')

    if action not in ['set', 'toggle'] or (action == 'set' and value == None):
        return "Action invalida.", status.HTTP_400_BAD_REQUEST

    if action == 'toggle':
        r = requests.get(f'{arduino_addr}:{arduino_port}/ledtoggle')
    
    if action == 'set':
        if value == 1:
            value = 'on'
        else:
            value = 'off'

        r = request.get(f'{arduino_addr}:{arduino_port}/led{value}')
    
    return r.status_code


# ================
#    front-end
# ================

@app.route('/')
def inicio():
    return render_template('content_template.html', content='paginas/inicio.html')

@app.route('/guia')
def guia():
    return render_template('content_template.html', content='paginas/guia.html')

@app.route('/controle')
def controle():
    return render_template('content_template.html', content='paginas/controle.html')

@app.route('/programacao')
def programacao():
    return render_template('content_template.html', content='paginas/programacao.html')

@app.route('/sobre')
def sobre():
    return render_template('content_template.html', content='paginas/sobre.html')

@app.route('/componentes')
def componentesroot():
    return render_template('content_template.html', content='paginas/componentes.html')

@app.route('/componentes/<componente>')
def componentes(componente):
    return render_template('content_template.html', componente=componente, content=f'/componentes/{componente}.html')

app.run(host='127.0.0.1', port='5000', debug=True)
