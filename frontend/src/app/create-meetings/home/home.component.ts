import { Component, OnInit } from '@angular/core';
import { HomeAgendaComponent } from '../../home-agenda/home-agenda.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  title = 'Home';

  ngOnInit() {
    // Coloque o código de inicialização do componente aqui
  }
}
