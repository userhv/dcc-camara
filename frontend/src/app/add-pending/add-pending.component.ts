import * as angular from "angular";
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { Router } from '@angular/router';
import { GetAgendaService } from '../meeting-details/meeting-details.component.service';

@Component({
  selector: 'add-pending',
  standalone: true,
  imports: [NgbModule, CommonModule,],
  templateUrl: './add-pending.component.html',
  styleUrls: ['./add-pending.component.css']
})
export class AddPendingComponent {

  constructor(private router: Router, private getAgendaService: GetAgendaService) {}

  updatePendingComment() {
    const agendaId = Number(localStorage.getItem("currentAgendaId"));
    const token = localStorage.getItem('access_token') || '';
    const comment = angular.element('#pending-comment').val()

    this.getAgendaService.updateAgendaComment(agendaId, comment, token).subscribe({
        next: (response: any) => {},
        error: (error: any) => {
          console.log(error)
        }
      });
  }
}
