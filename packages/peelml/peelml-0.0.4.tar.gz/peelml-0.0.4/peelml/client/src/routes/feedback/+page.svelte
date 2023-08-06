<script>
  import HorizontalStackedBar from "../../lib/feedback/HorizontalStackedBar.svelte";
  import QATable from "../../lib/feedback/QATable.svelte";
  import ColumnChart from "../../lib/feedback/ColumnChart.svelte";
  import HistogramAnswer from "../../lib/feedback/HistogramAnswer.svelte";
  import HistogramQuestion from "../../lib/feedback/HistogramQuestion.svelte";
  import MetricCardAbsolute from "../../lib/feedback/MetricCardAbsolute.svelte";
  import MetricCardPercentage from "../../lib/feedback/MetricCardPercentage.svelte";
</script>

<div class="feedback-container">
  <div class="feedback-left">
    <div class="left-text">
      <div class="card-1">
        <MetricCardAbsolute />
      </div>
      <div class="card-2">
        <MetricCardPercentage />
      </div>
    </div>
    <div class="left-confidence">
      <HorizontalStackedBar />
    </div>
    <div class="left-question">
      <ColumnChart feedback={"Bad"} />
    </div>
    <div class="left-filter">
      <HistogramQuestion />
    </div>
    <div class="left-filter2">
      <HistogramAnswer />
    </div>
  </div>
  <div class="feedback-right">
    <div class="right-chart">
      <div class="right-chart-1" />
      <div class="right-chart-2" />
    </div>
    <div class="right-table">
      <QATable />
    </div>
  </div>
</div>

<style>
  .feedback-container {
    border-bottom: var(--line);
    border-right: var(--line);
    display: grid;
    grid-template-columns: 30% 70%;
    grid-template-rows: 100%;
    width: 100%;
    height: calc(100vh - var(--headerHeight));
  }
  .feedback-left {
    border-bottom: var(--line);
    display: grid;
    grid-template-columns: 100%;
    grid-template-rows: 25% 25% 25% 12.5% 12.5%;
  }
  .left-text {
    text-align: center;
    border-bottom: var(--line);
    border-right: var(--line);
    display: grid;
    grid-template-rows: 100%;
    grid-template-columns: 50% 50%;
  }
  .left-confidence {
    text-align: center;
    border-bottom: var(--line);
    border-right: var(--line);
    display: grid;
    grid-template-rows: 25% 75%;
  }
  .left-question {
    border-bottom: var(--line);
    border-right: var(--line);
  }
  .left-filter {
    border-bottom: var(--line);
    border-right: var(--line);
  }
  .feedback-right {
    border-bottom: var(--line);
    border-right: var(--line);
    display: grid;
    grid-template-columns: 100%;
    grid-template-rows: 30% 70%;
    grid-template-rows: 0% 100%;
  }
  .right-chart {
    border-bottom: var(--line);
    border-right: var(--line);
    display: grid;
    grid-template-columns: 50% 50%;
    grid-template-rows: 100%;
  }
  .right-chart-1,
  .right-chart-2 {
    border-right: var(--line);
  }
  .right-table {
    border-bottom: var(--line);
    border-right: var(--line);
  }
  .right-download {
    border-bottom: var(--line);
    border-right: var(--line);
  }
  .card-1 {
    border-right: var(--line);
  }
</style>
