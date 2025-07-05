<script lang="ts">
  import { createEventDispatcher, onMount } from 'svelte';
  import { Upload, Image } from 'lucide-svelte';
  import { alert, alertType, displayAlert } from '$lib/stores/alerts';


  export let userId: string;
  export let uploadUrl: string = '/api/upload';
  export let avatarUrl: string | null = null; // Optional preview image

  const dispatch = createEventDispatcher();
  

  let fileInput: HTMLInputElement;
  let selectedFile: File | null = null;
  let previewUrl: string | null = null;
  let status = '';

  function openFileDialog() {
    fileInput.click();
  }

  function handleFileSelect(event: Event) {
    const target = event.target as HTMLInputElement;
    selectedFile = target.files?.[0] || null;

    if (selectedFile) {
      previewUrl = URL.createObjectURL(selectedFile);
      avatarUrl = previewUrl; 
      status = `Selected: ${selectedFile.name}`;
      dispatch('fileSelected', { file: selectedFile }); // Dispatch event
    }
  }

  async function uploadFile() {
    if (!selectedFile || !userId) {
      status = 'No file or user ID provided.';
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('user_id', userId);

    try {
      const res = await fetch(uploadUrl, {
        method: 'POST',
        body: formData
      });

      if (res.ok) {
        const result = await res.json();
        status = `✅ Uploaded: ${result.file_key}`;
        displayAlert(`File uploaded successfully: ${result.file_key}`, 'success');
        dispatch('uploadComplete', { success: true, file: result });

        // Optionally update avatar preview
        //previewUrl = `s3://serverless-framework-deployments-us-east-1-bea978b8-d2fe/testadmin/${result.file_key}`;
      } else {
        const err = await res.json();
        status = `❌ Error: ${err.error}`;
        dispatch('uploadComplete', { success: false, error: err.error });
        displayAlert(`Upload failed: ${err.error}`, 'error');
      }
    } catch (error) {
      status = `❌ Exception: ${error}`;
      dispatch('uploadComplete', { success: false, error });
      displayAlert(`Upload failed: ${error}`, 'error'); 
    }
  }
</script>

<!-- 🔐 Hidden file input -->
<input
  type="file"
  accept="image/*"
  bind:this={fileInput}
  on:change={handleFileSelect}
  class="hidden"
/>

<!-- 🧱 Stylized Card -->
<div class="max-w-sm mx-auto p-4 bg-white shadow-md rounded-xl space-y-4">
  <div class="flex flex-col items-center">
    <!-- Avatar / Image Preview -->
    <button
      type="button"
      class="focus:outline-none"
      on:click={openFileDialog}
      aria-label="Change user avatar"
    >
      <img
        src={previewUrl || avatarUrl || '/avatar.jpg'}
        alt="User Avatar"
        class="w-24 h-24 rounded-full object-cover border-2 border-gray-300 cursor-pointer"
        draggable="false"
      />
    </button>

    <p class="text-sm mt-2 text-gray-500">{status}</p>
  </div>

  <!-- Buttons -->
  <div class="flex justify-center space-x-4">
    <button
      on:click={openFileDialog}
      class="flex items-center bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 text-sm"
    >
      <Image size="16" class="mr-1" /> Choose
    </button>

    <button
      on:click={uploadFile}
      class="flex items-center bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 text-sm"
      disabled={!selectedFile}
    >
      <Upload size="16" class="mr-1" /> Upload
    </button>
  </div>
</div>
