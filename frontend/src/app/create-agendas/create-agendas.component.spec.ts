import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateAgendasComponent } from './create-agendas.component';

describe('CreateAgendaComponent', () => {
  let component: CreateAgendasComponent;
  let fixture: ComponentFixture<CreateAgendasComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CreateAgendasComponent]
    });
    fixture = TestBed.createComponent(CreateAgendasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
