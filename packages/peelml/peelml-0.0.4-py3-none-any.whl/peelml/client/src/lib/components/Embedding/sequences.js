export function makeSequences(
  points,
  metadata,
  nSequencesPerLabel = 3,
  sequenceLength = 5
) {
  const pointIndicesByLabel = new Map();
  points.forEach((point, index) => {
    const label = metadata[index].label;
    const pointIndices = pointIndicesByLabel.get(label) || [];
    pointIndices.push(index);
    pointIndicesByLabel.set(label, pointIndices);
  });

  const sequences = [];

  pointIndicesByLabel.forEach((indices) => {
    for (let i = 0; i < nSequencesPerLabel; i++) {
      const sequence = { indices: [] };
      for (let j = 0; j < sequenceLength; j++) {
        const index = indices[i * sequenceLength + j];
        sequence.indices.push(index);
      }
      sequence.indices.push(sequence.indices[0]);
      sequences.push(sequence);
    }
  });

  return sequences;
}
