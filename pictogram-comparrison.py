import sys
import math
sys.path.append( "." ) 
from indpendent_work.colors import color
from PIL import Image
import pygame
import pandas as pd

pygame.init()

grid_width = 50
grid_height = 50

screen_width = 1000
screen_height = 1000

display = pygame.display.set_mode(( screen_width, screen_height ))
running = True

# importing data
xls = pd.ExcelFile(
    "indpendent_work/pictogram/data/archive/HighestGrossers.xlsx"
)
data = pd.read_excel( xls, "HighestGrossers")

movie_data = []

for i in range(0, len(data["MOVIE"])):    
    movie = data["MOVIE"].iloc[i]
    revenue = data["TOTAL IN 2019 DOLLARS"].iloc[i]
    icon = pygame.image.load( "./indpendent_work/pictogram/images/icons/$" + "{:,}".format(data["TOTAL FOR YEAR"].iloc[i]) + " .png")
    movie_data.append((movie, revenue, icon))

series = len(movie_data)

# determining scales

total_revenue = 0
for movie in movie_data:
    total_revenue += movie[1]

value_per_cell = total_revenue / (grid_width * grid_height)
print( "value per image = ", value_per_cell)

for index in range(0, len(movie_data)):
    movie = movie_data[index]
    cell_count = movie[1] / value_per_cell
    movie_data[index] = (movie[0], movie[1], movie[2], int(cell_count) - 1)

# image stuff
constructed_image = Image.open( "./indpendent_work/pictogram/images/base.png" )
constructed_image = constructed_image.resize( ( grid_width, grid_height ), Image.BILINEAR )
pixel_values = []


# rendering new image

for x in range(0, grid_width):
    for y in range(0, grid_height):
        color_tup = constructed_image.getpixel(( x, y )) 
        color_obj = color( color_tup[0], color_tup[1], color_tup[2] )
        pixel_values.append( (( x, y), color_tup ) )

def clamp_value(value):
    return math.floor(value / (100 / series)) * (100 / series) 

current_movie = 0
current_box_number = 0

for pixel in pixel_values:
    p_width = screen_width / (grid_width)
    p_height = screen_height / grid_height

    x = pixel[0][0] * p_width
    y = pixel[0][1] * p_height

    rect = pygame.Surface( (int(p_width), int(p_height))  )
    rect.set_alpha(160)
    rect.fill(pixel[1])

    temp = pygame.transform.scale( movie_data[min(current_movie, len(movie_data)-1)][2], ( p_width, p_height ) )
    temp.blit( rect, (0, 0) )
    display.blit( temp, (x, y - p_height) )
    
    current_box_number += 1
    if current_box_number > movie_data[ min(current_movie, len(movie_data)-1) ][3]:
        current_movie += 1
        current_box_number = 0
    


# pygame stuff

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()





