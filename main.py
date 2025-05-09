import win32com.client

app = win32com.client.Dispatch("PowerPoint.Application")
app.Visible = True

presentation = app.ActivePresentation
slide = presentation.Slides(2)

# Collect the limits
limits = {}
for shape in slide.Shapes:
    if shape.Name.lower().startswith("limit"):
        limits[shape.Name.lower()] = shape

# Ensure all 4 limits are present
if not all(f"limit{i}" in limits for i in range(4)):
    raise Exception("Missing one or more limits (limit0 to limit3)")

# Define the bounding box using limits
limit0 = limits["limit0"]  # Top
limit1 = limits["limit1"]  # Right
limit2 = limits["limit2"]  # Bottom
limit3 = limits["limit3"]  # Left

min_x = limit3.Left
max_x = limit1.Left
min_y = limit0.Top
max_y = limit2.Top

# Validate bounding box
if max_x - min_x == 0 or max_y - min_y == 0:
    raise ValueError("Invalid bounding box: zero width or height")

# Define matrix size
cols = int(max_x - min_x)
rows = int(max_y - min_y)
matrix = [[0 for _ in range(cols)] for _ in range(rows)]

# Function to convert PowerPoint coords to matrix coords
def to_matrix_coords(x, y):
    col = int(((x - min_x) / (max_x - min_x)) * (cols - 1))
    row = int(((y - min_y) / (max_y - min_y)) * (rows - 1))
    return row, col

# Function to draw line in matrix
def draw_line(matrix, row1, col1, row2, col2):
    steps = max(abs(row2 - row1), abs(col2 - col1))
    for i in range(steps + 1):
        r = int(row1 + (row2 - row1) * i / steps)
        c = int(col1 + (col2 - col1) * i / steps)
        if 0 <= r < rows and 0 <= c < cols:
            matrix[r][c] = 1

for shape in slide.Shapes:
    if shape.Type == 9:  # msoLine shape type
        x1, y1 = shape.Left, shape.Top
        x2, y2 = shape.Left + shape.Width, shape.Top + shape.Height

        row1, col1 = to_matrix_coords(x1, y1)
        row2, col2 = to_matrix_coords(x2, y2)

        draw_line(matrix, row1, col1, row2, col2)

    if shape.Type == 1: # msoRectangle shape type
        x1, y1 = shape.Left, shape.Top
        x2, y2 = x1 + shape.Width, y1 + shape.Height

        row1, col1 = to_matrix_coords(x1, y1)
        row2, col2 = to_matrix_coords(x2, y2)

        # Draw top edge
        draw_line(matrix, row1, col1, row1, col2)
        # Draw bottom edge
        draw_line(matrix, row2, col1, row2, col2)
        # Draw left edge
        draw_line(matrix, row1, col1, row2, col1)
        # Draw right edge
        draw_line(matrix, row1, col2, row2, col2)


for row in matrix:
    print("".join(str(cell) for cell in row))