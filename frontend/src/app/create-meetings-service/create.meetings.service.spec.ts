import { TestBed } from '@angular/core/testing';

import { CreateMeetingsService } from './create.meetings.service';

describe('CreateMeetingsService', () => {
  let service: CreateMeetingsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CreateMeetingsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
