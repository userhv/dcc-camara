import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiserviceFetch } from '../home-agenda/home-agenda.component.service';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { format } from 'date-fns'; // Importe a função format de date-fns
import { JwtHelperService } from '@auth0/angular-jwt';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'meeting-details',
  templateUrl: './meeting-details.component.html',
  styleUrls: ['./meeting-details.component.css']
})
export class MeetingDetailsComponent {
  newdata: any;
  newAgenda: any;
  title = 'Home';
  currentDate: Date;
  token: any;
  agendas: any[] = [];
  meeting_id: any;
  meeting: any[] = [];

  constructor(private _apiservice: ApiserviceFetch, private jwtHelper: JwtHelperService, private router: ActivatedRoute) {
    this.currentDate = new Date();
    this.token = localStorage.getItem('access_token')
    this.meeting_id = this.router.snapshot.params["id"];
  }

  ngOnInit() {
    this._apiservice.getdata().subscribe({
      next: (res) => {
        this.newdata = res;
        this.getMeeting();
      },
      error: (err) => console.log(err)
    });
    this._apiservice.getAgenda().subscribe({
      next: (res) => {
        this.newAgenda = res;
        this.getAgendas();
        console.log(this.agendas)
      },
      error: (err) => console.log(err)
    })
  }

  getMeeting(){
    this.newdata.data.forEach((meeting: [any, any, any]) => {
      const [id, title, dateStr] = meeting;
      if(id == this.meeting_id){
        this.meeting = meeting
        return
      }
    })
  }

  getAgendas(){
    this.newAgenda.data.forEach((agendaData: [any, any, any]) => {
      const [titulo, reuniao_id, documento] = agendaData;
      if(reuniao_id == this.meeting_id){
        this.agendas.push(agendaData)
      }
    })
  }
}
