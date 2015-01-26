from app import app
import pygame

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()                      #initialize pygam

app.run(debug=True, host= '0.0.0.0')
