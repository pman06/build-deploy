import { render, screen } from '@testing-library/react';
import App from './App';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});

test('adds 1 + 2 to equal 3', () => {
    expect(1 + 2).toBe(3);
});

// test('should fail', () => { 
// 	fail('it should not reach here');
//  })