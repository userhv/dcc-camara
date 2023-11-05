import * as angular from "angular";
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { Router } from '@angular/router';

@Component({
  selector: 'app-request-agenda',
  standalone: true,
  imports: [NgbModule, CommonModule,],
  templateUrl: './request-agenda.component.html',
  styleUrls: ['./request-agenda.component.css']
})
export class RequestAgendaComponent {

  constructor() {}

  requestAgenda(){
    const TITLE_PREFIX = "REUNIÃO DE "

    const date = angular.element('#meeting-date').val()
    const title = TITLE_PREFIX + date

    const [dd, mm, yyyy] = date.split("/")
    const formatedDate = `${yyyy}-${mm}-${dd}`

    const token = localStorage.getItem('access_token') || "";
  }
}
