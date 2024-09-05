package main

import (
	"fmt"
	"time"
)

const (
	width  = 10 // Width of the grid
	height = 10 // Height of the grid
)

type Grid [][]bool

func NewGrid() Grid {
	grid := make(Grid, height)
	for i := range grid {
		grid[i] = make([]bool, width)
	}
	return grid
}

func (g Grid) Print() {
	for _, row := range g {
		for _, cell := range row {
			if cell {
				fmt.Print("O")
			} else {
				fmt.Print(".")
			}
		}
		fmt.Println()
	}
}

func (g Grid) Next() Grid {
	newGrid := NewGrid()
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			liveNeighbors := g.countLiveNeighbors(x, y)
			if g[y][x] {
				// A live cell survives with 2 or 3 neighbors
				newGrid[y][x] = liveNeighbors == 2 || liveNeighbors == 3
			} else {
				// A dead cell becomes live with exactly 3 neighbors
				newGrid[y][x] = liveNeighbors == 3
			}
		}
	}
	return newGrid
}

func (g Grid) countLiveNeighbors(x, y int) int {
	count := 0
	for dy := -1; dy <= 1; dy++ {
		for dx := -1; dx <= 1; dx++ {
			if dx == 0 && dy == 0 {
				continue // Skip the cell itself
			}
			nx, ny := x+dx, y+dy
			if nx >= 0 && nx < width && ny >= 0 && ny < height {
				if g[ny][nx] {
					count++
				}
			}
		}
	}
	return count
}

func main() {
	grid := NewGrid()

	// Example initial configuration (can be customized)
	grid[1][2] = true
	grid[2][3] = true
	grid[3][1] = true
	grid[3][2] = true
	grid[3][3] = true

	fmt.Println("Initial Grid:")
	grid.Print()

	var x, y int
	fmt.Println("Enter coordinates to toggle (negative numbers to end):")
	for {
		fmt.Print("x y: ")
		fmt.Scanf("%d %d", &x, &y)
		if x < 0 || y < 0 {
			break
		}
		if x < width && y < height {
			grid[y][x] = !grid[y][x]
		}
		fmt.Println("Updated Grid:")
		grid.Print()
	}

	for {
		time.Sleep(1 * time.Second)
		fmt.Println("Next Generation:")
		grid = grid.Next()
		grid.Print()
	}
}
