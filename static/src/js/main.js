import { GameState } from './game/GameState.js';
import { createGameConfig } from './config/game-config.js';

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/js/config.json');
        const data = await response.json();

        const gameState = new GameState();
        gameState.setConfig(data.config);
        gameState.setTeam(data.teams[0]);
        
        document.getElementById('loading').style.display = 'none';

        new Phaser.Game(createGameConfig(gameState));
    } catch (error) {
        console.error('Failed to initialize game:', error);
    }
});