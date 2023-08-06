export class Dataset {
  constructor(points, metadata = []) {
    this.points = points;
    this.metadata = metadata;
    const dimensions = points[0].length;
    if (!(dimensions === 2 || dimensions === 3)) {
      throw new Error("DIMENSIONALITY_ERROR_MESSAGE");
    }
    for (const point of points) {
      if (dimensions !== point.length) {
        throw new Error("DIMENSIONALITY_ERROR_MESSAGE");
      }
    }
    this.dimensions = dimensions;
  }

  setSpriteMetadata(spriteMetadata) {
    this.spriteMetadata = spriteMetadata;
  }
}
