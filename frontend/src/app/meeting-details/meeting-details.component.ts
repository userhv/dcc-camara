import { Component, OnInit, Input } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ApiserviceFetch } from '../home-agenda/home-agenda.component.service';
import { JwtHelperService } from '@auth0/angular-jwt';
import { ActivatedRoute } from '@angular/router';
import { Meeting } from '../../meeting/meeting';
import { DomSanitizer } from '@angular/platform-browser'; // Importe o DomSanitizer
import { GetAgendaService } from './meeting-details.component.service';

@Component({
  selector: 'meeting-details',
  templateUrl: './meeting-details.component.html',
  styleUrls: ['./meeting-details.component.css']
})

export class MeetingDetailsComponent {
  newdata: any;
  newAgenda_: any;
  title = 'Home';
  currentDate: Date;
  token: any;
  agendas: any[] = [];
  meeting_id: any;
  meeting: any[] = [];
  agendaTitle: string = ''; // Inicialize a variável agendaTitle
  selectedFiles: FileList | null = null; // Inicialize a variável selectedFiles

  constructor(
    private _apiservice: ApiserviceFetch,
    private getAgendaService: GetAgendaService,
    private jwtHelper: JwtHelperService,
    private router: ActivatedRoute,
    private route: ActivatedRoute,
    private sanitizer: DomSanitizer // Injete o DomSanitizer
  ) {
    this.currentDate = new Date();
    this.token = localStorage.getItem('access_token');
    this.meeting_id = this.router.snapshot.params['id'];
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
        this.newAgenda_ = res;
        this.getAgendas();
        console.log(this.agendas);
      },
      error: (err) => console.log(err)
    });
  }

  getMeeting() {
    this.meeting = Meeting.getMeetingWithID(this.newdata.data, this.meeting_id);
  }

  getAgendas() {
    this.agendas = Meeting.getAgendasWithMeetingID(this.newAgenda_.data, this.meeting_id);
  }

  downloadPDF(agenda: any[]) {
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
    const downloadPDF = true;

    const token = localStorage.getItem('access_token') || '';

    this.getAgendaService
      .getDownloadService(agenda_title, reunion_id, document, downloadPDF, token)
      .subscribe({
        next: (response: any) => {
          const blob = new Blob([response], { type: 'application/pdf' });
          const url = URL.createObjectURL(blob);
          console.log(url)
          window.open(url, '_blank');
        },
        error: (error: any) => {
          console.log(error.url)
          window.open(error.url, '_blank');
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
          window.open(url);
        },
        error: (error: any) => {
          console.log(error.url)
          window.open(error.url);
        }
      });
  }

  removeAgenda(agenda: any, reload = true){
    const token = localStorage.getItem('access_token') || "";
    const agendaTitle = agenda[0]
    const reuniao_id = agenda[1]

    this.getAgendaService.removeAgenda(agendaTitle, reuniao_id, token).subscribe(
      (response:any) => {
        console.log(response)
        if (reload) window.location.reload();
      },
      (error) => {
        console.error('Deleting agenda failed:', error);
      }
    )
  }

  newAgenda() {
    const token = localStorage.getItem('access_token') || '';
    const id = this.route.snapshot.params['id'];

    if (this.selectedFiles && this.selectedFiles.length > 0) {
      const file = this.selectedFiles.item(0) as File;
      this.getAgendaService
        .createAgendaWithFile(this.agendaTitle, id, file, token)
        .subscribe(
          (response: any) => {
            console.log(response);
            window.location.reload();
          },
          (error) => {
            console.error('Create new meeting failed:', error);
          }
        );
    }
  }

  onFileSelected(event: any) {
    this.selectedFiles = event.target.files;
  }

  editAgenda(agenda: any) {
    this.newAgenda()
    this.removeAgenda(agenda, false)
  }
}
