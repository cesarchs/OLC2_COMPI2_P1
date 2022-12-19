import { Component, Input, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { Router } from '@angular/router'
import { ServiciosService } from 'src/app/Services/servicios.service'
//import { graphviz } from 'd3-graphviz';
import { graphviz } from 'd3-graphviz';

@Component({
  selector: 'app-reportes',
  templateUrl: './reportes.component.html',
  styleUrls: ['./reportes.component.css']
})


export class ReportesComponent implements OnInit {


  constructor(private fase1services: ServiciosService) { }

  ngOnInit(): void {

    console.log(this.fase1services.AST)
  }

  //ItemsArray= [{id:"007",name:"007",email:"007",phone:"007",address:"007"},{id:"007",name:"007",email:"007",phone:"007",address:"007"}];

  ItemsArray=this.fase1services.Errores
  ItemsArray2=this.fase1services.TablaSimbolos

  ItemsArray3 = this.fase1services.TablaMirilla//para reporte de mirilla



  d3() {


    //console.log('puto grahpviz de mierdaa')

    try {
      graphviz('#zzz').renderDot(String(this.fase1services.AST));
      console.log("GOKU")

    } catch (e) {
      //console.log(e);
      console.log("error");
    }



  }

  Errores(){}
  TSimbolos(){}



}
