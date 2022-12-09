import { Component, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { Router } from '@angular/router'
import { ServiciosService } from 'src/app/Services/servicios.service'
import { Analizar } from 'src/app/Modelos/analizar'
import { Flask,FlaskMirilla } from 'src/app/Modelos/flask'
import { __values } from 'tslib';
//import {ReportesComponent} from 'src/app/Components/reportes/reportes.component'


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {


  constructor(private fase1services: ServiciosService, private _sanitizer: DomSanitizer, private router: Router) { }

  objeto: Analizar = {
    code: ""

  }


  Mirilla: FlaskMirilla ={
    C3D_OPTIMIZADO_MIRILLA:"",
    REPORTES_MIRILLA:null
  }

  flask: Flask = {
    AST: "",
    TABLASIMBOLO: null,
    CONSOLA: "",
    ERRORES: null
  }

  ngOnInit() {
    const app:any = document.getElementById("ERRORES")
    app.innerHTML = this.fase1services.consola
    //document.getElementById("TIENDAS").innerHTML = this.fase1services.codigo
  }

  Compilar(texto: any) {

    console.log(texto)
    this.fase1services.codigo = texto


    console.log("*******************    FLASK    **********************\n\n\n")
    this.objeto.code = texto

    //var valeria = "{ \"code\":\""+texto+"\"}"
    console.log(this.objeto.code)

    var alfa = this.fase1services.Flask(this.objeto)
      .subscribe(
        (res: any) => {
          console.log(res)
          alert("analisis finalizado!")
          this.flask = res
          console.log("::::::::::::::::::::::::::::::::::::::")
          console.log(this.flask)
          //console.log("::::::::::::::::::::::::::::::::::::::")
          //console.log(this.flask.AST)//STRING
          //console.log(this.flask.CONSOLA)//STRING
          //console.log(this.flask.ERRORES)//ARRAY
          //console.log(this.flask.TABLASIMBOLO)//nose q tipo es xd
          const app:any =document.getElementById("ERRORES")
          app.innerHTML = this.flask.CONSOLA

          const app2:any =document.getElementById("ERRORES3")
          app2.innerHTML = this.flask.CONSOLA
          

          this.fase1services.AST = this.flask.AST
          this.fase1services.consola = this.flask.CONSOLA
          this.fase1services.Errores = this.flask.ERRORES
          this.fase1services.TablaSimbolos = this.flask.TABLASIMBOLO


        },
        err => console.log(err)
      )



  }

  
  OptimizarMirilla(texto: any) {

    console.log(texto)
    this.fase1services.codigo = texto


    console.log("*******************    FLASK MIRILLA    **********************\n\n\n")
    this.objeto.code = texto

    //var valeria = "{ \"code\":\""+texto+"\"}"
    console.log(this.objeto.code)

    var alfa = this.fase1services.FlaskMirilla(this.objeto)
      .subscribe(
        (res: any) => {
          console.log(res)
          alert("optimizacion finalizada!")
          this.Mirilla = res
          console.log("::::::::::::::::::::::::::::::::::::::")
          console.log(this.Mirilla)
          //console.log("::::::::::::::::::::::::::::::::::::::")
          //console.log(this.Mirilla.AST)//STRING
          //console.log(this.Mirilla.CONSOLA)//STRING
          //console.log(this.Mirilla.ERRORES)//ARRAY
          //console.log(this.Mirilla.TABLASIMBOLO)//nose q tipo es xd
          const app:any =document.getElementById("ERRORES2")
          app.innerHTML = this.Mirilla.C3D_OPTIMIZADO_MIRILLA
          
          
          this.fase1services.TablaMirilla = this.Mirilla.REPORTES_MIRILLA

          /*this.fase1services.consola = this.Mirilla.CONSOLA
          this.fase1services.Errores = this.Mirilla.ERRORES
          this.fase1services.TablaSimbolos = this.Mirilla.TABLASIMBOLO*/


        },
        err => console.log(err)
      )



  }








}
