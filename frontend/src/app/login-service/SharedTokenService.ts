import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedTokenService {
 
  private tokenSubject: BehaviorSubject<string> = new BehaviorSubject<string>('');

  token$ = this.tokenSubject.asObservable();

  updateToken(token: string) {

    this.tokenSubject.next(token);
  }
}
