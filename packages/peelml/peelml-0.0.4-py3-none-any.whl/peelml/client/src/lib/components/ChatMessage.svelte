<script>
  export let message;
</script>

<div class="chat-message {message.user === 'gpt' ? 'chatgpt' : ''}">
  <div class="chat-message-center">
    <div class="avatar {message.user === 'gpt' ? 'chatgpt' : ''}">
      {#if message.user === "gpt"}
        <!-- bot -->
        <!-- <img src={bruceIcon} class="bruce-avatar" alt="Bruce.ai logo" /> -->
      {/if}
    </div>
    <p>{message.message}</p>
  </div>
</div>

<style>
  .chat-message {
    background-color: var(--white);
    border-bottom: var(--line);
  }
  .chat-message.chatgpt {
    background-color: var(--lightGrey);
    color: var(--black);
  }

  .chat-message-center {
    display: flex;
    max-width: 640px;
    margin-left: auto;
    margin-right: auto;
    padding: 12px;
    padding-left: 24px;
    padding-right: 24px;
    align-items: center;
    /* border-top: var(--line); */
  }

  .chat-message-center > p {
    margin-left: 1rem;
  }

  .avatar {
    background: var(--lightgrey);
    border-radius: 50%;
    width: 40px;
    height: 40px;
  }

  .avatar.chatgpt {
    background: var(--primary);
    border-radius: 50%;
    width: 40px;
    height: 40px;
  }

  .message {
    padding-left: 40px;
    padding-right: 40px;
  }
</style>
