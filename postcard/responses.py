from fastapi.responses import Response


class SVGResponse(Response):
    media_type = "image/svg+xml"
