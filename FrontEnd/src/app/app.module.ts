import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import{HttpClientModule} from'@angular/common/http'
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './Components/home/home.component';
import { ReportesComponent } from './Components/reportes/reportes.component';
import {FormsModule} from '@angular/forms'
import{ ServiciosService }from 'src/app/Services/servicios.service';
import { SigInComponent } from './Components/sig-in/sig-in.component'

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ReportesComponent,
    SigInComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule//fase 3
  ],
  providers: [
    ServiciosService

  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
