<script>
  export let column;
  export let table;

  function getTopFiveFacets(columnId) {
    if (!columnId) return { top5: [], next20: [], hasMore: false };
    const column = table.getColumn(columnId);
    if (!column) return { top5: [], next20: [], hasMore: false };

    const facets = column.getFacetedUniqueValues();
    const facetsArr = Array.from(facets, ([name, value]) => ({ name, value }));

    const sortedFacets = facetsArr.sort((a, b) => {
      return b.value - a.value;
    });

    const top5 = sortedFacets.slice(0, 5);
    const next20 = sortedFacets.slice(5, 25);
    const hasMore = sortedFacets.length > 25;

    return { top5, next20, hasMore };
  }

  let facetVals = getTopFiveFacets(column.id);

  let checkedCols = new Set();

  function handleCheck(e) {
    const target = e.target;
    const checked = target.checked;
    const name = target.name;

    if (checked) {
      checkedCols.add(name);
    } else {
      checkedCols.delete(name);
    }

    console.log("ch", checkedCols);

    column.setFilterValue(Array.from(checkedCols));
  }
</script>

<div>
  {#each facetVals.top5 as top5}
    <div>
      <label class="checkbox">
        <input type="checkbox" on:change={handleCheck} name={top5.name} />
        {top5.name} ({top5.value})
      </label>
    </div>
  {/each}
  {#if facetVals.next20.length > 0}
    <div>
      <details>
        <summary>More</summary>
        <div>
          {#each facetVals.next20 as next20}
            <div>
              <label class="checkbox">
                <input
                  type="checkbox"
                  on:change={handleCheck}
                  name={next20.name}
                />
                {next20.name} ({next20.value})
              </label>
            </div>
          {/each}
          {#if facetVals.hasMore}
            <span>More values not displayed...</span>
          {/if}
        </div>
      </details>
    </div>
  {/if}
</div>
