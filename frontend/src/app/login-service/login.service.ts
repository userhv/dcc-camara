import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  private loginUrl = 'http://127.0.0.1:5000/login'; 

  constructor(private http: HttpClient) {}

  login(username: string, password: string) {
    const data = { "nome":username, "password":password };

    return this.http.post(this.loginUrl, data);
  }
}
