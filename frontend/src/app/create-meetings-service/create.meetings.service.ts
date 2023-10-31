
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CreateMeetingsService {
  private newMeetingUrl = 'http://127.0.0.1:5000/new_meeting';

  constructor(private http: HttpClient) {}

  createMeeting(title: string, date: string, token: string): Observable<any> {
    const data = {title, date, token};
    return this.http.post(this.newMeetingUrl, data);
  }
}
