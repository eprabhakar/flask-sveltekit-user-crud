// src/lib/stores/alert.ts
import { writable } from 'svelte/store';

export const alert = writable('');
export const alertType = writable<'success' | 'error' | 'info' | 'warning'>('success');
//export const showAlert = writable(false);

export function displayAlert(msg: string, type: 'success' | 'error' | 'info' | 'warning' = 'success') {
  alert.set(msg);
  alertType.set(type);
  setTimeout(() => alert.set(''), 3000); // auto-hide
}
