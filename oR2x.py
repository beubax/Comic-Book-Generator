import requests
import os.path
import openai.error
import tqdm
import io
# from PIL import Image, ImageDraw, ImageFont
import openai

openai.api_key = "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"
# story = """
# Lakshmannan was a fat, Tamil villain who lived in a small village on the outskirts of town. He was known for his greedy and dishonest ways, and many people in the village disliked him.
# One day, Lakshmannan's brother, who lived in a different town, heard about his brother's reputation and decided to take revenge on him. He knew that Lakshmannan had a weakness for sweets, so he came up with a plan to trick him.
# He disguised himself as a kind old man and went to visit Lakshmannan, pretending to be a distant relative. He brought with him a large basket of sweets and offered them to Lakshmannan as a gift.
# Lakshmannan, who couldn't resist the temptation of sweets, eagerly accepted the gift and gobbled them all up. However, little did he know that his brother had laced the sweets with a powerful laxative.
# As soon as Lakshmannan ate the sweets, he began to feel a sudden urge to use the bathroom. He rushed to the bathroom, but it was too late. The laxative took effect and he was stuck in the bathroom for hours, feeling embarrassed and humiliated.
# In the end, Lakshmannan learned his lesson and vowed to be a better person. He apologized to all the people he had wronged and made amends for his past mistakes. And from that day on, he lived a much happier and fulfilling life.
# """
# sentences = story.split('.')

# images: list[Image.Image] = []


# DIM = 512

# for index, sentence in tqdm.tqdm(list(enumerate(sentences))):
#     filename = f'story-{index:03}.png'
#     if os.path.exists(filename):
#         continue

#     try:
#         response = openai.Image.create(
#             prompt= f'{sentence} anime style',
#             n=1,
#             size="512x512"
#         )
#         image_url = response['data'][0]['url']
#     except openai.error.InvalidRequestError:
#         image_url = 'https://ca-times.brightspotcdn.com/dims4/default/0ccdca9/2147483647/strip/true/crop/2048x1075+0+144/resize/1200x630!/quality/80/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2F78%2Fa1%2F233543333be12375cedd5993fad3%2Fla-me-california-gay-marriage-20150626-picture-005'
#     response = requests.get(image_url)
#     response.raise_for_status()

#     with open(filename, 'wb') as f:
#         f.write(response.content)

# for index, sentence in tqdm.tqdm(list(enumerate(sentences))):
#     MAX_WIDTH = 50

#     words = sentence.split()

#     line_words = []

#     for index_, word in enumerate(words):
#         line_words.append(word)
#         if (index_ + 1) % 7 == 0:
#             line_words.append('\n')

#     sentence = ' '.join(line_words)

#     print(sentence)





#     filename = f'story-{index:03}.png'

#     with open(filename, 'rb') as f:
#         im = Image.open(f)
#         font = ImageFont.truetype("Acme-Regular.ttf", 27)
#         draw = ImageDraw.Draw(im)
#         # draw.multiline_textbbox((10,10), sentence, font=font, spacing=500, align="right")
#         x, y = (10, 10)
#         text = sentence
#         shadowcolor = (0,0,0)
#         fillcolor = (255,255,255)

#         # thicker border
#         draw.multiline_text((x-1, y-1), text, font=font, fill=shadowcolor)
#         draw.multiline_text((x+1, y-1), text, font=font, fill=shadowcolor)
#         draw.multiline_text((x-1, y+1), text, font=font, fill=shadowcolor)
#         draw.multiline_text((x+1, y+1), text, font=font, fill=shadowcolor)

#         # now draw the text over it
#         draw.multiline_text((x, y), text, font=font, fill=fillcolor)
        
#         images.append(im)

# comic_pallete = Image.new("RGBA", (DIM, DIM*len(images)))

# for index, img_buffer in enumerate(images):
#     comic_pallete.paste(img_buffer, (0, index*DIM))


# comic_pallete.show()

# response = openai.Image.create_variation(
#   image=open("test.png", "rb"),
#   n=1,
#   size="1024x1024"
# )
# print(response['data'][0]['url'])

import cv2
import numpy as np

# load image
img = cv2.imread('foreground.png')

# convert to graky
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# threshold input image as mask
mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]

# negate mask
mask = 255 - mask

# apply morphology to remove isolated extraneous noise
# use borderconstant of black since foreground touches the edges
kernel = np.ones((3,3), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# anti-alias the mask -- blur then stretch
# blur alpha channel
mask = cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)

# linear stretch so that 127.5 goes to 0, but 255 stays 255
mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

# put mask into alpha channel
result = img.copy()
result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
result[:, :, 3] = mask

# save resulting masked image
cv2.imwrite('person_transp_bckgrnd.png', result)

# display result, though it won't show transparency
cv2.imshow("INPUT", img)
cv2.imshow("GRAY", gray)
cv2.imshow("MASK", mask)
cv2.imshow("RESULT", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
