from qrcode import QRCode, constants
from typing import Any
from PIL import Image, ImageDraw


def generate_qrcode(data: str, code_kws: dict[str, Any] = None, fill_color='black', back_color='white') -> Image:
    code_kws = code_kws or dict()
    base_code_kws = dict(
        version=3,
        box_size=100,
        error_correction=constants.ERROR_CORRECT_H,
        border=1
    )

    qr = QRCode(**(base_code_kws | code_kws))
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color=fill_color, back_color=back_color)


def add_logo_with_background(qr_img: Image.Image, logo: Image, back_color='black',
                             logo_size: float = 0.40,
                             padding: float = 1,
                             ) -> Image.Image:
    # convert logo to Black and White
    logo = logo.convert("RGBA")

    # Resize logo to fit QR code
    qr_width, qr_height = qr_img.size
    logo_size = int(qr_width * logo_size)
    logo = logo.resize((logo_size, logo_size))

    # Add background behind logo with rounded corners

    bg = Image.new("RGBA", logo.size, back_color)
    bg = rounded_corners(bg, radius=logo_size / 10)
    logo_with_bg = Image.alpha_composite(bg, logo)

    # Compute position for centering the logo
    pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

    # Paste the logo with white background onto the QR
    qr_img = qr_img.convert("RGBA")
    qr_img.paste(logo_with_bg, pos, logo_with_bg)  # use mask for transparency handling

    return qr_img


def rounded_corners(image: Image, radius: float) -> Image:
    # Create a mask for rounded corners
    mask = Image.new('L', image.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, image.size[0], image.size[1]], radius=radius, fill=255)

    # Apply the mask to the image
    image.putalpha(mask)
    return image