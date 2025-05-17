from fastapi import APIRouter, Form, File, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image
from tools.v1.qr_generator import generate_qrcode, add_logo_with_background


router = APIRouter(prefix='/v1/qr', tags=["QR Generator"])


@router.post("/create_qr")
def create_qr(data=Form(...),
              version: int = Form(3),
              box_size: int = Form(100),
              fill_color: str = Form("black"),
              background_color: str = Form("white")
              ):
    kws = dict(version=version, box_size=box_size)

    qrimage = generate_qrcode(data, code_kws=kws, fill_color=fill_color, back_color=background_color)

    buffer = BytesIO()
    qrimage.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")


@router.post("/create_qr_with_logo")
async def create_qr_with_logo(
        data: str = Form(...),
        version: int = Form(3),
        box_size: int = Form(100),
        padding: float = Form(1),
        logo_size: float = Form(0.3),
        fill_color: str = Form("black"),
        background_color: str = Form("white"),
        logo: UploadFile = File(...)
):
    qrimage = generate_qrcode(
        data,
        code_kws=dict(version=version, box_size=box_size),
        fill_color=fill_color,
        back_color=background_color,
    )

    logo_image = Image.open(logo.file).convert("RGBA")

    qrimage_with_logo = add_logo_with_background(
        qrimage,
        logo_image,
        back_color=background_color,
        logo_size=logo_size,
        padding=padding
    )

    buffer = BytesIO()
    qrimage_with_logo.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")
