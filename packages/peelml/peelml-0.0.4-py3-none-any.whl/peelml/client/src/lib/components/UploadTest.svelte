<script>
  let content = "hey";
  let serverResponse = null;
  let loading = false;

  async function handleClick(event) {
    event.preventDefault();
    console.log("event", event);
    loading = true;

    let todo = { content };
    console.log("todo", todo);
    const response = await fetch("/api/uploadTest", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(todo),
    });
    const data = await response.json();
    console.log("response", data);
    loading = false;
    serverResponse = data;
  }
</script>

<div>
  <h1>Upload</h1>
  <form on:submit|preventDefault={handleClick}>
    <input type="text" bind:value={content} />
    <button type="submit">
      {content}
    </button>
  </form>
  {#if loading}
    <div id="loader" />
  {/if}
  {#if !loading && serverResponse}
    <p>Server response: {JSON.stringify(serverResponse)}</p>
  {/if}
</div>
