#!/usr/bin/env python3

import pygame
import random
import datetime


def take_screenshot(surface):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    pygame.image.save(surface, filename)
    print(f"Screenshot saved as {filename}")
    
    
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def initialize(outer_circle_radius, outer_circle_position):
    inner_circle_radius = outer_circle_radius * random.random()
    inner_circle_position = outer_circle_position + outer_circle_radius - inner_circle_radius
    pen_radius = inner_circle_radius * random.random()
    return inner_circle_position, pen_radius, inner_circle_radius, None


def main():
    pygame.init()

    window_dimensions = width, height = 1800, 900

    surface = pygame.display.set_mode(window_dimensions)
    pygame.display.set_caption("Spirograph")
    surface.fill("black")
    
    # outer circle
    outer_circle_radius = pygame.Vector2(min(width, height) // 2, 0) 
    outer_circle_position = pygame.Vector2(width // 2, height // 2)
    
    # inner circle
    inner_circle_position, pen_radius, inner_circle_radius, last_pen_position = initialize(outer_circle_radius, outer_circle_position)

    # Drawing Surface
    drawing_surface = pygame.surface.Surface(window_dimensions)
    drawing_surface.fill("black")
    
    pen_color = random_color()
    rotation_speed = .1
    
    running = True
    show_circles = True
    enable_drawing = False

    while running:
       
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q: running = False
                    case pygame.K_s: take_screenshot(surface)
                    case pygame.K_d: 
                        enable_drawing = not enable_drawing
                    case pygame.K_c:
                        pen_color = random_color()
                    case pygame.K_h:
                        show_circles = not show_circles
                    case pygame.K_PLUS:
                        rotation_speed += .1
                    case pygame.K_MINUS:
                        rotation_speed -= .1
                    case pygame.K_RETURN:
                        inner_circle_position, pen_radius, inner_circle_radius, last_pen_position = initialize(outer_circle_radius, outer_circle_position)
                    
        # Fill screen black
        surface.fill("black")
        
        # Merge surfaces
        surface.blit(drawing_surface, (0, 0))
        
        # inner circle
        inner_circle_position = outer_circle_position + (inner_circle_position - outer_circle_position).rotate(rotation_speed)

        # pen
        pen_radius = pen_radius.rotate(-rotation_speed * outer_circle_radius.length() / inner_circle_radius.length())
        pen_position = inner_circle_position + pen_radius
        
        # Draw outer circles
        if show_circles:
            pygame.draw.circle(surface, 'white', outer_circle_position, outer_circle_radius.length(), 3)
            pygame.draw.circle(surface, 'white', inner_circle_position, inner_circle_radius.length(), 3)
            pygame.draw.line(surface, 'white', inner_circle_position, pen_position, 1)
            pygame.draw.circle(surface, pen_color, pen_position, 5)
        
        # Draw with pen
        if last_pen_position and enable_drawing:
            pygame.draw.line(drawing_surface, pen_color, last_pen_position, pen_position, 1)
        
        last_pen_position = pen_position
        
        pygame.display.flip()


if __name__ == "__main__":
    main()
