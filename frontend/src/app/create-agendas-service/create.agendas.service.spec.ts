import { TestBed } from '@angular/core/testing';

import { CreateAgendasService } from './create.agendas.service';

describe('CreateAgendasService', () => {
  let service: CreateAgendasService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CreateAgendasService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
