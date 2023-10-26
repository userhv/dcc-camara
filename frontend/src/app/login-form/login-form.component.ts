import { Component } from '@angular/core';
import { LoginService } from '../login-service/login.service';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Token } from '@angular/compiler';
@Component({
  selector: 'app-login',
  templateUrl: './login-form.component.html',
  styleUrls: ['./login-form.component.css']
})


export class LoginFormComponent {
  
  username: any
  password: any
  

  constructor(private loginService: LoginService ,private router: Router) {}

  login() {
    this.loginService.login(this.username, this.password).subscribe(
      (response:any) => {
       
        const data = response
      
        localStorage.setItem('access_token', response.access_token as string);
       
        this.router.navigate(['/home'])
      },
      (error) => {
        console.error('Login failed:', error);
      }
    );
  }
}
