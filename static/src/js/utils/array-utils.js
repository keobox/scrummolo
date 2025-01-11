/**
 * Shuffles an array using Fisher-Yates algorithm
 * @template T
 * @param {T[]} array Array to shuffle
 * @returns {T[]} Shuffled array
 */
export function shuffle(array) {
    const arrayCopy = [...array];
    for (let m = arrayCopy.length; m;) {
        const i = Math.floor(Math.random() * m--);
        [arrayCopy[m], arrayCopy[i]] = [arrayCopy[i], arrayCopy[m]];
    }
    return arrayCopy;
}