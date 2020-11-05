from flask import Flask, render_template, request
import requests

app = Flask(__name__)

arduino_addr = '127.0.0.1'
arduino_port = 0

@app.route('/bind')
def bind():
    try:
        arduino_addr = request.args.get('addr')
        arduino_port = request.args.get('port') 
        return 'ok'
    except:
        return 'erro'

@app.route('/cmd')
def move():
    cmdname = request.args.get('cmdname')
    cmdstatus = request.args.get('cmdstatus')
    r = requests.get(f'{arduino_addr}:{arduino_port}/?cmdname={cmdname}&cmdstatus={cmdstatus}')
    return r.status_code


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

@app.route('/componentes/<componente>')
def componentes(componente):
    return render_template('content_template.html', content=f'/componentes/{componente}.html')

app.run(host='192.168.1.217', port='5000', debug=True)
