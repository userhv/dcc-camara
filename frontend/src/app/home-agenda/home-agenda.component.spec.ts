import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeAgendaComponent } from './home-agenda.component';

describe('HomeAgendaComponent', () => {
  let component: HomeAgendaComponent;
  let fixture: ComponentFixture<HomeAgendaComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [HomeAgendaComponent]
    });
    fixture = TestBed.createComponent(HomeAgendaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
