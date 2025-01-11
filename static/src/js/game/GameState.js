import { shuffle } from '../utils/array-utils.js';

/**
 * Manages the game's state and business logic
 */
export class GameState {
    width = 800;
    height = 600;
    xMargin = 10;
    yMargin = 10;

    /** @type {number} */
    playerIndex = 0;

    /** @type {number} */
    questionIndex = 0;

    /** @type {boolean} */
    gameOver = false;

    /** @type {boolean} */
    isFinalScreenDisplayed = false;

    /** @type {boolean} */
    isTimerElapsed = false;

    /** @type {Object} */
    config = null;

    /** @type {Object} */
    team = null;

    /** @type {number} */
    timerSeconds = 0;

    /** @type {Phaser.GameObjects.Text} */
    timerText = null;

    /**
     * Sets the game configuration
     * @param {Object} config Game configuration object
     */
    setConfig(config) {
        this.config = config;
    }

    /**
     * Sets the team and initializes team-related state
     * @param {Object} team Team configuration object
     */
    setTeam(team) {
        this.team = team;
        this.duration = team.duration;
        this.questions = team.questions;
        this.timerSeconds = team.duration * 60;
        this.players = shuffle(team.players);
    }

    /**
     * @returns {string} Current player name
     */
    getCurrentPlayer() {
        return this.players[this.playerIndex];
    }

    /**
     * @returns {string} Current question
     */
    getCurrentQuestion() {
        return this.questions[this.questionIndex];
    }

    /**
     * Advances the game state to the next step
     */
    step() {
        if (this.questionIndex < this.questions.length - 1) {
            this.questionIndex++;
            if (this.playerIndex === this.players.length - 1 &&
                this.questionIndex === this.questions.length - 1) {
                this.gameOver = true;
            }
        } else {
            if (this.playerIndex < this.players.length - 1) {
                this.questionIndex = 0;
                this.playerIndex++;
            }
        }
    }

    /**
     * Updates the timer
     */
    tick() {
        if (this.timerSeconds > 0) {
            this.timerSeconds--;
            const minutes = Math.floor(this.timerSeconds / 60);
            const seconds = this.timerSeconds % 60;
            this.timerText.setText(
                `${this.padWithZero(minutes)}:${this.padWithZero(seconds)}`
            );
        } else if (!this.isTimerElapsed) {
            this.isTimerElapsed = true;
            this.timerText.setColor('#ff0000');
        }
    }

    /**
     * Pads a number with leading zero if needed
     * @param {number} n Number to pad
     * @returns {string} Padded number
     */
    padWithZero(n) {
        return n < 10 ? `0${n}` : n.toString();
    }
}