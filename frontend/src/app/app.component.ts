import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ApiserviceService } from './service';
import { NavbarComponent } from './navbar/navbar.component';
import { CreateMeetingsComponent } from './create-meetings/create-meetings.component';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-root',   
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  
})

export class AppComponent implements OnInit {
  newdata:any;
  title = 'frontend';

  constructor(private _apiservice:ApiserviceService) { }

  ngOnInit() {
    this._apiservice.getdata().subscribe({
      next: (res) => this.newdata=res,
      error: (err) => console.log(err)
    })
  }

}
