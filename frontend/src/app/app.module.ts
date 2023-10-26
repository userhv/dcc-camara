import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { NavbarComponent } from './navbar/navbar.component';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from  '@angular/common/http';
import { LoginFormComponent } from './login-form/login-form.component';
import { HomeComponent } from './home/home.component';
import { CreateMeetingsComponent } from './create-meetings/create-meetings.component';
import { FormsModule } from '@angular/forms';
import { JwtModule,JWT_OPTIONS} from '@auth0/angular-jwt';
import { JwtHelperService} from '@auth0/angular-jwt'


export function jwtOptionsFactory(jwtHelper: JwtHelperService) {
  return {
    tokenGetter: () => {
      return localStorage.getItem('access_token');
    },
 
    headerName: 'Authorization',
    authScheme: 'Bearer',
    throwNoTokenError: true,
  
    skipWhenExpired: true,
    debug: false,
    errorHandler: (error: any) => {
      // Handle token verification errors
    },
    secretOrKey: 'ydw9iqbZby', // Replace with your actual secret key
  };
}
AppComponent
@NgModule({
  declarations: [
    AppComponent,
    LoginFormComponent, 
    NavbarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,  
    FormsModule,
    JwtModule
   
  ],
  providers: [ { provide: JWT_OPTIONS, useValue: JWT_OPTIONS },
    JwtHelperService],
  bootstrap: [AppComponent]
})
export class AppModule { }
