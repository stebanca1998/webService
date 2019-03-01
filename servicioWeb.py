#!/usr/bin/python
import subprocess
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

#1) Listar las maquinas virtuales del host

@app.route('/maquinas')
def listVms():
	ejec = subprocess.check_output(['vboxmanage','list','vms'])
	res = ejec.splitlines()
	return jsonify({'list': res})

#2) Listar las maquinas en ejecucion del host

@app.route('/corriendo')
def listRunning():
	ejec = subprocess.check_output(['vboxmanage','list','runningvms'])
	res = ejec.splitlines()
	return jsonify({'list': res})

#-------------DADA UNA MAQUINA VIRTUAL-------------------
#3) Caracteristicas de La maquina virtual

@app.route('/maquinas/<string:mv>')
def features(mv):
	ejec = subprocess.check_output(['vboxmanage','showvminfo',mv])
	res = ejec.splitlines()
	return jsonify({'list': res})

#4) Ver la ram de la maquna virtua

@app.route('/maquinas/ram/<string:mv>')
def ram(mv):
	ejec = subprocess.Popen(['vboxmanage','showvminfo',mv], stdout=subprocess.PIPE)
	tail = subprocess.check_output(['grep','Memory'], stdin=ejec.stdout)
	res = tail.splitlines()
	return jsonify({'list': res})

#5) Ver el #de procesadores aignados a la maquina virtual

@app.route('/maquinas/cpus/<string:mv>')
def cpu(mv):
	ejec = subprocess.Popen(['vboxmanage','showvminfo', mv], stdout = subprocess.PIPE)
	tail = subprocess.check_output(['grep','CPUs'], stdin=ejec.stdout)
	res = tail.splitlines()
	return jsonify({'list': res})

#6) Tarjetas de red conectadas a la maquina virtual

@app.route('/maquinas/net/<string:mv>')
def net(mv):
	ejec = subprocess.Popen(['vboxmanage','showvminfo', mv], stdout=subprocess.PIPE)
	tail1 = subprocess.Popen(['grep', 'NIC'], stdin=ejec.stdout, stdout=subprocess.PIPE)
	tail2 = subprocess.Popen(['grep','MAC'], stdin=tail1.stdout, stdout=subprocess.PIPE)
	res = subprocess.check_output(['wc','-l'], stdin = tail2.stdout)
	return jsonify({'list': res})

#7) Modificar el numero de CPUs

@app.route('/maquinas/modify/cpu/<string:mv>/<string:cpu>')
def modifycpu(mv,cpu):
	subprocess.call(['vboxmanage','modifyvm', mv, '--cpus', cpu])
	return "Se cambio el numero de cpus de la maquina virtual a "+ cpu

#8) Modificar la RAM asignada a la maquina virtual

@app.route('/maquinas/modify/ram/<string:mv>/<string:ram>')
def modifyram(mv,ram):
	subprocess.call(['vboxmanage','modifyvm', mv, '--memory', ram])
	return "Se cambio la ram de la maquina virtual a "+ ram

#9) Modificar el porcentaje de procesador asignado a una maquina virtual

@app.route('/maquinas/modify/usecpu/<string:mv>/<string:cpupercentage>')
def modifycpuper(mv,cpupercentage):
	subprocess.call(['vboxmanage','modifyvm', mv, '--cpuexecutioncap', cpupercentage])
	return "Se cambio el porcentaje de cpu que puede ser usado a "+ cpupercentage

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True, port=5001)
