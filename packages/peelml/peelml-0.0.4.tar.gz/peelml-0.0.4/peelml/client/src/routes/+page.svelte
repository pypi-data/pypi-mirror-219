<script>
  import Card from "$lib/UI/Card.svelte";
</script>

<div class="page center">
  <h3 class="page-title">{"\u2192"} Your Cambio Application</h3>
  <p>Welcome to your CambioML Hub!</p>
  <p>
    Setting up your own custom large language model has never been easier.
    <br />
    Simply upload your data, then proceed to train and visualize your custom model.
  </p>
  <div class="grid cols-3">
    <Card
      title="Chatbot"
      buttonText="Let's Do It!"
      text="Get started with a new model by uploading your documents to the language model of your choice!"
      link="/upload"
    />
    <Card
      title="Knowledge Graph"
      buttonText="Let's Do It!"
      text="Get started with a new model by uploading your documents to the language model of your choice!"
      link="/upload"
    />
    <Card
      title="Explore Embeddings"
      buttonText="Let's Do It!"
      text="Get started with a new model by uploading your documents to the language model of your choice!"
      link="/upload"
    />
  </div>
</div>
