import * as angular from "angular";
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CreateAgendasService } from '../create-agendas-service/create.agendas.service';
import { Router,ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-create-agendas',
  standalone: true,
  imports: [NgbModule, CommonModule,],
  templateUrl: './create-agendas.component.html',
  styleUrls: ['./create-agendas.component.css']
})
export class CreateAgendasComponent {

  constructor(private createAgendaService: CreateAgendasService, private router: Router, private route: ActivatedRoute) {}

  newAgenda(){
    const agendaTitle = angular.element('#agenda-title').val()
    const agendaFiles = angular.element('#agenda-files').val().replace("C:\\fakepath\\","\\assets\\")

    const token = localStorage.getItem('access_token') || "";

    const id = this.route.snapshot.params["id"]

    this.createAgendaService.createAgenda(agendaTitle, id, agendaFiles, token).subscribe(
      (response:any) => {
        console.log(response)
        window.location.reload();
      },
      (error) => {
        console.error('Create new meeting failed:', error);
      }
    )
  }
}
