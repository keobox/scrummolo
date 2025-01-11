import { GameState } from './GameState.js';
import { resizeImage } from '../utils/image-utils.js';

export class GameScene extends Phaser.Scene {
    /** @type {GameState} */
    #gameState;
    #lastPointerUp = false;

    /**
     * @param {GameState} gameState Game state instance
     */
    constructor(gameState) {
        super('gameScene');
        this.#gameState = gameState;
    }

    preload() {
        const { team, config } = this.#gameState;

        this.load.atlas(
            team.skin,
            `${config.assets}/${team.skin}/${team.skin}.png`,
            `${config.assets}/${team.skin}/${team.skin}.json`
        );

        this.load.image(
            'gameOverImage',
            `${config.assets}/${config.gameOverImage}`
        );

        this.load.audio(
            'gameOverSound',
            `${config.assets}/${config.gameOverSound}`
        );
    }

    create() {
        this.setupGame();
        this.setupInputs();
        this.setupTimer();
    }

    setupGame() {
        const gameState  = this.#gameState;
        gameState.frames = this.textures.get(gameState.team.skin).getFrameNames();

        const playerImage = this.createPlayerImage();
        const playerText = this.createPlayerText();
        const questionText = this.createQuestionText();

        gameState.playerImage = playerImage;
        gameState.playerText = playerText;
        gameState.questionsText = questionText;
        gameState.gameOverSound = this.sound.add('gameOverSound');
    }

    createPlayerImage() {
        const gameState = this.#gameState;
        const playerImage = this.add.image(
            gameState.width / 2 + gameState.xMargin,
            gameState.yMargin,
            gameState.team.skin,
            Phaser.Math.RND.pick(gameState.frames)
        ).setOrigin(0, 0);

        resizeImage(
            playerImage,
            gameState.width / 2,
            gameState.height / 2
        );

        return playerImage;
    }

    createPlayerText() {
        return this.add.text(
            100,
            100,
            `${this.#gameState.getCurrentPlayer()}, is your turn!`,
            { font: '21px Arial', fill: '#fff' }
        );
    }

    createQuestionText() {
        return this.add.text(
            100,
            500,
            this.#gameState.getCurrentQuestion(),
            { font: '40px Arial', fill: '#fff' }
        );
    }

    setupInputs() {
        // Setup keyboard input
        this.#gameState.spaceKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);

        // Setup pointer/touch input for the entire game area
        const advanceArea = this.add.rectangle(
            0,
            0,
            this.cameras.main.width,
            this.cameras.main.height,
            0x000000,
            0  // Fully transparent
        );
        advanceArea.setOrigin(0, 0);
        advanceArea.setInteractive();

        // Add pointer up event (works for both mouse click and touch)
        // using the Phaser3 event handler this is way is not handled in update
        advanceArea.on('pointerup', () => {
            this.handleAdvanceGame();
        });
    }

    setupTimer() {
        const gameState  = this.#gameState;
        gameState.timerText = this.add.text(
            100,
            300,
            `${gameState.duration}:00`,
            { font: '36px Arial', fill: '#fff' }
        );

        gameState.timer = this.time.addEvent({
            delay: 1000,
            callback: gameState.tick,
            callbackScope: gameState,
            loop: true
        });
    }

    update() {
        // Check for keyboard input
        if (Phaser.Input.Keyboard.JustDown(this.#gameState.spaceKey)) {
            this.handleAdvanceGame();
        }
    }

    handleAdvanceGame() {
        const gameState = this.#gameState;

        if (!gameState.gameOver) {
            this.handleGameStep();
        } else if (!gameState.isFinalScreenDisplayed) {
            this.showGameOver();
        }
    }

    handleGameStep() {
        const  gameState  = this.#gameState;
        gameState.step();
        gameState.questionsText.setText(gameState.getCurrentQuestion());

        if (gameState.questionIndex === 0) {
            this.updatePlayerTurn();
        }
    }

    updatePlayerTurn() {
        const  gameState  = this.#gameState;
        gameState.playerText.setText(
            `${gameState.getCurrentPlayer()}, is your turn!`
        );

        gameState.playerImage
            .setTexture(
                gameState.team.skin,
                Phaser.Math.RND.pick(gameState.frames)
            )
            .setOrigin(0, 0);

        resizeImage(
            gameState.playerImage,
            gameState.width / 2,
            gameState.height / 2
        );
    }

    showGameOver() {
        const  gameState  = this.#gameState;
        gameState.isFinalScreenDisplayed = true;

        // Cleanup existing elements
        gameState.playerText.destroy();
        gameState.questionsText.destroy();
        gameState.playerImage.destroy();
        gameState.timerText.destroy();
        gameState.timer.destroy();

        // Show game over screen
        this.add.text(
            100,
            500,
            gameState.config.gameOverText,
            { font: '40px Arial', fill: '#fff' }
        );

        const gameOverImage = this.add.image(
            gameState.width / 2,
            gameState.yMargin,
            'gameOverImage'
        ).setOrigin(0, 0);

        resizeImage(
            gameOverImage,
            gameState.width / 2,
            gameState.height / 2
        );

        gameState.gameOverSound.play();
    }
}