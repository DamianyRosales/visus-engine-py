from COM.com_client import Client
from utils import logger as log
from .slides import Slides
import math

COM_CLIENT = Client()
ppt_instance = COM_CLIENT.get_app()

class Game:
    
    def __init__(self):
        self.loop = True
    
    Slides = Slides(ppt_instance)
    
    class Render:
        
        @staticmethod
        def raycast(matrix, player_x, player_y, angle, max_distance=100):
            """
            Cast a single ray from (player_x, player_y) in the given angle.
            Returns (hit_x, hit_y, distance) where the ray hits a wall.
            """
            ray_x = player_x
            ray_y = player_y

            step_size = 0.1  # Step resolution (the smaller, the smoother)
            dx = math.cos(angle) * step_size
            dy = math.sin(angle) * step_size

            distance = 0

            while distance < max_distance:
                ray_x += dx
                ray_y += dy
                distance += step_size

                col = int(ray_x)
                row = int(ray_y)

                if 0 <= row < len(matrix) and 0 <= col < len(matrix[0]):
                    cell = matrix[row][col]
                    if cell != 0 and cell != "p":
                        return (ray_x, ray_y, distance, matrix[row][col])
                else:
                    break  # Out of bounds

            return None  # No wall hit

        @staticmethod
        def cast_all_rays(matrix, player_x, player_y, direction, fov=math.pi/3, num_rays=60):
            """Casts multiple rays in a FOV and returns the hit distances"""
            half_fov = fov / 2
            """
                direction angles:
                    Right: 0 degrees
                    Down: 90 degrees
                    Left: 180 degrees
                    Up: 270 degrees
            """
            start_angle = direction - half_fov

            hits = []
            for i in range(num_rays):
                angle = start_angle + (i / num_rays) * fov
                hit = Game.Render.raycast(matrix, player_x, player_y, angle)
                if hit[3] not in hits: hits.append(hit[3])
            
            return hits
        
        def cast_rays(matrix, player_x, player_y, player_angle_deg, fov_deg, num_rays):
            hits = []
            half_fov = fov_deg / 2
            angle_step = fov_deg / num_rays

            for i in range(num_rays):
                ray_angle = math.radians(player_angle_deg - half_fov + i * angle_step)
                dx = math.cos(ray_angle)
                dy = math.sin(ray_angle)

                x, y = player_x, player_y

                for step in range(100):  # max steps for ray
                    x += dx * 0.1
                    y += dy * 0.1

                    row = int(y)
                    col = int(x)

                    # Bounds check
                    if 0 <= row < len(matrix) and 0 <= col < len(matrix[0]):
                        cell = matrix[row][col]
                        if cell != 0:  # Could be a string like "wall0"
                            hits.append({
                                "ray": i,
                                "row": row,
                                "col": col,
                                "hit_name": cell,
                                "distance": math.sqrt((x - player_x)**2 + (y - player_y)**2)
                            })
                            break
                    else:
                        break  # Out of bounds

            return hits
