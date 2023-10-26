import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginFormComponent } from './login-form/login-form.component';
import { HomeComponent } from './home/home.component';
import { CreateMeetingsComponent } from './create-meetings/create-meetings.component';
import { AuthGuard } from './auth.guard';
const routes: Routes = [
  { path: 'home', component:HomeComponent, canActivate: [AuthGuard],},
  { path: 'criar-reunioes', component: CreateMeetingsComponent, canActivate: [AuthGuard],},
  { path: 'login', component: LoginFormComponent, },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
