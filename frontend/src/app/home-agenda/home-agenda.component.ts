import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiserviceFetch } from './home-agenda.component.service';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { format } from 'date-fns'; // Importe a função format de date-fns
import { JwtHelperService } from '@auth0/angular-jwt';
import { RouterModule } from '@angular/router';
import { GetAgendaService } from '../meeting-details/meeting-details.component.service';
import { RequestAgendaComponent } from '../request-agenda/request-agenda.component';
import { AddPendingComponent } from '../add-pending/add-pending.component';

@Component({
  selector: 'home-agenda',
  standalone: true,
  imports: [NgbModule, CommonModule, RouterModule, RequestAgendaComponent, AddPendingComponent],
  templateUrl: './home-agenda.component.html',
  styleUrls: ['./home-agenda.component.css']
})
export class HomeAgendaComponent implements OnInit {
  newdata: any;
  pendingAgendas: any = [];
  newAgenda: any;
  title = 'Home';
  currentDate: Date;
  upcomingMeetings: any[] = [];
  pastMeetings: any[] = [];
  token: any;
  decodedToken: any;
  userType: any;
  agendas: any[] = [];
  currentMeetingId = 0;

  constructor(private _apiservice: ApiserviceFetch, private getAgendaService: GetAgendaService, private jwtHelper: JwtHelperService) {
    this.currentDate = new Date();
    this.token = localStorage.getItem('access_token')
    if (this.token) {
      this.decodedToken = this.jwtHelper.decodeToken(this.token)
      this.userType = "Chefia" == this.decodedToken.user_type // Verifica se o usuário logado é chefia
    }
  }

  ngOnInit() {
    this._apiservice.getdata().subscribe({
      next: (res) => {
        this.newdata = res;
        console.log('Dados da API:', this.newdata);
        this.mapAndFilterMeetings();
      },
      error: (err) => console.log(err)
    });
    this._apiservice.getAgenda().subscribe({
      next: (res) => {
        this.newAgenda = res;
        console.log('Dados de pautas', this.newAgenda);
        this.mapAndFilterAgendas();
      },
      error: (err) => console.log(err)
    })
  }

  mapAndFilterMeetings() {
    this.newdata.data.forEach((meetingData: [any, any, any]) => {
      const [id, title, dateStr] = meetingData;
      const meetingDate = new Date(dateStr);

      const formattedDate = format(meetingDate, 'dd/MM/yyyy'); // Formate a data
      if (meetingDate >= this.currentDate) {
        this.upcomingMeetings.push({ id, title, date: `${formattedDate}` });
      } else {
        this.pastMeetings.push({ id, title, date: `${formattedDate}` });
      }
    });

    console.log('Reuniões Futuras:', this.upcomingMeetings);
    console.log('Reuniões Passadas:', this.pastMeetings);
  }

  mapAndFilterAgendas() {
    this.newAgenda.data.forEach((agendaData: [any, any, any, any, any, any]) => {
      const [titulo, reuniao_id, documento, aprovado, comentario, pauta_id] = agendaData
      if (aprovado){
        this.agendas.push(agendaData)
      }else{
        this.pendingAgendas.push(agendaData)
      }
    })

    console.log('Pautas:', this.agendas);
    console.log('Pautas pendentes:', this.pendingAgendas);
  }

  updateCurrentMeetingId(meetingId: number) {
    localStorage.setItem("currentMeetingId", meetingId.toString());
    console.log(localStorage.getItem("currentMeetingId"))
  }

  rejectPending(agendaData: any){
    const [titulo, reuniao_id, documento, aprovado, comentario, pauta_id] = agendaData
    const token = localStorage.getItem('access_token') || '';
    
    console.log(pauta_id, token);

    this.getAgendaService.rejectAgenda(pauta_id, token).subscribe({
      next: (response: any) => {
        window.location.reload();
      },
      error: (error: any) => {
        console.log(error)
      }
    });
  }

  approvePending(agendaData: any){
    const [titulo, reuniao_id, documento, aprovado, comentario, pauta_id] = agendaData
    const token = localStorage.getItem('access_token') || '';

    console.log(pauta_id, token);

    this.getAgendaService.approveAgenda(pauta_id, token).subscribe({
      next: (response: any) => {
        window.location.reload();
      },
      error: (error: any) => {
        console.log(error)
      }
    });
  }

  openPDF(agenda: any) {
    function processString(_string: string): string {
      const processed_string = _string
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/\s+/g, '_');
      return processed_string;
    }
    const agenda_title = processString(agenda[0]);
    const reunion_id = agenda[1];
    const document = agenda[2];

    const token = localStorage.getItem('access_token') || '';

    this.getAgendaService
      .getAgendaService(agenda_title, reunion_id, document, token)
      .subscribe({
        next: (response: any) => {
          const blob = new Blob([response], { type: 'application/pdf' });
          const url = URL.createObjectURL(blob);
          console.log(url)
          window.open(url, '_blank');
        },
        error: (error: any) => {
          console.log(error.url)
          window.open(error.url);
        }
      });
  }
}
