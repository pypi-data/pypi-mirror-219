<script>
  import { writable } from "svelte/store";

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

  async function kickoffInference() {
    console.log("running inference");
    setLoading(true);
    const response = await fetch("/api/index", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: "hey" }),
    });
    // once the indexing has run, set index to true
    setLoading(false);
    setIndexed(true);
  }

  async function sendMessage(event) {
    event.preventDefault();
    console.log("event", event);
    loading = true;
    chatLog = [...chatLog, { user: "me", message: `${message}` }];
    input = "";
    let todo = { message };
    console.log("todo", todo);
    const messages = chatLog.map((message) => message.message).join("\n");
    console.log("messages", messages);
    const res = await fetch(`/api/inference/${message}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(todo),
    });
    const data = await res.json();
    console.log("response", data);
    response = data["answer"];
    reply = true;
    loading = false;
    serverResponse = data;
    chatLog = [...chatLog, { user: "gpt", message: `${data.answer}` }];
  }
</script>

<div>
  <p>Documents Indexed! Query below.</p>
  <form on:submit|preventDefault={sendMessage}>
    <input type="text" bind:value={message} />
    <button type="submit">Ask Question</button>
  </form>
</div>
