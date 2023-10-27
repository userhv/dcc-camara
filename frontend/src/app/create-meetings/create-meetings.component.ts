import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-create-meetings',
  standalone: true,
  imports: [NgbModule, CommonModule,],
  templateUrl: './create-meetings.component.html',
  styleUrls: ['./create-meetings.component.css']
})
export class CreateMeetingsComponent {

}
