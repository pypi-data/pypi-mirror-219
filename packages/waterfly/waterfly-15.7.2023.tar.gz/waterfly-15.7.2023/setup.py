from setuptools import setup

setup(
    name='waterfly',
    version='15.7.2023',
    install_requires=[
        'googletrans>=3.1.0a0',
        'opencv-python',
        'rembg',
        'requests',
        'pyautogui',
        'qrcode'
    ],
    description='Waterfly is a powerful new AI tool to create Firefly URLs, process images, and draw on images.',
    long_description='''

Hi here!

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

    ABOUT NEW

— New functions such as create.textimage(), create.palette(), edit.oldtv(), random.image_url(), 
info.image.created(), info.image.motificated(), info.image.exist() and more

— Added a filter for premium images, now when you generate premium images,
images with watermarks are ignored!

— The code is now better commented

— Firefly-referenced functions no longer require translation,
so this has been removed for optimisation purposes

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

    CREATE URLS FOR IMAGES AND TEXT STYLES

create.image('Chocolate tree', ['hyper_realistic', 'cool_colors', 'studio_light'], 'portrait')
Create a great photo of a chocolate tree for your Instagram stories with very realistic graphics,
beautiful colors, and studio lighting.
Not interested in stories? Create something else! Example:
create.image('Sakura tree', ['cartoon', 'beautiful', 'pastel_colors', dramatic_light'], 'widescreen')
Creates a beautifully drawn picture of a sakura tree, in cartoon style, beautiful,
in pastel colors and with dramatic lighting,
with an aspect ratio that is ideal for desktop backgrounds

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

    ALREADY HAVE THE IMAGE YOU NEED? EDIT IT!

The code that will remove the background:
edit.backdrop('image.img', 'backdrop.img')
You can add a vignette like this:
edit.vignette('image.img', level)
Turn the image into a cartoon:
edit.cartoon('image.img')

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

    LIFEHACKS

1. A vulnerability has been discovered in Adobe Firefly, you can upload images without a watermark!
   Check the element code and find the img tag with alt="Variation n of 4",
   follow the link in the src and upload the image with the PNG or JPG extension

2. If you don't know how much time it takes to create random image, itc.

        from waterfly import*
        from time import time

        start = time()
        random.image()
        print(f'The code execution took {time()-start} seconds')

   The result should be as follows

        The code execution took 0.9839651584625244 seconds

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Want to point out something in an image?
Build any shape with lines and ellipses!

And much more...

''',
    author = 'Igor_Shapovalov_Andrejovich',
    packages = ['waterfly'],
    author_email = 'igor.shapovalov.andrejovich@gmail.com'
)