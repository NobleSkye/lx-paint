package main

import (
	"fmt"
	"image/color"
	"log"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

const (
	screenWidth  = 640
	screenHeight = 480
	paddleWidth  = 10
	paddleHeight = 80
	ballSize     = 10
)

type Game struct {
	player1Y     float64
	player2Y     float64
	ballX        float64
	ballY        float64
	ballVX       float64
	ballVY       float64
	player1Score int
	player2Score int
	ballInPlay   bool
}

func (g *Game) Update() error {
	// Player 1 controls
	if ebiten.IsKeyPressed(ebiten.KeyW) && g.player1Y > 0 {
		g.player1Y -= 4
		if !g.ballInPlay {
			g.ballInPlay = true
			g.ballVX = 4
			g.ballVY = 4
		}
	}
	if ebiten.IsKeyPressed(ebiten.KeyS) && g.player1Y < screenHeight-paddleHeight {
		g.player1Y += 4
		if !g.ballInPlay {
			g.ballInPlay = true
			g.ballVX = 4
			g.ballVY = 4
		}
	}

	// Player 2 controls
	if ebiten.IsKeyPressed(ebiten.KeyUp) && g.player2Y > 0 {
		g.player2Y -= 4
		if !g.ballInPlay {
			g.ballInPlay = true
			g.ballVX = 4
			g.ballVY = 4
		}
	}
	if ebiten.IsKeyPressed(ebiten.KeyDown) && g.player2Y < screenHeight-paddleHeight {
		g.player2Y += 4
		if !g.ballInPlay {
			g.ballInPlay = true
			g.ballVX = 4
			g.ballVY = 4
		}
	}

	// Ball movement
	if g.ballInPlay {
		g.ballX += g.ballVX
		g.ballY += g.ballVY
	}

	// Ball collision with top and bottom
	if g.ballY <= 0 || g.ballY >= screenHeight-ballSize {
		g.ballVY *= -1
	}

	// Ball collision with paddles
	if (g.ballX <= paddleWidth && g.ballY >= g.player1Y && g.ballY <= g.player1Y+paddleHeight) ||
		(g.ballX >= screenWidth-paddleWidth-ballSize && g.ballY >= g.player2Y && g.ballY <= g.player2Y+paddleHeight) {
		g.ballVX *= -1
	}

	// Ball out of bounds
	if g.ballX < 0 {
		g.player2Score++
		g.resetBall()
	}
	if g.ballX > screenWidth {
		g.player1Score++
		g.resetBall()
	}

	return nil
}

func (g *Game) resetBall() {
	g.ballX = screenWidth / 2
	g.ballY = screenHeight / 2
	g.ballVX = 0
	g.ballVY = 0
	g.ballInPlay = false
}

func (g *Game) Draw(screen *ebiten.Image) {
	// Draw paddles
	ebitenutil.DrawRect(screen, 0, g.player1Y, paddleWidth, paddleHeight, color.White)
	ebitenutil.DrawRect(screen, screenWidth-paddleWidth, g.player2Y, paddleWidth, paddleHeight, color.White)

	// Draw ball
	ebitenutil.DrawRect(screen, g.ballX, g.ballY, ballSize, ballSize, color.White)

	// Draw scores
	scoreText := fmt.Sprintf("Player 1: %d  Player 2: %d", g.player1Score, g.player2Score)
	ebitenutil.DebugPrint(screen, scoreText)
}

func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return screenWidth, screenHeight
}

func main() {
	game := &Game{
		player1Y:   screenHeight/2 - paddleHeight/2,
		player2Y:   screenHeight/2 - paddleHeight/2,
		ballX:      screenWidth / 2,
		ballY:      screenHeight / 2,
		ballInPlay: false,
	}
	ebiten.SetWindowSize(screenWidth, screenHeight)
	ebiten.SetWindowTitle("Pong in Go with Score")
	if err := ebiten.RunGame(game); err != nil {
		log.Fatal(err)
	}
}
