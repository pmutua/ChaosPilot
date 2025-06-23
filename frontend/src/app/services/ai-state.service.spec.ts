import { TestBed } from '@angular/core/testing';

import { AiStateService } from './ai-state.service';

describe('AiStateService', () => {
  let service: AiStateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AiStateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
