from COM.com_client import Client
from utils import logger as log

COM_CLIENT = Client()
ppt_instance = COM_CLIENT.get_app()

class Grid:
    
    def __init__(self, slide_index):
        self.slide_index = slide_index
        self.__app = ppt_instance
        self.slide = self.__app.ActivePresentation.Slides(self.slide_index)
        self.limits = self.__collect_limits()
        self.min_x = self.limits["limit3"].Left
        self.max_x = self.limits["limit1"].Left
        self.min_y = self.limits["limit0"].Top
        self.max_y = self.limits["limit2"].Top
        self.cols = int(self.max_x - self.min_x)
        self.rows = int(self.max_y - self.min_y)
        self.matrix = self.define_matrix(self.cols, self.rows)

    # Collect the limits
    def __collect_limits(self):
        try:
            limits = {}
            for shape in self.slide.Shapes:
                if shape.Name.lower().startswith("limit"):
                    limits[shape.Name.lower()] = shape

            # Ensure all 4 limits are present
            if not all(f"limit{i}" in limits for i in range(4)):
                raise Exception("Missing one or more limits (limit0 to limit3)")
            
            return limits
        except Exception as error:
            log.error(f"Failed collecting matrix limits", error)

    def define_matrix(self, cols, rows):
        try:
            return [[0 for _ in range(cols)] for _ in range(rows)]
        except Exception as error:
            log.error(f"Failed to define the matrix", error)
    
    # Function to convert PowerPoint coords to matrix coords
    def to_matrix_coords(self,x,y):
        try:
            col = int(((x - self.min_x) / (self.max_x - self.min_x)) * (self.cols - 1))
            row = int(((y - self.min_y) / (self.max_y - self.min_y)) * (self.rows - 1))
            return row, col
        except Exception as error:
            log.error(f"Failed during to_matrix_coords()", error)
    
    # Function to draw line in matrix
    def __draw_line(self, row1, col1, row2, col2, shape_name):
        try:
            steps = max(abs(row2 - row1), abs(col2 - col1))
            for i in range(steps + 1):
                r = int(row1 + (row2 - row1) * i / steps)
                c = int(col1 + (col2 - col1) * i / steps)
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    self.matrix[r][c] = str(shape_name)
        except Exception as error:
            log.error(f"Failed to draw line in the matrix", error)

    def update_matrix(self):
        try:
            for shape in self.slide.Shapes:
                if shape.Type == 9:  # msoLine shape type
                    x1, y1 = shape.Left, shape.Top
                    x2, y2 = shape.Left + shape.Width, shape.Top + shape.Height

                    row1, col1 = self.to_matrix_coords(x1, y1)
                    row2, col2 = self.to_matrix_coords(x2, y2)

                    self.__draw_line(row1, col1, row2, col2, shape.Name)

                if shape.Type == 1: # msoRectangle shape type
                    x1, y1 = shape.Left, shape.Top
                    x2, y2 = x1 + shape.Width, y1 + shape.Height

                    row1, col1 = self.to_matrix_coords(x1, y1)
                    row2, col2 = self.to_matrix_coords(x2, y2)

                    # Draw top edge
                    self.__draw_line(row1, col1, row1, col2, shape.Name)
                    # Draw bottom edge
                    self.__draw_line(row2, col1, row2, col2, shape.Name)
                    # Draw left edge
                    self.__draw_line(row1, col1, row2, col1, shape.Name)
                    # Draw right edge
                    self.__draw_line(row1, col2, row2, col2, shape.Name)
        except Exception as error:
            log.error(f"Failed to update matrix", error)

    def log_matrix(self):
        try:
            for row in self.matrix:
                print("".join(str(cell) for cell in row))
        except Exception as error:
            log.error(f"Failed to log matrix", error)