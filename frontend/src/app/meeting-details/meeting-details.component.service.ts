import { Injectable } from '@angular/core';
import { HttpClient,HttpParams } from "@angular/common/http";
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class GetAgendaService {
  private getAgendaURL = 'http://127.0.0.1:5000/get_agenda';
  private removeAgendaUrl = 'http://127.0.0.1:5000/remove_agenda';
  private newAgendaUrl = 'http://127.0.0.1:5000/new_agenda';

  private rejectAgendaUrl = 'http://127.0.0.1:5000/reject_agenda';
  private approveAgendaUrl = 'http://127.0.0.1:5000/approve_agenda';

  constructor(private http: HttpClient) {}

  removeAgenda(title: string, reuniaoId: number, token: string,): Observable<any> {
    const data = {title, reuniaoId, token};
    return this.http.post(this.removeAgendaUrl, data);
  }

  getAgendaService(
    agenda_title: string,
    reunion_id: number,
    document: string,
    token: string
  ): Observable<any> {
    const params = new HttpParams()
    .set('title', agenda_title as string)
    .set('reunion_id', reunion_id.toString() as string)
    .set('token', token as string)
    .set('document', document as string);
    return this.http.get(this.getAgendaURL, {params});
  }

  getDownloadService(
    agenda_title: string,
    reunion_id: number,
    document: string,
    download: boolean,
    token: string
  ): Observable<any> {
    const params = new HttpParams()
    .set('title', agenda_title as string)
    .set('reunion_id', reunion_id.toString() as string)
    .set('token', token as string)
    .set('document', document as string)
    .set('download', download as boolean);

    return this.http.get(this.getAgendaURL, {params});
  }

  createAgendaWithFile(
    title: string,
    reunion_id: number,
    document: File,
    token: string
  ): Observable<any> {
    const formData = new FormData();
    formData.append('title', title);
    formData.append('reunion_id', reunion_id.toString());
    formData.append('token', token);
    formData.append('document', document);

    return this.http.post(this.newAgendaUrl, formData);
  }

  rejectAgenda(
    agendaId: number,
    token: string
  ): Observable<any> {
    return this.http.post(this.rejectAgendaUrl, {agendaId, token});
  }

  approveAgenda(
    agendaId: number,
    token: string
  ): Observable<any> {
    return this.http.post(this.approveAgendaUrl, {agendaId, token});
  }
}
