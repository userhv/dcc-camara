
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CreateAgendasService {
  private newAgendaUrl = 'http://127.0.0.1:5000/new_agenda';

  constructor(private http: HttpClient) {}

  createAgenda(title: string, reunion_id: number, document: string, token: string,): Observable<any> {
    const data = {title, reunion_id, document, token};
    return this.http.post(this.newAgendaUrl, data);
  }
}
