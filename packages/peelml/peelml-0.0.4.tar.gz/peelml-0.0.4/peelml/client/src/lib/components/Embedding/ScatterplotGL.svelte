<script>
  import { onMount } from "svelte";
  import { data } from "./data/projection";
  import { Dataset } from "./data";
  import { makeSequences } from "./sequences";
  import { ScatterGL } from "scatter-gl";
  import { projections } from "../../../store";

  let dataPoints = [];
  let metadata = [];
  let lastSelectedPoints = [];
  let renderMode = "points";
  let scatterGL;
  let sequences;
  let dataset;
  let message = "";

  let is3D = true;
  let isRotating = true;
  let showSequences = false;

  const hues = [...new Array(10)].map((_, i) => Math.floor((255 / 10) * i));

  const lightTransparentColorsByLabel = hues.map(
    (hue) => `hsla(${hue}, 100%, 50%, 0.05)`
  );
  const heavyTransparentColorsByLabel = hues.map(
    (hue) => `hsla(${hue}, 100%, 50%, 0.75)`
  );
  const opaqueColorsByLabel = hues.map((hue) => `hsla(${hue}, 100%, 50%, 1)`);

  onMount(() => {
    message = "";
    $projections.projection.forEach((vector, index) => {
      const labelIndex = data.labels[index];
      dataPoints.push(vector);
      metadata.push({
        labelIndex,
        label: data.labelNames[labelIndex],
      });
    });

    sequences = makeSequences(dataPoints, metadata);
    dataset = new Dataset(dataPoints, metadata);

    scatterGL = new ScatterGL(document.getElementById("container"), {
      onClick: (point) => {
        message = `click ${point}`;
      },
      onHover: (point) => {
        message = `hover ${point}`;
      },
      onSelect: (points) => {
        if (points.length === 0 && lastSelectedPoints.length === 0) {
          message = "no selection";
        } else if (points.length === 0 && lastSelectedPoints.length > 0) {
          message = "deselected";
        } else if (points.length === 1) {
          message = `selected ${points}`;
        } else {
          message = `selected ${points.length} points`;
        }
      },
      orbitControls: {
        zoomSpeed: 1.125,
      },
    });
    scatterGL.render(dataset);

    // Add in a resize observer for automatic window resize.
    window.addEventListener("resize", () => {
      scatterGL.resize();
    });
  });

  // Function declarations for event handlers
  function handleInteractionChange(e) {
    if (e.target.value === "pan") {
      scatterGL.setPanMode();
    } else if (e.target.value === "select") {
      scatterGL.setSelectMode();
    }
  }

  function toggleOrbit() {
    if (scatterGL.isOrbiting()) {
      // isRotating = true;
      scatterGL.stopOrbitAnimation();
    } else {
      // isRotating = false;

      scatterGL.startOrbitAnimation();
    }
  }

  function handleDimensionChange() {
    scatterGL.setDimensions(is3D ? 3 : 2);
  }

  function handleSequenceChange() {
    scatterGL.setSequences(showSequences ? sequences : []);
  }

  function handleRenderModeChange() {
    console.log("renderMode", renderMode);
    if (renderMode === "points") {
      scatterGL.setPointRenderMode();
    } else if (renderMode === "text") {
      scatterGL.setTextRenderMode();
    }
  }

  let colorMode = "default"; // assuming 'default' is the initial color mode

  function handleColorModeChange() {
    if (colorMode === "default") {
      scatterGL.setPointColorer(null);
    } else if (colorMode === "label") {
      scatterGL.setPointColorer((i, selectedIndices, hoverIndex) => {
        const labelIndex = dataset.metadata[i]["labelIndex"];
        const opaque = renderMode !== "points";
        if (opaque) {
          return opaqueColorsByLabel[labelIndex];
        } else {
          if (hoverIndex === i) {
            return "red";
          }

          // If nothing is selected, return the heavy color
          if (selectedIndices.size === 0) {
            return heavyTransparentColorsByLabel[labelIndex];
          }
          // Otherwise, keep the selected points heavy and non-selected light
          else {
            const isSelected = selectedIndices.has(i);
            return isSelected
              ? heavyTransparentColorsByLabel[labelIndex]
              : lightTransparentColorsByLabel[labelIndex];
          }
        }
      });
    }
  }

  let interactionMode = "pan";

  function setColorMode(mode) {
    colorMode = mode;
    handleColorModeChange();
  }

  function handleInteractionModeChange(mode) {
    interactionMode = mode;
    if (interactionMode === "pan") {
      scatterGL.setPanMode();
    } else if (interactionMode === "select") {
      scatterGL.setSelectMode();
    }
  }
</script>

<div id="grid-container">
  <div id="container" />
  <div id="controls">
    <h5>{message}</h5>
    <hr />
    <div class="interactions control">
      <h5>Controls</h5>
      <button
        class:active={interactionMode === "pan"}
        on:click={() => handleInteractionModeChange("pan")}
      >
        Pan
      </button>
      <button
        class:active={interactionMode === "select"}
        on:click={() => handleInteractionModeChange("select")}
      >
        Select
      </button>
    </div>
    <div>
      <label for="orbit-render">
        <input
          type="checkbox"
          id="orbit-render"
          name="orbit"
          bind:checked={isRotating}
          on:change={toggleOrbit}
        />
        <span>Rotate</span>
      </label>
    </div>
    <hr />
    <div class="render-modes control">
      <h5>Render</h5>
      <label for="point-render">
        <input
          type="radio"
          id="point-render"
          name="render"
          value="points"
          bind:group={renderMode}
          on:change={handleRenderModeChange}
        />
        <span>Points</span>
      </label>

      <label for="text-render">
        <input
          type="radio"
          id="text-render"
          name="render"
          value="text"
          bind:group={renderMode}
          on:change={handleRenderModeChange}
        />
        <span>Text</span>
      </label>
      <div id="switch-3D">
        <label for="dimensions-render">
          <input
            type="checkbox"
            id="dimensions-render"
            name="3D"
            bind:checked={is3D}
            on:change={handleDimensionChange}
          />
          <span class="mdl-switch__label">3D</span>
        </label>
      </div>
      <div id="switch-sequences">
        <label for="sequences-render">
          <input
            type="checkbox"
            id="sequences-render"
            name="sequences"
            bind:checked={showSequences}
            on:change={handleSequenceChange}
          />
          <span class="mdl-switch__label">Show Connections</span>
        </label>
      </div>
    </div>

    <div class="color control">
      <h5>Color by</h5>
      <button
        class={colorMode === "default" ? "active" : ""}
        on:click={() => setColorMode("default")}
      >
        Nothing
      </button>
      <button
        class={colorMode === "label" ? "active" : ""}
        on:click={() => setColorMode("label")}
      >
        Extension
      </button>
    </div>
    <hr />
  </div>
</div>

<style>
  #grid-container {
    display: grid;
    grid-template-columns: 80% 20%;
    height: calc(100vh - var(--headerHeight));
  }

  #container {
    grid-column: 1 / 2;
    width: 100%;
    height: 100%;
  }

  #controls {
    grid-column: 2 / 3;
    padding: 10px;
  }

  #switch-3D {
    margin-top: 10px;
  }

  .color.control button {
    background-color: white;
    color: black;
    border: none;
    cursor: pointer;
    padding: 10px;
    margin-right: 5px;
    display: inline-block;
    transition: all 0.5s;
  }
  .color.control button.active {
    background-color: black;
    color: white;
  }

  .interactions button {
    background-color: white;
    color: black;
    border: none;
    padding: 10px;
    margin: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
  }

  .interactions button.active {
    background-color: black;
    color: white;
  }
</style>
