<script lang="ts">
  export let message = "";
  export let type: "success" | "error" | "info" | "warning" = "info";
  export let onClose: () => void = () => {};
</script>

<div
  class={`flex items-center justify-between p-4 mb-4 rounded-lg border-l-4 shadow-md transition-all duration-300
    ${type === "success" ? "bg-green-50 border-green-500 text-green-800" : ""}
    ${type === "error" ? "bg-red-50 border-red-500 text-red-800" : ""}
    ${type === "info" ? "bg-blue-50 border-blue-500 text-blue-800" : ""}
    ${type === "warning" ? "bg-yellow-50 border-yellow-500 text-yellow-800" : ""}`}>
  <div class="flex-1">{message}</div>
  <button
    class="ml-4 text-sm font-bold"
    on:click={onClose}
    aria-label="Close"
  >
    ✕
  </button>
</div>
