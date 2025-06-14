<script lang="ts">
  import CustomAlert from '$lib/components/CustomAlert.svelte';
  import { alert, alertType } from '$lib/stores/alerts';
  import { displayAlert } from '$lib/stores/alerts';
  export let user: any;
  export let visible: boolean;
  export let onClose: () => void;
  export let onSuccess: () => void;
  //$: show = $alert !== '';

  let password = "";
  let confirmPassword = "";
  let error = "";

  //let showAlert = false;
  let alertMessage = "User created successfully!";
  //let showAlert = false;

  function closeAlert() {
    password = "";
    confirmPassword = "";
    //showAlert = false;
  }

  async function resetPassword(userId: number, password: string) {
    if (password.length < 6) {
      error = "Password must be at least 6 characters long.";
      return;
    }
    if (password !== confirmPassword) {
      error = "Passwords do not match.";
      return;
    }

    const res = await fetch(`http://localhost:5000/users/${userId}/reset-password`, {
      method: "PUT",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password: password }),
    }); 

    if (res.ok) {
      error = "";
      onSuccess();
      onClose();
      password = "";
      confirmPassword = "";
      alertMessage = "Password reset successfull!";
      //showAlert = true;
      //displayAlert(alertMessage, 'success');
      //showAlert=true
    } else {
      const err = await res.json();
      password = "";
      confirmPassword = "";
      //displayAlert(err.error || "Failed to reset password.", "error");
      //showAlert = true;
      error = err.error || "Failed to reset password.";
    }
    //setTimeout(() => showAlert=false, 3000);
    closeAlert();
  }


</script>



{#if visible}
  <div class="absolute top-20 left-1/2 transform -translate-x-1/2 z-50 p-6 bg-gray-100 shadow-lg rounded-md w-80">
      <h2 class="text-lg text-blue-600 font-semibold mb-4">Reset Password for : {user.username}</h2>

      <input
        type="password"
        bind:value={password}
        placeholder="New Password"
        class="w-full mb-3 p-2 border rounded text-sm"
      />
      <input
        type="password"
        bind:value={confirmPassword}
        placeholder="Confirm Password"
        class="w-full mb-3 p-2 border rounded text-sm"
      />

      {#if error}
        <p class="text-red-600 text-sm mb-3">{error}</p>
      {/if}

      <div class="flex justify-end space-x-2">
        <button on:click={onClose} class="px-4 py-2 bg-gray-300 text-black rounded">Cancel</button>
        <button on:click={()=>resetPassword(user.id, password)} class="px-4 py-2 bg-blue-600 text-white rounded">Reset</button>
      </div> 
  </div>

{/if}


