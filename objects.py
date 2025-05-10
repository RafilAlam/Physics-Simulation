import pygame
import pymunk

class Rectangle():
    def __init__(self, display, color, size, mass, elasticity, friction, pos):
        self.display = display
        self.size = size
        self.color = color
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = pos
        self.shape = pymunk.Poly.create_box(self.body, self.size)
        self.shape.mass = mass
        self.shape.elasticity = elasticity
        self.shape.friction = friction
    def draw(self):
        vertices = self.shape.get_vertices()
        points = [(v.rotated(self.body.angle) + self.body.position) for v in vertices]
        points = [(int(point.x), int(point.y)) for point in points]
        pygame.draw.polygon(self.display, self.color, points)

class Circle():
    def __init__(self, display, color, radius, mass, elasticity, friction, pos):
        self.display = display
        self.color = color
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.mass = mass
        self.shape.elasticity = elasticity
        self.shape.friction = friction
    def draw(self):
        pygame.draw.circle(self.display, self.color, (int(self.body.position.x), int(self.body.position.y)), int(self.shape.radius))

class Line():
    def __init__(self, display, color, start_pos, end_pos, thickness, mass, elasticity, friction, body=None):
        self.display = display
        self.color = color
        self.thickness = thickness

        # Calculate the length and center position of the line
        length = pymunk.Vec2d(end_pos[0], end_pos[1]).get_distance(start_pos)
        center_pos = ((start_pos[0] + end_pos[0]) / 2, (start_pos[1] + end_pos[1]) / 2)

        # Use external body if provided, otherwise create a new one
        body.mass   = mass
        body.moment = pymunk.moment_for_segment(mass, (0, 0), (length, 0), thickness)
        self.body = body if body else pymunk.Body(mass, pymunk.moment_for_segment(mass, (0, 0), (length, 0), thickness))
        self.body.position = center_pos

        self.shape = pymunk.Segment(self.body, (-length / 2, 0), (length / 2, 0), thickness)
        self.shape.elasticity = elasticity
        self.shape.friction = friction

    def draw(self):
        start_pos = self.body.local_to_world(self.shape.a)
        end_pos = self.body.local_to_world(self.shape.b)
        print(start_pos)
        start_pos = (int(start_pos[0]), int(start_pos[1]))
        end_pos = (int(end_pos[0]), int(end_pos[1]))
        pygame.draw.line(self.display, self.color, start_pos, end_pos, int(self.thickness))