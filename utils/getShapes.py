from COM.com_client import Client

com_instance = Client()
powerpoint = com_instance.get_app()

presentation = powerpoint.ActivePresentation
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