from __future__ import absolute_import
import re
import math

from PIL import Image, ImageFilter, ImageOps, ImageFile

CUT_SIZE = 10

class TransformImage(object):
    """
    """
    FILTER_MAP = {
      "monochrome": lambda x, y: x._monochrome(*y),
      "alphachrome": lambda x, y: x._alphachrome(*y),
      "nocrop": lambda x, y: x._nocrop(*y),
      "warp": lambda x, y: x._warp(*y),
      "fit": lambda x, y: x._fit(*y),
      "fill": lambda x, y: x._fill(*y),
      "resize": lambda x, y: x._resize(*y),
      "crop": lambda x, y: x._crop(*y),
      "series": lambda x, y: x._do_series(*y),
    }

    def __init__(self, fil,  height=None, width=None):
        self.image = Image.open(fil)
        self.image.load()
        self.format = self.image.format
        if self.format in ('GIF', 'gif') and 'transparency' in self.image.info:
            self.transparency = self.image.info['transparency']
        else:
            self.transparency = None
        self.w, self.h = self.image.size[0]*1.0, self.image.size[1]*1.0
        if(width):
            self.width = width*1.0
        else:
            self.width = self.w
        if(height):
            self.height = height*1.0
        else:
            self.height = self.h

        if self.width == 0:
            self.width = self.w
        if self.height == 0:
            self.height = self.h

    def save_file(self, fileloc, format=None, **kwargs):
        if format is None:
            format = self.format
        if self.transparency is not None:

            if 'transparency' in kwargs:
                transparency = kwargs['transparency']
                kwargs = kwargs.copy()
                del kwargs['transparency']
            else:
                transparency = self.transparency
            self.image.save(fileloc, format, transparency=transparency, optimize=True, **kwargs)
        else:
            self.image.save(fileloc, format, optimize=True, **kwargs)

    def apply_filter(self, filter):
        m = re.match('(\w+)(\((.*)\))?$', filter)
        filter_name = m.group(1)
        args = m.group(3)
        if args is not None:
            args = [item.strip() for item in args.split(',')]
        else:
            args = []
        clean_args = []
        # convert integer arguments into integer values
        for i in range(len(args)):
            try:
                val = int(args[i])
                clean_args.append(val)
            except:
                if args[i]:
                    clean_args.append(args[i])
        filter_func = TransformImage.FILTER_MAP.get(filter_name, None)
        if filter_func is not None:
            filter_func(self, clean_args)
        return self

    def _do_series(self, *filters):
        for filter in filters:
            self.apply_filter(filter)

    def __getrgba(self, value):
        match = re.search(r'^#?[0-9a-fA-F]{3,3}([0-9a-fA-F]{3,3})?([0-9a-fA-F]{2,2})?$', value)
        if match is None:
            raise Exception("Value '%s' is not a valid rgb color hexidecimal." % value)
        if value[0] == '#':
            value = value[1:]

        a = 255
        if len(value) == 3:
            colors = value[0]*2, value[1]*2, value[2]*2
            r, g, b = map(lambda x: int(x, 16), colors)
        elif len(value) == 6:
            colors = value[:2], value[2:4], value[4:6]
            r, g, b = map(lambda x: int(x, 16), colors)
        elif len(value) == 8:
            colors = value[:2], value[2:4], value[4:6], value[6:8]
            r, g, b, a = map(lambda x: int(x, 16), colors)
        else:
            raise Exception("Value '%s' is not a valid rgb color hexidecimal." % s)

        for x in r, g, b, a:
            if x < 0 or x > 255:
                raise TypeError("Somehow a hex value is to greater than 255 or negative.")

        return (r, g, b, a)

    def __make_linear_ramp(self, white):
        ramp = []
        r, g, b = white
        for i in range(255):
            ramp.extend((int(r*i/255), int(g*i/255), int(b*i/255)))
        return ramp

    def _monochrome(self, chrome="FFF0C0", *args):
        r, g, b, a = self.__getrgba(chrome)
        palette = self.__make_linear_ramp((r, g, b))
        # Get the alpha layer:
        if self.image.mode != "RGBA":
            self.image = self.image.convert("RGBA")
        alpha = self.image.split()[-1]
        # Make black and white for applying monochrome.
        self.image = self.image.convert("L")
        # self.image = self.image.convert("1")
        # self.image.save("./image_output/"+output_path+"new", "BMP", quality=100, optimize=True, progressive=True)
        # apply contrast enhancement here
        self.image = ImageOps.autocontrast(self.image)
        # apply monochrome palette
        self.image.putpalette(palette)
        # convert back to RGB
        self.image = self.image.convert("RGBA")
        # put the alpha back onto the image
        self.image.putalpha(alpha)

    def _nocrop(self):
        '''
        :return:
        '''
        raise NotImplementedError

    def _alphachrome(self, chrome="3377FF", *args):
        r, g, b, a = self.__getrgba(chrome)

        # Get the alpha layer:
        if self.image.mode != "RGBA":
            self.image = self.image.convert("RGBA")
        alpha = self.image.split()[-1]

        # generate a solid field of color for the new image.
        colorfield = Image.new('RGBA', (int(self.width), int(self.height)), (r, g, b, a))

        # save the solid color as the image, then apply the alpha to it.
        self.image = colorfield
        self.image.putalpha(alpha)

    def _warp(self, *args):
        ratio_w = (1.0*self.width)/(self.w)
        ratio_h = (1.0*self.height)/(self.h)

        self.image = self.image.resize((int(self.w*ratio_w), int(self.h*ratio_h)), Image.ANTIALIAS)
        self.w, self.h = self.image.size[0]*1.0, self.image.size[1]*1.0

    def _fit(self):
        '''
        _fit shinks the image down so that it fits entirely inside the bounding box.

        The size of the image will be proportional to its original size and
        smaller than the bounding box, or possibly the same size.
        '''

        if (self.w/self.width > self.h/self.height):
            ratio = self.width/self.w
        else:
            ratio = self.height/self.h

        self.image = self.image.resize((int(self.w*ratio), int(self.h*ratio)), Image.ANTIALIAS)
        self.w, self.h = self.image.size[0]*1.0, self.image.size[1]*1.0

    def _fill(self, *args):
        if (self.w/self.width < self.h/self.height):
            ratio = self.width/self.w
        else:
            ratio = self.height/self.h

        self.image = self.image.resize((int(self.w*ratio), int(self.h*ratio)), Image.ANTIALIAS)
        self.w, self.h = self.image.size[0]*1.0, self.image.size[1]*1.0

    def _resize(self, percent=100):
        '''
        _resize shinks the image down to a percentage of its size difference with the
        bounding box, as specified by the "percent" paramater.  The default value for
        "percent" is 100
        '''
        if (self.w/self.width < self.h/self.height):
            diff = abs(self.width-self.w)*percent/100.0
            ratio = (self.width+diff)/self.w
        else:
            diff = abs(self.height-self.h)*percent/100.0
            ratio = (1.0*self.height+diff)/(self.h*1.0)

        self.image = self.image.resize((int(self.w*ratio), int(self.h*ratio), ))
        self.w, self.h = self.image.size[0]*1.0, self.image.size[1]*1.0

    def __entropy(self, image=None):
        image = image if image is not None else self.image
        hist = image.histogram()
        hist_size = sum(hist)

        if hist_size == 0:
            entropy = 0
        else:
            hist = [float(h) / hist_size for h in hist]
            entropy = -sum([p * math.log(p, 2) for p in hist if p != 0])

        return entropy

    def __smartcrop(self):
        self.w, self.h = self.image.size[0]*1.0, self.image.size[1]*1.0
        wdiff = self.w - self.width
        hdiff = self.h - self.height

        while wdiff > 0 or hdiff > 0:
            if wdiff >= hdiff:
                slice_width = int(min(wdiff, CUT_SIZE))
                left = self.image.crop((0, 0, slice_width, int(self.h)))
                right = self.image.crop((int(self.w-slice_width), 0, int(self.w), int(self.h)))

                if self.__entropy(left) > self.__entropy(right):
                    cropbox = (0, 0, int(self.w - slice_width), int(self.h))
                else:
                    cropbox = (slice_width, 0, int(self.w), int(self.h))

            else:
                slice_height = int(min(hdiff, CUT_SIZE))
                top = self.image.crop((0, 0, int(self.w), slice_height))
                bottom = self.image.crop((0, int(self.h - slice_height), int(self.w), int(self.h)))

                if self.__entropy(top) > self.__entropy(bottom):
                    cropbox = (0, 0, int(self.w), int(self.h - slice_height))
                else:
                    cropbox = (0, slice_height, int(self.w), int(self.h))

            self.image = self.image.crop(cropbox)
            self.w, self.h = self.image.size[0]*1.0, self.image.size[1]*1.0

            wdiff = self.w - self.width
            hdiff = self.h - self.height

    def _crop(self, retain="center", background=None):
        '''
        If a "background" is specified (in the string-hex format RRGGBBAA), then the image
        will be sized to match the bounding box, with extra space filled by the specified
        "background" color+alpha, and with the image placed at the location specified by
        the "retain" parameter.

        Otherwise, the crop will simply cut away aspects of the image that are outside
        the bounding box,
        '''
        if retain == "center":
            crop_w = (self.w-self.width)/2
            crop_h = (self.h-self.height)/2

            cropbox = (crop_w, crop_h, crop_w+self.width, crop_h+self.height)
            # cropbox = map(lambda x: int(x), cropbox)
            cropbox = list(map(int, cropbox))

            self.image = self.image.crop(cropbox)
            self.w, self.h = self.image.size[0]*1.0, self.image.size[1]*1.0

        elif retain == "top-left":
            cropbox = (0, 0, int(self.width), int(self.height))

            self.image = self.image.crop(cropbox)
            self.w, self.h = self.image.size[0]*1.0, self.image.size[1]*1.0

        elif retain == "bottom-right":
            cropbox = (self.w - self.width, self.h - self.height, self.w, self.h)
            cropbox = map(lambda x: int(x), cropbox)

            self.image = self.image.crop(cropbox)
            self.w, self.h = self.image.size[0]*1.0, self.image.size[1]*1.0

        elif retain == "smart":
            self.__smartcrop()

        else:
            raise TypeError("Crop instruction retain=%s is not understood." % retain)

        if background is not None and background != '':
            self._background(retain, background)

    def _background(self, placement="center", background="FFFFFF00"):

        r, g, b, a = self.__getrgba(background)
        background = Image.new('RGBA', (int(self.width), int(self.height)), (r, g, b, a))

        if placement == "center":
            box = (self.width-self.w)/2, (self.height-self.h)/2
        if placement == "top-left":
            box = (0, 0)
        if placement == "bottom-right":
            box = (self.width-self.w, self.height-self.h)
        box = tuple(map(lambda x: int(x), box))

        background.paste(self.image, box)
        self.image = background
        self.w, self.h = self.image.size[0]*1.0, self.image.size[1]*1.0

