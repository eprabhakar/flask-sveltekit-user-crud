<script lang="ts">
  import { onMount } from "svelte";
  import { session } from "$lib/stores/session";
  import UserList from "$lib/components/UserList.svelte";
  import { goto } from '$app/navigation';
  import { Plus, Search } from 'lucide-svelte';
  import * as api from '$lib/api/users';
  import PasswordResetModal from '$lib/components/PasswordResetModal.svelte';
  import { alert, alertType, displayAlert } from '$lib/stores/alerts';
  //import { displayAlert } from '$lib/stores/alerts';
  import CustomAlert from '$lib/components/CustomAlert.svelte';

  type AlertType = "success" | "error" | "info" | "warning" | undefined;

  //$: show = $alert !== '';
  let showAlert = false; // show alert state
  let filteredUsers: any[] = []; // Users filtered based on search


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
  $: displayUsers = query.trim() ? filteredUsers : users;
  let usersOfSearch = [];

  let selectedUser:any;
  let showResetModal = false;

  function myAlert(message: string, type: AlertType) {
    showAlert = true;
    displayAlert(message, type);
    setTimeout(() => showAlert=false, 3000);
  }

  function handleResetSuccess() {
    myAlert("Password reset successful!", "success");
  }

  function openResetModal(user:any) {
    selectedUser = user;
    showResetModal = true;
  }

  // Toggle create form visibility
  function toggleCreateForm() {
    showCreateForm = !showCreateForm;
    showSearchForm = false; 
    query = ''; // Reset search query when showing create form
  }

  let showSearchForm = false;

  // Toggle search form visibility
  function toggleSearchForm() {
    showSearchForm = !showSearchForm;
    showCreateForm = false; // Hide create form when showing search form
    if(!showSearchForm) {
      query = ''; // Reset search query when closing the form
      //loadUsers(); // Fetch all users again
    }
  }

  // Load users from the API
  async function loadUsers() {
    try {
      users = await api.fetchUsers();
    } catch (e) {
      if (e instanceof Error) {
        error = e.message;
      } else {
        error = String(e);
      }
      if (error) {
        myAlert(error, "error");
        console.error("Failed to load users:", error);
      }      
    }
  }

  // Handle user creation
  async function handleCreate() {
    try {
      const user = await api.createUser({ username: newUsername, email: newEmail, password: newPassword, role: newRole });
      users = [...users, user];
      newUsername = newEmail = newPassword = "";
    } catch (e) {
      if (e instanceof Error) {
        error = e.message;
      } else {
        error = String(e);
      }
    }
    if (error) {
      myAlert(error, "error");
    } else {
      myAlert("User created successfully!", "success");
    }
  }   

  // Load users on mount if user is logged in
  onMount(() => {
    if (user) {
        loadUsers();
        console.log("User:"+ api.myname); 
      }  
    else goto("/login");
  });

  // Handle search form submission
  async function handleSearchSubmit() {
    handleSearchInput();
  }
  // Filter users based on search query
  function handleSearchInput() {
    const lowerQuery = query.toLowerCase();
    filteredUsers = users.filter(user =>
      user.username.toLowerCase().includes(lowerQuery) ||
      user.email.toLowerCase().includes(lowerQuery)
    );
    
  }
  // Start editing a user
  function startEdit(u: any) {
    editing = u.id;
    editUsername = u.username;
    editEmail = u.email;
  }

  async function handleUpdate(id: number) {
    try {
      await api.updateUser(id, { username: editUsername, email: editEmail });
      await loadUsers();
      editing = null;
      error = null;
    } catch (e) {
      if (e instanceof Error) {
        error = e.message;
      } else {
        error = String(e);
      }
    }
    if (error) {
      myAlert(error, "error");
    } else {
      myAlert("User updated successfully!", "success");
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
      myAlert("User deleted successfully!", "success");
    } else {
      //alert("Failed to delete user");
      const err = await res.json();
      if (err.error) {
        myAlert(err.error, "error");
      } else {
        myAlert("Failed to delete user.", "error");
      }
    }
  }

</script>

{#if showAlert}
  <div class="w-full max-w-5xl mx-auto mt-4">
    <CustomAlert type={$alertType} message={$alert} />
  </div>
{/if}

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
          <form on:submit|preventDefault={handleCreate} class="space-y-4">
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
          <form on:submit|preventDefault={handleSearchSubmit} class="w-full max-w-md mb-6 flex gap-2">
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
            {#each displayUsers as user}
              <tr class="hover:bg-gray-50">
                {#if editing === user.id}
                  <td class="px-4 py-2">
                    <input bind:value={editUsername} class="w-full px-2 py-1 border rounded" />
                  </td> 
                  <td class="px-4 py-2">
                    <input bind:value={editEmail} class="w-full px-2 py-1 border rounded"/>
                  </td>
                  <td class="px-4 py-2 space-x-2 text-center">
                    <button on:click={() => handleUpdate(user.id)} class="text-green-600 hover:underline">Save</button>
                    <button on:click={() => (editing = null)} class="text-gray-500 hover:underline">Cancel</button>
                  </td>
                {:else}
                  <td class="px-4 py-2 text-sm text-gray-900">{user.username}</td>
                  <td class="px-4 py-2 text-sm text-gray-600">{user.email}</td>
                  <td class="px-4 py-2 text-sm text-gray-600">{user.role}</td>
                  <td class="px-4 py-2 space-x-2 text-center">
                    <button on:click={() => startEdit(user)} class="text-blue-600 hover:underline">Edit</button>
                    <button on:click={() => deleteUser(user.id)} class="text-red-600 hover:underline">Delete</button>
                    <button on:click={() => openResetModal(user)} class="text-blue-500 hover:underline ml-2" >Reset Password</button>
                  </td>
                {/if}
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
      <PasswordResetModal
        user={selectedUser}
        visible={showResetModal}
        onClose={() => showResetModal = false}
        onSuccess={handleResetSuccess}
      />
    </div>
  </main>
{/if}


