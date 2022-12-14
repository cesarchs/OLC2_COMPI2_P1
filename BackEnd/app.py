from flask import Flask, request,jsonify,render_template#,url_for,render_template,redirect,flash
#from flask_cors import CORS   #para que la conexion fornt-back se de sino F
from Interprete import Analizador





app = Flask(__name__)
#app.secret_key="123456"

#CORS(app)


f = open("entrada.py","r",encoding="utf-8")
entrada = f.read()

valor=entrada



AnalisisPyToPy={}
MirillaPyToPy={}
#@app.route("/", methods=["POST","GET"])
@app.route("/",methods=["GET"])
def helloWorld():
  return "<h1>CESAR LEONEL CHAMALE SICAN - 201700634</h1>"


@app.route("/Flask", methods=["POST"])
def FUNCIONAAA():

    Input = request.json['code']
    print(">>codigo a analizar:\n\n\n\n"+Input+"\n\n\n----------------------------------------------------------------------------------------------------------")

    print()
    analsis = Analizador()
    analsis.Main(Input+"\n")#para q el EOF no la joda

    global AnalisisPyToPy
    AnalisisPyToPy['AST']=analsis.grafo
    AnalisisPyToPy['TABLASIMBOLO']=analsis.TablaSimbolosREPORT#analsis.ast.getTablaSimbolosGlobal()#     falta aun 
    AnalisisPyToPy['CONSOLA']=analsis.C3D
    AnalisisPyToPy['ERRORES']=analsis.erroresSTR#analsis.ast.getExcepciones()

    print(str(analsis.ast.getExcepciones()))


    #cosa = {"hola":"holaMundo desde flask"}
    return jsonify( AnalisisPyToPy)



@app.route("/FlaskMirilla", methods=["POST"])
def Mirilla():
    Input = request.json['code']
    print(">>codigo a optimizar mirilla:\n\n\n\n"+Input+"\n\n\n----------------------------------------------------------------------------------------------------------")
    print()
    analsis = Analizador()
    analsis.Mirilla(Input)#para q el EOF no la joda

    global MirillaPyToPy
    MirillaPyToPy['C3D_OPTIMIZADO_MIRILLA']=analsis.OptimizacionMirilla
    MirillaPyToPy['REPORTES_MIRILLA']=analsis.ErroresMirilla
    

    print(analsis.OptimizacionMirilla)


    #cosa = {"hola":"holaMundo desde flask"}
    return jsonify(  MirillaPyToPy)





    
#if __name__ == "__main__":
#  app.run( port=5000,debug=True)

#if __name__ == "__app__":
 #   app.run(debug=True)#para que se actualice al detectar cambios

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')