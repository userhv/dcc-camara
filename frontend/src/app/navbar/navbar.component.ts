import { Component,OnInit} from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { CommonModule } from '@angular/common';
import { JwtHelperService } from '@auth0/angular-jwt';

@Component({
  selector: 'app-navbar',
 
  template: 
  `
  <ng-container *ngIf="showNavbar">
  <nav class="navbar">
  <div class="navbar-logo">
  
    <img src="../assets/logo-dcc.png" alt="Logo">
  </div>
  <ul class="navbar-nav">

    <li class="nav-item">
      <a routerLink="/home" routerLinkActive="active">Home</a>
    </li>
    <li class="nav-item">
      <a routerLink="/home" routerLinkActive="active">Minhas Reunioes</a>
    </li>
  <ng-container *ngIf="adminType">
    <li class="nav-item">
      <a routerLink="/criar-reunioes" routerLinkActive="active">Criar Reunioes</a>
    </li>
    </ng-container>
    
  </ul>
</nav>
</ng-container>

  `,
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent   {
  token:  any;
  decodedToken :any
  adminType= false
  showNavbar=false
  constructor(private router: Router,private jwtHelper: JwtHelperService) {
    
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.showNavbar = event.url !== '/login';
      }
    });
    this.token = localStorage.getItem('access_token')  // Get the token from localStorage
    this.decodedToken = this.jwtHelper.decodeToken(this.token)
    // Decode the token
    if (this.token) {
      this.decodedToken = this.jwtHelper.decodeToken(this.token)
      this.adminType = "Chefia"==this.decodedToken.user_type
      console.log(this.adminType,this.decodedToken.user_type)
    
    }
}

}
