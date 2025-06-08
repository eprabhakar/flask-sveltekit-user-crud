<script lang="ts">
  import { onMount } from "svelte";
  import { session } from "$lib/stores/session";
  import UserList from "$lib/components/UserList.svelte";
  import { goto } from '$app/navigation';
  import { Plus, Search } from 'lucide-svelte';

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

  let showCreateForm = false;

  let query = '';
  let usersOfSearch = [];

  function toggleCreateForm() {
    showCreateForm = !showCreateForm;
  }

  let showSearchForm = false;

  function toggleSearchForm() {
    showSearchForm = !showSearchForm;
    if(!showSearchForm) {
      query = ''; // Reset search query when closing the form
      fetchUsers(); // Fetch all users again
    } 
  }

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

  async function handleSubmit() {
    console.log("Search query:", query);
    const res = await fetch(`http://localhost:5000/search?q=${encodeURIComponent(query)}`);
    users = await res.json();
  }

  function handleSearchInput() {
    //handleSubmit( new Event('submit'));
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



{#if !isAdmin}
  <UserList {users}/>
{:else }
  <main class="flex-1 overflow-auto ">
    <!-- Main Utility Card with Content -->
    <div class="w-full bg-white shadow-md overflow-hidden">
      <!-- Title and actions -->
      <div class="px-4 bg-white shadow-md border border-gray-200 border-collapse flex items-center justify-between">
        <!-- Title / Breadcrumb -->
        <div class="text-sm font-semibold text-gray-800">
          Admin >> Manage Users
        </div>

        <!-- Actions -->
        <div class="flex space-x-1 p-1">
          <button
            class="inline-flex items-center gap-2 bg-gray-100 text-gray text-sm px-2 py-2  hover:bg-gray-300 transition rounded-md"
            on:click={toggleCreateForm}
            aria-label="Create New"
          >
            <span class="flex items-center justify-center w-6 h-6 bg-white text-blue-600 rounded-full">
              <Plus size="12" stroke-width="2" />
            </span>
            <span class="text-sm font-medium">New</span>            
          </button>
          <button
            class="inline-flex items-center gap-2 bg-gray-100 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-300 transition" 
            on:click={toggleSearchForm}
            aria-label="Search"
          >
            <span class="flex items-center justify-center w-6 h-6 bg-white text-blue-600 rounded-full">
              <Search size="16" />
            </span>
            <span class="text-sm font-medium">Search</span>
          </button>
        </div>
      </div>

      <!-- Main Content Below Header -->
      {#if showCreateForm}
        <div class="mt-4 px-2">
          <form on:submit|preventDefault={createUser} class="space-y-4">
            <input 
              type="text"          
              bind:value={newUsername} 
              placeholder="Username" 
              class="text-sm px-2 py-1 border border-gray-200"
              required 
            />
            <input 
              type="email" bind:value={newEmail} 
              placeholder="Email" 
              class="text-sm px-2 py-1 border border-gray-200 "
              required 
            />
            <input 
              type="password" bind:value={newPassword} 
              placeholder="Password" 
              class="text-sm px-2 py-1 border border-gray-200 "
              required 
            />
            <select bind:value={newRole} class="text-sm px-6 py-1 border border-gray-200 ">
              <option value="user">User</option>
              <option value="admin">Admin</option>
            </select>
            <button 
              type="submit"
              class="text-sm bg-gray-100 hover:bg-gray-300 text-black py-1 px-2"
            >
              Create User
            </button>
          </form>
        </div>
      {/if}

      {#if showSearchForm}
        <div class="mt-4 px-2">
          <form on:submit|preventDefault={handleSubmit} class="w-full max-w-md mb-6 flex gap-2">
            <div class="relative flex-grow">
              <input 
                type="text" 
                bind:value={query} 
                placeholder="username or email" 
                class="text-sm px-2 py-1 border border-gray-200 w-full"
              />
            </div>
            <button
              type="submit"
              class="text-sm bg-gray-100 hover:bg-gray-300 text-black py-1 px-2"
            >
              Search
            </button>
          </form>
        </div>
      {/if}

      <div class="p-2  bg-white">
        <!-- You can replace this with your dynamic content -->
        <table class="min-w-full  border border-gray-200 border-collapse divide-y divide-gray-200">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-4 border border-gray-200 py-2 text-left text-sm font-semibold text-gray-700">Name</th>
              <th class="px-4 border border-gray-200 py-2 text-left text-sm font-semibold text-gray-700">Email</th>
              <th class="px-4 border border-gray-200 py-2 text-left text-sm font-semibold text-gray-700">Role</th>
              <th class="px-4 border border-gray-200 py-2 text-sm font-semibold text-gray-700">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 bg-white">
            {#each users as user}
              <tr class="hover:bg-gray-50">
                {#if editing === user.id}
                  <td class="px-4 py-2">
                    <input bind:value={editUsername} class="w-full px-2 py-1 border rounded" />
                  </td> 
                  <td class="px-4 py-2">
                    <input bind:value={editEmail} class="w-full px-2 py-1 border rounded"/>
                  </td>
                  <td class="px-4 py-2 space-x-2 text-center">
                    <button on:click={() => saveEdit(user.id)} class="text-green-600 hover:underline">Save</button>
                    <button on:click={() => (editing = null)} class="text-gray-500 hover:underline">Cancel</button>
                  </td>
                {:else}
                  <td class="px-4 py-2 text-sm text-gray-900">{user.username}</td>
                  <td class="px-4 py-2 text-sm text-gray-600">{user.email}</td>
                  <td class="px-4 py-2 text-sm text-gray-600">{user.role}</td>
                  <td class="px-4 py-2 space-x-2 text-center">
                    <button on:click={() => startEdit(user)} class="text-blue-600 hover:underline">Edit</button>
                    <button on:click={() => deleteUser(user.id)} class="text-red-600 hover:underline">Delete</button>
                  </td>
                {/if}
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  </main>
{/if}

