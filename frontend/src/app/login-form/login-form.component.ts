import { Component } from '@angular/core';
import { LoginService } from '../login-service/login.service';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Token } from '@angular/compiler';
import { SharedTokenService } from '../login-service/SharedTokenService'
@Component({
  selector: 'app-login',
  templateUrl: './login-form.component.html',
  styleUrls: ['./login-form.component.css']
})


export class LoginFormComponent {
  
  username: any
  password: any
  token: any
  
  constructor(private loginService: LoginService, private router: Router, private sharedService: SharedTokenService) {}

  login() {
    this.loginService.login(this.username, this.password).subscribe(
      (response:any) => {
        localStorage.setItem('access_token', response.access_token as string);

        this.sharedService.updateToken(response.access_token);
        this.router.navigate(['/home'])
      },
      (error) => {
        console.error('Login failed:', error);
      }
    );
  }
}
