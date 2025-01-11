/**
 * Calculates new dimensions maintaining aspect ratio
 * @param {number} width Original width
 * @param {number} height Original height
 * @param {number} maxWidth Maximum allowed width
 * @param {number} maxHeight Maximum allowed height
 * @returns {[number, number]} New [width, height]
 */
export function calculateDimensions(width, height, maxWidth, maxHeight) {
    const deltaWidth = width - maxWidth;
    const deltaHeight = height - maxHeight;

    if (deltaHeight <= 0 && deltaWidth <= 0) {
        return [width, height];
    }

    if (deltaHeight >= deltaWidth) {
        return [width * maxHeight / height, maxHeight];
    }

    return [maxWidth, height * maxWidth / width];
}

/**
 * Resizes a Phaser image maintaining aspect ratio
 * @param {Phaser.GameObjects.Image} image Phaser image object
 * @param {number} maxWidth Maximum allowed width
 * @param {number} maxHeight Maximum allowed height
 */
export function resizeImage(image, maxWidth, maxHeight) {
    const [newWidth, newHeight] = calculateDimensions(
        image.width,
        image.height,
        maxWidth,
        maxHeight
    );

    image.displayWidth = newWidth;
    image.displayHeight = newHeight;
}