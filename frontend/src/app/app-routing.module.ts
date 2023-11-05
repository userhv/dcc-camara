import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginFormComponent } from './login-form/login-form.component';
import { HomeComponent } from './create-meetings/home/home.component';
import { CreateMeetingsComponent } from './create-meetings/create-meetings.component';
import { MeetingComponent } from './meeting/meeting.component';
import { AuthGuard } from './auth.guard';
const routes: Routes = [
  { path: 'home', component:HomeComponent, canActivate: [AuthGuard],},
  { path: 'criar-reunioes', component: CreateMeetingsComponent, canActivate: [AuthGuard],},
  { path: 'login', component: LoginFormComponent, },
  { path: 'meeting/:id', component: MeetingComponent, canActivate: [AuthGuard]}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
