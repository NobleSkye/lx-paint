package main

import (
	"image/color"
	"log"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

const (
	screenWidth  = 300
	screenHeight = 300
)

var (
	board         [3][3]string
	currentPlayer = "X"
	gameOver      = false
)

type Game struct{}

func (g *Game) Update() error {
	if gameOver {
		return nil
	}

	if ebiten.IsMouseButtonPressed(ebiten.MouseButtonLeft) {
		x, y := ebiten.CursorPosition()
		row, col := y/100, x/100

		if row >= 0 && row < 3 && col >= 0 && col < 3 && board[row][col] == "" {
			board[row][col] = currentPlayer
			if checkWin(currentPlayer) {
				gameOver = true
			} else if isDraw() {
				gameOver = true
				currentPlayer = "Draw"
			} else {
				switchPlayer()
			}
		}
	}

	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	screen.Fill(color.White)

	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			x, y := float64(j*100), float64(i*100)
			if board[i][j] == "X" {
				ebitenutil.DebugPrintAt(screen, "X", int(x)+40, int(y)+30)
			} else if board[i][j] == "O" {
				ebitenutil.DebugPrintAt(screen, "O", int(x)+40, int(y)+30)
			}
			ebitenutil.DrawLine(screen, x, y, x+100, y, color.Black)
			ebitenutil.DrawLine(screen, x, y, x, y+100, color.Black)
		}
	}

	ebitenutil.DrawLine(screen, 0, 300, 300, 300, color.Black)
	ebitenutil.DrawLine(screen, 300, 0, 300, 300, color.Black)

	if gameOver {
		if currentPlayer == "Draw" {
			ebitenutil.DebugPrintAt(screen, "It's a draw!", 100, 130)
		} else {
			ebitenutil.DebugPrintAt(screen, currentPlayer+" wins!", 100, 130)
		}
	}
}

func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return screenWidth, screenHeight
}

func switchPlayer() {
	if currentPlayer == "X" {
		currentPlayer = "O"
	} else {
		currentPlayer = "X"
	}
}

func checkWin(player string) bool {
	for i := 0; i < 3; i++ {
		if board[i][0] == player && board[i][1] == player && board[i][2] == player {
			return true
		}
		if board[0][i] == player && board[1][i] == player && board[2][i] == player {
			return true
		}
	}
	if board[0][0] == player && board[1][1] == player && board[2][2] == player {
		return true
	}
	if board[0][2] == player && board[1][1] == player && board[2][0] == player {
		return true
	}
	return false
}

func isDraw() bool {
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			if board[i][j] == "" {
				return false
			}
		}
	}
	return true
}

func main() {
	ebiten.SetWindowSize(screenWidth, screenHeight)
	ebiten.SetWindowTitle("Tic Tac Toe")

	game := &Game{}
	if err := ebiten.RunGame(game); err != nil {
		log.Fatal(err)
	}
}
