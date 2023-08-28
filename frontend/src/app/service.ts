import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable({
  providedIn: 'root'
})

export class ApiserviceService {
  private url = 'http://127.0.0.1:5000/api/data'

  constructor(private http: HttpClient) { }

    getdata() {
      return this.http.get(this.url);
    }

}
