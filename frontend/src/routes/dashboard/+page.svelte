<script lang="ts">
  import { onMount } from "svelte";
  import { session } from "$lib/stores/session";
  import LogOutButton from "$lib/components/LogoutButton.svelte";

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
    if (isAdmin) fetchUsers();
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


{#if isAdmin}
  <h2>Admin – User Management</h2>
  {#if error}
    <p style="color: red;">{error}</p>
  {:else}
    <h3>Create New User</h3>
    <form on:submit|preventDefault={createUser}>
      <input bind:value={newUsername} placeholder="Username" required />
      <input bind:value={newEmail} placeholder="Email" required />
      <input type="password" bind:value={newPassword} placeholder="Password" required />
      <select bind:value={newRole}>
        <option value="user">User</option>
        <option value="admin">Admin</option>
      </select>
      <button type="submit">Create</button>
    </form>
    <h3>Edit existing User</h3>
    <ul>
      {#each users as u}
        <li>
          {#if editing === u.id}
            <input bind:value={editUsername} />
            <input bind:value={editEmail} />
            <button on:click={() => saveEdit(u.id)}>Save</button>
            <button on:click={() => (editing = null)}>Cancel</button>
          {:else}
            <strong>{u.username}</strong> – {u.email} ({u.role})
            <button on:click={() => startEdit(u)}>Edit</button>
            <button on:click={() => deleteUser(u.id)}>Delete</button>
          {/if}
        </li>
      {/each}
    </ul>
  {/if}
{/if}
<LogOutButton />
