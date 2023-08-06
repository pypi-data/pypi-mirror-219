<script>
  import { writable } from "svelte/store";

  let files = [];
  let selectedFiles = false;
  let uploadedFiles;
  let loading = false;
  let indexed = false;

  const handleFileChange = (event) => {
    const targetFiles = event.target.files;

    uploadedFiles = Array.from(targetFiles).map((file) => ({
      name: file.name,
      size: file.size,
      extension: file.name.split(".").pop(),
    }));

    uploadedFiles.forEach((file) =>
      console.log(`Size of ${file.name}: ${file.size} bytes`)
    );

    files = uploadedFiles;
    selectedFiles = true;
  };

  async function kickoffInference() {
    console.log("running inference");
    loading = true;
    const response = await fetch("/api/index", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: "hey" }),
    });
    const data = await response.json();
    console.log("response", data);
    // once the indexing has run, set index to true
    loading = false;
    indexed = true;
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(files);
    console.log("submit!");
    // Emit an event instead of calling the prop directly
    // dispatch("fileupload", true);
  };
</script>

<div>
  {#if selectedFiles}
    <p>
      These are the files your LLM will use to learn from.
      <br />
      Select more, or click Process Files to continue.
    </p>
  {:else}
    <div>
      <h3>Upload Files</h3>
      <p>Select the files your LLM will use to learn from.</p>
    </div>
  {/if}
  <form on:submit|preventDefault={handleSubmit}>
    {#if !selectedFiles}
      <button class="submit-button" type="submit"> Process Files </button>
      <a href="/process">Go!</a>
    {/if}
    <br />
    <input type="file" on:change={handleFileChange} multiple />
  </form>

  <form on:submit|preventDefault={kickoffInference}>
    <button type="submit" value="Upload File"> Index Fileees </button>
    <br />
    <!-- <input type="file" on:change={handleFileChange} multiple /> -->
  </form>
</div>
