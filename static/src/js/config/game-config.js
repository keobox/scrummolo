import { GameState } from '../game/GameState.js';
import { GameScene } from '../game/GameScene.js';

/**
 * Creates Phaser game configuration
 * @param {GameState} gameState Game state instance
 * @returns {Phaser.Types.Core.GameConfig} Phaser game configuration
 */
export function createGameConfig(gameState) {
    return {
        type: Phaser.AUTO,
        width: gameState.width,
        height: gameState.height,
        scene: [new GameScene(gameState)]
    };
}