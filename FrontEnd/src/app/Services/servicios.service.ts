import { Injectable } from '@angular/core';
import{HttpClient,HttpHeaders} from'@angular/common/http'
import { Observable } from "rxjs";



@Injectable({
  providedIn: 'root'
})
export class ServiciosService {

  constructor(private http: HttpClient) {} 

    AST:string //SON GLOBALES PARA TODOS LOS COMPONENTES
    | undefined
    consola:string //SON GLOBALES PARA TODOS LOS COMPONENTES
    | undefined
    TablaSimbolos:any
    Errores:any

    codigo=""


    TablaMirilla:any

    CargaTiendas(txt: string){
      console.log("***********************************************************************\n"+txt)
      var json = JSON.parse(txt);
      return this.http.post('http://localhost:5000/cargartienda',json )
    }



    Flask(txt:any){
      console.log("____________\n"+txt)
      //var json = JSON.parse(txt);
      return this.http.post('http://127.0.0.1:5000/Flask',txt )
    }



    FlaskMirilla(txt:any){
      console.log("____________\n"+txt)
      //var json = JSON.parse(txt);
      return this.http.post('http://127.0.0.1:5000/FlaskMirilla',txt )
    }


  
}

