import { HttpClient,HttpParams } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable({
  providedIn: 'root'
})

export class ApiserviceFetch{
    private url = 'http://127.0.0.1:5000/meetings'
    private urlAgenda = 'http://127.0.0.1:5000/agenda'
  
    constructor(private http: HttpClient) { }
      getdata() {
        const params = new HttpParams()
        .set('token', localStorage.getItem("access_token") as string)
        return this.http.get(this.url, {params});
      }

      getAgenda() {
        const params = new HttpParams()
        .set('token', localStorage.getItem("access_token") as string)
        return this.http.get(this.urlAgenda, {params});
      }
  }