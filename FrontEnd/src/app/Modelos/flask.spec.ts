import { Flask } from './flask';

describe('Flask', () => {
  it('should create an instance', () => {
    expect(new Flask()).toBeTruthy();
  });
});
