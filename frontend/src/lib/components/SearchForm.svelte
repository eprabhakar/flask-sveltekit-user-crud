<!-- src/lib/components/SearchForm.svelte -->
<script lang="ts">
  
    export let onSearch: (query: string) => void = (query: string) => {};

    let query = "";    

</script>

<div class="mt-4 px-2">
    <form
        on:submit|preventDefault={() => onSearch(query)}
        class="w-full max-w-md mb-6 flex gap-2"
    >
        <div class="relative flex-grow">
            <input
                type="text"
                bind:value={query}
                on:input={() => onSearch(query)}
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
