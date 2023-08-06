<script>
  import { writable } from "svelte/store";
  // import UploadedDocuments from "./UploadedDocuments.svelte";
  import UploadFiles from "$lib/components/UploadFiles.svelte";
  // import bruceIcon from "../assets/bruce.svg";
  import UploadTest from "$lib/components/UploadTest.svelte";
  let selectedFile = null;
  let serverResponse = null;
  let loading = false;
  let uploadedDocs = [];
  let indexed = false;
  let message = "What is gradient descent?";
  let response = "";
  let reply = false;
  let input = "";
  let chatLog = [];

  // ... rest of the functions goes here, you should change all setState functions to simple assignments ...

  async function handleSubmit(event) {
    event.preventDefault();
    // rest of your code...
  }

  // ... rest of your functions...
</script>

<div class="myComponentStyle">
  {#if !serverResponse}
    <!-- <UploadTest /> -->
    <UploadFiles />
  {/if}
  <!--   
    {#if !indexed && serverResponse}
      <UploadedDocuments {uploadedDocs} />
      <button type="submit" value="Upload File" on:click={kickoffInference}>
        Index Files
      </button>
    {/if}
    
    {#if loading}
      <div id="loader"></div>
    {/if}
    
    {#if indexed}
      <p>Documents Indexed! Query below.</p>
      <form on:submit|preventDefault={sendMessage}>
        <input
          type="text"
          bind:value={message}
        />
        <button type="submit" value="Add Todo">
          Ask Question
        </button>
      </form>
    {/if}
  
    {#if indexed && reply}
      <section className="chatbox">
        <div className="chat-log">
          {#each chatLog as message, index (index)}
            <ChatMessage {message} />
          {/each}
        </div>
      </section>
    {/if} -->
</div>

<style>
  .myComponentStyle {
    margin: auto;
    width: 600px;
    text-align: center;
  }
</style>
