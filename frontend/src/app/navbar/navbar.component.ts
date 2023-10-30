import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { HttpClient, HttpParams } from '@angular/common/http';
import { SharedTokenService } from '../login-service/SharedTokenService';
import { CommonModule } from '@angular/common';  
import { BrowserModule } from '@angular/platform-browser';
@Component({
  selector: 'app-navbar',

  template:
    `
  <ng-container *ngIf="showNavbar">
  <nav class="navbar">
  <div class="navbar-logo">
  
    <img src="../assets/dcc.png" alt="Logo">
  </div>
  <ul class="navbar-nav">
    
  <h1 class="simple-text">{{username}} </h1>
  <p class="role-text">{{role}}</p>
    <button class="nav-item button-nav">
      <a routerLink="/home" >Inicio</a>
    </button>
 
    <ng-container *ngIf="adminType">
      <app-create-meetings class="nav-item button-nav" ></app-create-meetings>
    </ng-container>

    <ng-container *!ngIf="adminType">
    <button class="nav-item">
      <a routerLink="" >Solicitar Pauta</a>
    </button>
    </ng-container>
    
  </ul>
</nav>
</ng-container>

  `,
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  token: any;
  adminType = false
  showNavbar = false
  username: any
  role:any
  constructor(private router: Router, private http: HttpClient, private SharedTokenService: SharedTokenService) {

    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.showNavbar = event.url !== '/login';
      }
    });
  }
  ngOnInit(): void {
    
    //this is terrible , fix later
    this.token = localStorage.getItem('access_token')
    this.SharedTokenService.token$.subscribe((token) => {
      this.token = token;
      if (this.token.length==0){
        this.token = localStorage.getItem('access_token')
       
      }
    
      const params = new HttpParams()
        .set('token', this.token as string)
        
        
      this.http.get('http://127.0.0.1:5000/user', { params }).subscribe((response: any) => {
        
        this.username = response.username;
        this.adminType = "Chefia" == response.role
        this.role =response.role
     
       
      });

    });

  
  }

}
