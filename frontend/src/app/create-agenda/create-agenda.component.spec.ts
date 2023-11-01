import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateAgendaComponent } from './create-agenda.component';

describe('CreateAgendaComponent', () => {
  let component: CreateAgendaComponent;
  let fixture: ComponentFixture<CreateAgendaComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CreateAgendaComponent]
    });
    fixture = TestBed.createComponent(CreateAgendaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
