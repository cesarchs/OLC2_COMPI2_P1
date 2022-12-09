import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './Components/home/home.component';
import { ReportesComponent } from './Components/reportes/reportes.component';
import { SigInComponent } from './Components/sig-in/sig-in.component';

const routes: Routes = [

  {
    path: '',                 //cuando esta asi es mi ruta inicial
    redirectTo: '/home',
    pathMatch: 'full'      
    },
    {
      path: 'home',
      component: HomeComponent
    },
    {
      path: 'reportes',
      component: ReportesComponent, //autenticar admin
     // canActivate:[Auth2Guard]
    }
    ,
    {
      path: 'autor',
      component: SigInComponent, //autenticar admin
     // canActivate:[Auth2Guard]
    }
    
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
