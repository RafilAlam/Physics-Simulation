import pygame
import pymunk
import pymunk.pygame_util
import math

import utils
import objects

pygame.init()

WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
worldObjs = []

def draw(window, space, draw_options, line, worldObjs):
    window.fill((20, 20, 20, 1))

    if line:
        pygame.draw.line(window, "black", line[0], line[1], 3)
    for instance in worldObjs:
        instance.draw()

    # space.debug_draw(draw_options)
    pygame.display.update()

def create_boundaries(space, width, height):
    rects = [
        [(width/2, height - 10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width - 10, height/2), (20, height)],
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)

def create_structure(space, width, height):
    BROWN = (139, 69, 19, 100)
    rects = [
        [(600, height - 120), (40, 200), BROWN, 100],
        [(900, height - 120), (40, 200), BROWN, 100],
        [(750, height - 240), (340, 40), BROWN, 150]
    ]

    for pos, size, color, mass in  rects:
        rectangle = objects.Rectangle(window, color, size, mass, elasticity=0.4, friction=0.4, pos=pos)
        space.add(rectangle.body, rectangle.shape)
        rectangle.body.body_type = pymunk.Body.DYNAMIC
        worldObjs.append(rectangle)

def create_pendulum(space):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (300, 300)

    body = pymunk.Body()
    body.position = (300, 300)
    line = pymunk.Segment(body, (0, 0), (255, 0), 5)
    circle = pymunk.Circle(body, 40, (255, 0))
    line.friction = 1
    circle.friction = 1
    line.mass = 8
    circle.mass = 30
    circle.elasticity = 0.95
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0))

    space.add(circle, line, body, rotation_center_joint)

def create_ball(space, radius, mass, pos):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0.9
    shape.friction = 0.4
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return shape

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 981)

    create_boundaries(space, width, height)
    create_structure(space, width, height)

    line = objects.Line(window, (0, 0, 255), (100, 100), (500, 500), 5, 0.1, 0.5, 0.5, pymunk.Body())
    space.add(line.body, line.shape)
    worldObjs.append(line)

    create_pendulum(space)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    pressed_pos = None
    ball = None

    while run:
        line = None
        if ball and pressed_pos:
            line = [pressed_pos, pygame.mouse.get_pos()]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball:
                    pressed_pos = pygame.mouse.get_pos()
                    ball = objects.Circle(window, (255, 0, 0, 100), 30, 10, 1, 0.4, pressed_pos)
                    space.add(ball.body, ball.shape)
                    worldObjs.append(ball)
                    ball.draw()
                elif pressed_pos:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    angle = utils.calculate_angle(*line)
                    force = utils.calculate_dist(*line) * 50
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    ball.body.apply_impulse_at_local_point((fx, fy), (0, 0))
                    pressed_pos = None
                else:
                    space.remove(ball.shape, ball.body)
                    worldObjs.remove(ball)
                    ball = None


        draw(window, space, draw_options, line, worldObjs)
        print(worldObjs)

        space.step(dt)
        clock.tick(fps)
    
    pygame.quit()

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)