package main

import (
	"image/color"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func main() {
	// Create a new application
	myApp := app.New()
	myWindow := myApp.NewWindow("Hello World Window")

	// Set the background color to blue using the color package
	background := canvas.NewRectangle(color.NRGBA{R: 0, G: 0, B: 255, A: 255}) // Blue color

	// Create a label with "Hello, World!"
	label := widget.NewLabel("Hello, World!")
	label.Alignment = fyne.TextAlignCenter // Center align the text

	// Create a container with the background and label
	content := container.NewMax(background, label)

	// Set the content of the window
	myWindow.SetContent(content)

	// Set window size
	myWindow.Resize(fyne.NewSize(300, 200))

	// Show and run the application
	myWindow.ShowAndRun()
}
