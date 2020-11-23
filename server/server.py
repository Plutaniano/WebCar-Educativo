# biblioteca requests, para realizar requests HTTP
import requests

# biblioteca Flask, responsavel por rodar o webserver
from flask import Flask, render_template, request
from flask_api import status

# criação do objeto app, onde o webserver irá rodar
app = Flask(__name__)

# ===============
#    back-end
# ===============

# inicialização do endereço do arduino para valores padrões
arduino_addr = '192.168.1.75'
arduino_port = 80

# /conectar
# recebe parametros para estabelecer IP e porta do carro
@app.route('/conectar')
def conectar():
    arduino_addr = request.args.get('addr')
    arduino_port = request.args.get('port')

    if arduino_port == None and arduino_addr == None:
        print(f'[ERRO]\t WebCar tentou conectar sem IP e porta.')
        return 'erro'

    print(f'WebCar conectado. [{arduino_addr}:{arduino_port}]')
    return 'ok', status.HTTP_200_OK

# /buzzer
# recebe frequencia e duração do som
# filtra para valores aceitaveis e envia comando ao carro
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

    r = requests.get(f'http://{arduino_addr}:{arduino_port}/buzzer?freq={freq}&sec={sec}')
    return str(r.status_code)

# /move
# recebe direção (frente, trás) e lado (direita, esquerda, None) que carrinho deve se mover
@app.route('/move')
def move():
    dir = request.args.get('dir')
    side = request.args.get('side')
    r = requests.get(f'http://{arduino_addr}:{arduino_port}/move?dir={dir}&side={side}')

    return str(r.status_code)
    

# /led
# recebe um parametro para togglar ou setar LED no carro
# envia comando ao carro
@app.route('/led')
def led():
    action = request.args.get('action')
    value = request.args.get('value')

    if action not in ['set', 'toggle'] or (action == 'set' and value == None):
        return "Action invalida.", status.HTTP_400_BAD_REQUEST

    if action == 'toggle':
        r = requests.get(f'http://{arduino_addr}:{arduino_port}/ledtoggle')
    
    if action == 'set':
        if value == 1:
            value = 'on'
        else:
            value = 'off'

        r = request.get(f'http://{arduino_addr}:{arduino_port}/led{value}')
    
    return str(r.status_code)


# ================
#    front-end
# ================

# cada função é responsavel por uma página
# carrega a template padrão e injeta o conteudo referente a página requisitada 
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

# roda o servidor no ip e porta especificado
app.run(host='192.168.1.217', port='5000', debug=True)
