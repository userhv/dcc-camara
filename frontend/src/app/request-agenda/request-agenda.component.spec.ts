import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RequestAgendaComponent } from './request-agenda.component';

describe('RequestAgendaComponent', () => {
  let component: RequestAgendaComponent;
  let fixture: ComponentFixture<RequestAgendaComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RequestAgendaComponent]
    });
    fixture = TestBed.createComponent(RequestAgendaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
