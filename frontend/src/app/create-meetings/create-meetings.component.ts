import * as angular from "angular";
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CreateMeetingsService } from '../create-meetings-service/create.meetings.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-meetings',
  standalone: true,
  imports: [NgbModule, CommonModule,],
  templateUrl: './create-meetings.component.html',
  styleUrls: ['./create-meetings.component.css']
})
export class CreateMeetingsComponent {

  constructor(private createMeetingService: CreateMeetingsService, private router: Router) {}

  newMeeting(){
    const TITLE_PREFIX = "REUNIÃO DE "

    const date = angular.element('#meeting-date').val()
    const title = TITLE_PREFIX + date

    const [dd, mm, yyyy] = date.split("/")
    const formatedDate = `${yyyy}-${mm}-${dd}`

    const token = localStorage.getItem('access_token') || "";

    this.createMeetingService.createMeeting(title, formatedDate, token).subscribe(
      (response:any) => {
        this.router.navigate(['/meeting/' + response.reuniao_id])
      },
      (error) => {
        console.error('Create new meeting failed:', error);
      }
    )
  }
}
