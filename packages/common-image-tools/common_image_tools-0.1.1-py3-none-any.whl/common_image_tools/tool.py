import cv2
import numpy as np


def merge_color(image: np.ndarray, mask: np.ndarray, target_color_rgb: tuple) -> np.ndarray:
    """Merge the target color with the image using the mask using hsv color space.ù

    Example:
        >>> import cv2
        >>> import numpy as np
        >>> from common_image_tools import tool
        >>> img = cv2.imread("imgs/test.jpg")
        >>> # Create one channel mask with the same size of the image
        >>> mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
        >>> # Draw a rectangle on the mask
        >>> cv2.rectangle(mask, (100, 100), (500, 500), (255, 255, 255), -1)
        >>> img = tool.merge_color(img, mask, (0, 255, 0))
        >>> cv2.imshow("img", img)
        >>> cv2.waitKey(0)

    Args:
        image (np.ndarray): Image in opencv format (BGR)
        mask (np.ndarray): Mask in opencv format one channel
        target_color_rgb (tuple): Target color in RGB format

    Returns:
        np.ndarray: Image with merged color in opencv format (BGR)

    """
    hsv_image = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv_image)

    color_to_merge = np.uint8([[target_color_rgb[:: -1]]])
    hsv_color = cv2.cvtColor(color_to_merge, cv2.COLOR_BGR2HSV)

    h.fill(hsv_color[0][0][0])
    s.fill(hsv_color[0][0][1])

    new_hsv_image = cv2.merge([h, s, v])

    new_hsv_image = cv2.cvtColor(new_hsv_image, cv2.COLOR_HSV2BGR)

    colored_image = cv2.bitwise_and(new_hsv_image, new_hsv_image, mask=mask)
    original_image = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(mask))
    final_img = cv2.bitwise_xor(colored_image, original_image)

    return final_img


def merge_texture(image, mask, texture):
    """Merge the texture with the image using the mask using hsv color space."""

    # if texture is smaller than image, resize it
    # if texture.shape[0] < image.shape[0] or texture.shape[1] < image.shape[1]:
    pattern = cv2.resize(texture, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_AREA)
    # pattern = pil_image_to_cv2(resize_image(cv2_image_to_pil(texture), image.shape[1]))
    # pattern = texture[0:image.shape[0], 0:image.shape[1]]

    # crop texture to image size

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_image)

    hsv_pattern = cv2.cvtColor(pattern, cv2.COLOR_BGR2HSV)
    hp, sp, vp = cv2.split(hsv_pattern)

    # new_h = cv2.add(hp, h)
    # new_s = cv2.add(sp, s)
    # new_v = cv2.add(vp, vp)
    new_v = cv2.addWeighted(v, 0.6, vp, 0.4, 0)  # TODO aggiungere filtro hard mesh? (non serve per demo)

    new_hsv_image = cv2.merge([hp, sp, new_v])
    # new_hsv_image = cv2.merge([new_h, new_s, v])

    new_hsv_image = cv2.cvtColor(new_hsv_image, cv2.COLOR_HSV2BGR)

    colored_image = cv2.bitwise_and(new_hsv_image, new_hsv_image, mask=mask)
    original_image = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(mask))
    final_img = cv2.bitwise_xor(colored_image, original_image)

    return final_img
