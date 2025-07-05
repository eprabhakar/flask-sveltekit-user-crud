// src/lib/api/users.ts
export let myname = "Prabhakar"

import { PUBLIC_API_BASE_URL } from '$env/static/public';
//const apiBase = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';

let filteredUsers: any[] = []; // Users filtered based on search


export function handleSearchInput(data:{users: any[], query: string}) {
    const lowerQuery = data.query.toLowerCase();
      filteredUsers = data.users.filter(user =>
        user.username.toLowerCase().includes(lowerQuery) ||
        user.email.toLowerCase().includes(lowerQuery)
    );
    return filteredUsers;    
  }

export async function fetchUsers() {
  const res = await fetch(`/api/users`, {
    credentials: "include"
  });
  if (!res.ok) throw new Error("Failed to fetch users");
  return await res.json();
}

export async function createUser(data: {
  username: string;
  email: string;
  password: string;
  role: string;
}) {
  const res = await fetch(`/api/user`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    //console.error("Error creating user:", res.status, res.statusText);
    const err = await res.json();
    //alert(err.error || "Failed to create user");
    throw new Error(err.error);
  }
  return await res.json();
}

export async function updateUser(id: number, data: { username: string; email: string }) {
  const res = await fetch(`/api/users/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error("Failed to update user");
}

export async function deleteUser(id: number) {
  const res = await fetch(`/api/users/${id}`, {
    method: "DELETE",
    credentials: "include"
  });
  if (!res.ok) throw new Error("Failed to delete user");
}

export async function searchUsers(query: string) {
  const res = await fetch(`${PUBLIC_API_BASE_URL}/search?q=${encodeURIComponent(query)}`, {
    credentials: "include"
  });
  if (!res.ok) throw new Error("Search failed");
  return await res.json();
}
