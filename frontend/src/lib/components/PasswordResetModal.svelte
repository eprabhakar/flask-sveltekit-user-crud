<script lang="ts">
  export let user: any;
  export let visible: boolean;
  export let onClose: () => void;
  export let onSuccess: () => void;

  let password = "";
  let confirmPassword = "";
  let error = "";

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
    } else {
      const err = await res.json();
      alert('Error resetting password: ' + err.error);
      error = err.error || "Failed to reset password.";
    }
  }
</script>

{#if visible}
  <div class="fixed inset-0 z-50 bg-gray bg-gray-100 bg-opacity-50 flex items-center justify-center">
    <div class="bg-white rounded-lg p-6 w-full max-w-md shadow-lg">
      <h2 class="text-lg font-semibold mb-4">Reset Password for {user.username}</h2>

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
  </div>
{/if}
