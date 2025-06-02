import { writable } from 'svelte/store';

export const session = writable<{ user: any | null }>({ user: null });

if (typeof window !== 'undefined') {
  if (typeof localStorage !== 'undefined') {
    const saved = localStorage.getItem('session');
    if (saved) session.set(JSON.parse(saved));
  }

  session.subscribe((val) => {
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem('session', JSON.stringify(val));
    }
  });

}