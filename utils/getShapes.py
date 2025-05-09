import win32com.client

app = win32com.client.Dispatch("PowerPoint.Application")
app.Visible = True

presentation = app.ActivePresentation
slide = presentation.Slides(2)

for shape in slide.Shapes:
    properties = {
        "Id": shape.Id,
        "Name": shape.Name,
        "Type": shape.Type,
        "Width": shape.Width,
        "Height": shape.Height,
        "Left": shape.Left,
        "Top": shape.Top,
    }
    print(properties)