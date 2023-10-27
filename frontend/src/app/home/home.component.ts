import { Component,OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../navbar/navbar.component';
import { ApiserviceFetch } from './home.component.service';
@Component({
  selector: 'app-home',
 
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  newdata:any;
  title = 'frontend';

  constructor(private _apiservice:ApiserviceFetch) { }
  ngOnInit() {
    this._apiservice.getdata().subscribe({
      next: (res) => this.newdata=res,
      error: (err) => console.log(err)
      
    })
  }

}