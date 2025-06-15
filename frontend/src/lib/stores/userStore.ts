// src/lib/stores/usersStore.ts
import { writable } from 'svelte/store';

export const users = writable<any[]>([]);
export const searchedUsers = writable<any[]>([]);
