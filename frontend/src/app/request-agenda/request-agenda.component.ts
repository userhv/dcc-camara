import * as angular from "angular";
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { Router } from '@angular/router';
import { GetAgendaService } from '../meeting-details/meeting-details.component.service';

@Component({
  selector: 'app-request-agenda',
  standalone: true,
  imports: [NgbModule, CommonModule,],
  templateUrl: './request-agenda.component.html',
  styleUrls: ['./request-agenda.component.css']
})
export class RequestAgendaComponent {
  selectedFiles: FileList | null = null; // Inicialize a variável selectedFiles

  constructor(private getAgendaService: GetAgendaService) {}

  requestAgenda(){
    const title = angular.element('#request-agenda-title').val()
    const meetingId = Number(localStorage.getItem("currentMeetingId"));
    const token = localStorage.getItem('access_token') || "";

    if (this.selectedFiles && this.selectedFiles.length > 0) {
      const file = this.selectedFiles.item(0) as File;
      this.getAgendaService
        .createAgendaWithFile(title, meetingId, file, token)
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
}
