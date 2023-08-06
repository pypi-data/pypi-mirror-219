<script>
  import Modal from "$lib/components/Modal.svelte";
  import AddBookForm from "$lib/components/AddBookForm.svelte";

  export let name;

  let showModal = false;
  let books = [];

  const toggleModal = () => {
    showModal = !showModal;
  };

  const addBook = (event) => {
    const book = event.detail;
    books = [book, ...books];
    showModal = false;
  };
</script>

<Modal {showModal} on:click={toggleModal}>
  <AddBookForm on:addBookEvent={addBook} />
</Modal>
<main>
  <h1>Hello {name}!</h1>
  <button on:click={toggleModal}>Show Modal</button>
  {#each books as book (book.id)}
    <div>
      <h4>{book.title} - {book.author}</h4>
    </div>
  {/each}
</main>
