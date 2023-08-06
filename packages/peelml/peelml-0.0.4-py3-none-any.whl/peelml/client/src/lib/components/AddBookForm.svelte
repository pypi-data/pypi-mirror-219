<script>
  import { createEventDispatcher } from "svelte";

  let dispatch = createEventDispatcher();

  let title;
  let author;

  const addBook = () => {
    const book = {
      id: Math.random(),
      title,
      author,
    };
    dispatch("addBookEvent", book);
  };
</script>

<form on:submit|preventDefault={addBook}>
  <input type="text" placeholder="title" bind:value={title} />
  <input type="text" placeholder="author" bind:value={author} />
  <button>Add Book</button>
</form>
