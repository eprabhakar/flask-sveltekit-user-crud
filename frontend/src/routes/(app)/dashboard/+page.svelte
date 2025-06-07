<script lang="ts">
  import { onMount } from "svelte";
  import { session } from "$lib/stores/session";
  import UserList from "$lib/components/UserList.svelte";
  import { goto } from '$app/navigation';

  let users: any[] = [];
  let error: string | null = null;
  let editing: number | null = null;

  let editUsername = "";
  let editEmail = "";

  $: user = $session.user;
  $: isAdmin = user?.role === "admin";
  let newUsername = "";
  let newEmail = "";
  let newPassword = "";
  let newRole = "user"; // default, can be changed to 'admin'

  async function createUser() {
    const res = await fetch("http://localhost:5000/user", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: newUsername,
        email: newEmail,
        password: newPassword,
        role: newRole,
      }),
    });

    if (res.ok) {
      const user = await res.json();
      users = [...users, user]; // Update UI
      newUsername = "";
      newEmail = "";
      newPassword = "";
      newRole = "user";
    } else {
      const err = await res.json();
      alert(err.error);
    }
  }

  async function fetchUsers() {
    const res = await fetch("http://localhost:5000/users", {
      credentials: "include",
    });
    if (res.ok) {
      users = await res.json();
    } else {
      const err = await res.json();
      error = err.error || "Failed to fetch users";
    }
  }

  onMount(() => {
    if (user) 
      fetchUsers();
    else
      goto('/login');   
  });

  function startEdit(u: any) {
    editing = u.id;
    editUsername = u.username;
    editEmail = u.email;
  }

  async function saveEdit(id: number) {
    const res = await fetch(`http://localhost:5000/users/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        username: editUsername,
        email: editEmail,
      }),
    });
    if (res.ok) {
      await fetchUsers();
      editing = null;
    } else {
      alert("Failed to update user");
    }
  }

  async function deleteUser(id: number) {
    if (!confirm("Are you sure you want to delete this user?")) return;
    const res = await fetch(`http://localhost:5000/users/${id}`, {
      method: "DELETE",
      credentials: "include",
    });
    if (res.ok) {
      users = users.filter((u) => u.id !== id);
    } else {
      alert("Failed to delete user");
    }
  }
</script>

<h1>Welcome, {user?.username}!</h1>
<p>Your role: {user?.role}</p>

{#if !isAdmin}
  <UserList {users}/>
{:else }
  <h2>Admin – User Management</h2>
  <div class="overflow-x-auto shadow-md border border-gray-200 bg-white p-4">
    <div class="mt-4">
      <form on:submit|preventDefault={createUser} class="space-y-4">
        <input 
          type="text"          
          bind:value={newUsername} 
          placeholder="Username" 
          class="text-sm px-2 py-1 border rounded-md"
          required 
        />
        <input 
          type="email" bind:value={newEmail} 
          placeholder="Email" 
          class="text-sm px-2 py-1 border rounded-md"
          required 
        />
        <input 
          type="password" bind:value={newPassword} 
          placeholder="Password" 
          class="text-sm px-2 py-1 border rounded-md"
          required 
        />
        <select bind:value={newRole} class="text-sm px-2 py-1 border rounded-md">
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
        <button 
          type="submit"
          class="text-sm bg-blue-600 hover:bg-blue-700 text-white font-semibold py-1 rounded-md"
        >
          Create User
        </button>
      </form>
    </div>
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-100">
        <tr>
          <th class="px-4 py-2 text-left text-sm font-semibold text-gray-700">Name</th>
          <th class="px-4 py-2 text-left text-sm font-semibold text-gray-700">Email</th>
          <th class="px-4 py-2 text-left text-sm font-semibold text-gray-700">Role</th>
          <th class="px-4 py-2 text-sm font-semibold text-gray-700">Actions</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100">
        {#each users as u}
          <tr class="hover:bg-gray-50">
            {#if editing === u.id}
              <td class="px-4 py-2">
                <input bind:value={editUsername} class="w-full px-2 py-1 border rounded" />
              </td> 
              <td class="px-4 py-2">
                <input bind:value={editEmail} class="w-full px-2 py-1 border rounded"/>
              </td>
              <td class="px-4 py-2 space-x-2 text-center">
                <button on:click={() => saveEdit(u.id)} class="text-green-600 hover:underline">Save</button>
                <button on:click={() => (editing = null)} class="text-gray-500 hover:underline">Cancel</button>
              </td>
            {:else}
                <td class="px-4 py-2 text-sm text-gray-900">{u.username}</td>
                <td class="px-4 py-2 text-sm text-gray-600">{u.email}</td>
                <td class="px-4 py-2 text-sm text-gray-600">{u.role}</td>
                <td class="px-4 py-2 space-x-2 text-center">
                  <button on:click={() => startEdit(u)} class="text-blue-600 hover:underline">Edit</button>
                  <button on:click={() => deleteUser(u.id)} class="text-red-600 hover:underline">Delete</button>
                </td>
            {/if}           
          </tr>
        {/each}
      </tbody>
    </table>

  </div> 
{/if}

