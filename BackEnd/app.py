from flask import Flask, request,render_template

from EnviarInformacion.pInterpretePy import Analisis
import gramaticaop as c3d

app = Flask(__name__)


f = open("entrada.py","r",encoding="utf-8")# Abrimos archivo de entrada inicial
entrada = f.read()                          # metodo de leer archivo de entrada inicial
valor=entrada                               # Guardamos en una variable el valor inicial


erroress={}
erroress['entrada']=valor
erroress['arbol']="digraph{PYTHON->PyToPy}"
erroress['ts']=[]
erroress['ts'].append({'no':'1','id':'-','tipo':'-','ambito':'-','valor':'-','fil':'-','col':'-'})
erroress['error']=[]
erroress['error'].append({'no':'0','tipo':'-','des':'-','fil':'-','col':'-','fecha':'-'})
erroress['consola']="aun no se ha realizado ningun analisis"
erroress['c3d']=''
erroress['bloques']=''
erroress['reporteMirilla']=[]
erroress['reporteBloques']=[]

@app.route("/", methods=["POST","GET"])
def vista():
    #global backupLista
    #flash("You were successfully logged in")
    #global backupLista
    global erroress
    
    if request.method == "POST":

        if request.form.get("limpiar"):
            #erroress={}
            global erroress
            erroress['entrada']=''
            erroress['arbol']="digraph{PYTHON->PyToPy}"
            erroress['ts']=[]
            erroress['ts'].append({'no':'1','id':'-','tipo':'-','ambito':'-','valor':'-','fil':'-','col':'-'})
            erroress['error']=[]
            erroress['error'].append({'no':'0','tipo':'-','des':'-','fil':'-','col':'-','fecha':'-'})
            erroress['consola']="aun no se ha realizado ningun analisis"
            erroress['c3d']=''
            erroress['bloques']=''
            erroress['reporteMirilla']=[]
            erroress['reporteBloques']=[]

            
            valor =""
            return render_template("analisis.html",initial="",regres = erroress['consola'],users=erroress['ts'],opts=erroress['reporteMirilla'],optsb=erroress['reporteBloques'],errors=erroress['error'],hola=erroress['arbol'],dotcode=erroress['arbol'])
        elif request.form.get("ejecutar"):
            inpt = request.form["inpt"]
            if inpt != "":
                #print("RESULTADO DE ANALIZAR: "+inpt)
                valor = inpt
                nuevoAnalisis = Analisis()
                #realiza analisis lexico,sintactico y semantico
                errore=nuevoAnalisis.principal(inpt)
                #retorna el valor luego de analisis
                erroress['entrada']=inpt
                erroress['consola']=errore.getConsola()+errore.getC3D()
                erroress['c3d']=''
                erroress['bloques']=''
                erroress['arbol']=errore.getArbol()
                erroress['ts']= errore.getTs()
                erroress['error']=errore.getErrores() 
                erroress['reporteMirilla']=[]
                erroress['reporteBloques']=[]

                return render_template("analisis.html",initial=valor,regres = erroress['consola'],c3dopt=erroress['c3d'],c3doptb=erroress['bloques'],users=erroress['ts'],opts=erroress['reporteMirilla'],optsb=erroress['reporteBloques'],errors=erroress['error'],hola=erroress['arbol'],dotcode=erroress['arbol'])
            else:

                return render_template("analisis.html",initial=erroress['entrada'],regres = erroress['consola'],c3dopt=erroress['c3d'],c3doptb=erroress['bloques'],users=erroress['ts'],opts=erroress['reporteMirilla'],optsb=erroress['reporteBloques'],errors=erroress['error'],hola=erroress['arbol'],dotcode=erroress['arbol'])
        elif request.form.get("mirilla"):
            inpta = request.form["c3dinp"]
            if inpta != "":
                try:
                    valorr = inpta
                    #mando entrada en c3d para optimizar
                    instrucciones = c3d.parseOP(valorr)
                    if instrucciones != None:
                        instrucciones.Mirilla()
                        salida = instrucciones.getCode()#aqui esta el codigo optimizado
                        #print(salida)
                        
                        erroress['consola']=valorr
                        erroress['c3d']=salida

                        erroress['reporteMirilla']= instrucciones.getReporte()

                        return render_template("analisis.html",initial=erroress['entrada'],regres = erroress['consola'],c3dopt=erroress['c3d'],c3doptb=erroress['bloques'],users=erroress['ts'],opts=erroress['reporteMirilla'],optsb=erroress['reporteBloques'],errors=erroress['error'],hola=erroress['arbol'],dotcode=erroress['arbol'])
                    else:
                        erroress['consola']='Hubo errores sintácticos en optimizacion, no se pudo recuperar'#este cambiara por la consola de opt
                        erroress['c3d']=''
                        erroress['bloques']=''
       
                        return render_template("analisis.html",initial=erroress['entrada'],regres = erroress['consola'],c3dopt=erroress['c3d'],c3doptb=erroress['bloques'],users=erroress['ts'],opts=erroress['reporteMirilla'],optsb=erroress['reporteBloques'],errors=erroress['error'],hola=erroress['arbol'],dotcode=erroress['arbol'])
                except:
                    print("NO SE PUDO EJECUTAR OPTIMIZACION")
        elif request.form.get("bloques"):
            inpts = request.form["c3dinp"]
            if inpts != "":
                try:
                    valorrr = inpts
                    #mando entrada en c3d para optimizar
                    instrucciones = c3d.parseOP(valorrr)
                    if instrucciones != None:

                        
                        return render_template("analisis.html",initial=erroress['entrada'],regres = erroress['consola'],c3dopt=erroress['c3d'],c3doptb=erroress['bloques'],users=erroress['ts'],opts=erroress['reporteMirilla'],optsb=erroress['reporteBloques'],errors=erroress['error'],hola=erroress['arbol'],dotcode=erroress['arbol'])
                    else:
                        erroress['consola']='Hubo errores sintácticos en optimizacion, no se pudo recuperar'#este cambiara por la consola de opt
                        erroress['c3d']=''
                        erroress['bloques']=''

                        return render_template("analisis.html",initial=erroress['entrada'],regres = erroress['consola'],users=erroress['ts'],opts=erroress['reporteMirilla'],optsb=erroress['reporteBloques'],errors=erroress['error'],hola=erroress['arbol'],dotcode=erroress['arbol'])
                except:
                    print("NO SE PUDO EJECUTAR OPTIMIZACION")
    else:

        return render_template("analisis.html",initial=erroress['entrada'],regres = erroress['consola'],users=erroress['ts'],opts=erroress['reporteMirilla'],optsb=erroress['reporteBloques'],errors=erroress['error'],hola=erroress['arbol'],dotcode=erroress['arbol'])


@app.route("/hi",methods=["GET"])
def helloWorld():
  return "<h1>CESAR LEONEL CHAMALE SICAN - 201700634</h1>"


#if __name__ == "__main__":
#  app.run( port=5000,debug=True)

#if __name__ == "__app__":
 #   app.run(debug=True)#para que se actualice al detectar cambios


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
