

class BoundingBox():
    """Contains coordinate of object on the page bottom left of the page correspond to 0,0"""

    def __init__(self, left=None, top=None, right=None, bottom=None, **kwargs):
        self.left = left  #
        self.bottom = bottom
        self.right = right
        self.top = top
        self.space_above = None
        self.space_bellow = None
        self._height = self.bottom - self.top

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def height(self):
        return self.bottom - self.top

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def width(self):
        return self.right - self.left

    def __repr__(self):
        return '(' + str(self.left) + " " + str(self.top) + " " + str(self.right) + " " + str(self.bottom) + " " + ")"



class TextBox(BoundingBox):

    def __init__(self, text, page, index=-1, **kwargs):

        super().__init__(**kwargs)
        self.page = page
        self.original_words = []
        self.add(text)
        self._index = index
        self.paragraph=None

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, TextBox):
            return self.Text == other.Text and self.left == other.left and self.top == other.top
        return False

    def __repr__(self):
        return '<' + self.Text + '>'

    def __str__(self):
        return self.Text

    def __hash__(self):
        return hash(str(self ) +str(self._index))

    def partially_within(self, bbox) -> bool:
        """
        Whether any part of the element is within the bounding box.

        Args:
            bbox (BoundingBox): The bounding box to check whether the element
                is partially within.

        Returns:
            bool: True if any part of the element is within the bounding box.
        """
        return all(
            [
                bbox.left <= self.right,
                bbox.right >= self.left,
                bbox.top <= self.bottom,
                bbox.bottom >= self.top,
            ]
        )

    def within(self, bbox, tollerance=2) -> bool:
        """
        Whether any part of the element is within the bounding box.

        Args:
            bbox (BoundingBox): The bounding box to check whether the element
                is partially within.

        Returns:
            bool: True if any part of the element is within the bounding box.
        """
        return all(
            [
                bbox.left < self.left,
                bbox.right > self.right,
                bbox.top-tollerance <= self.top,
                bbox.bottom+tollerance >= self.bottom,
            ]
        )

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, val):
        self._index=val

    @property
    def page_number(self):
        return self.page.page_number

    @property
    def Text(self):
        return ' '.join([e.Text for e in self.original_words])

    @property
    def width(self):
        return self.right-self.left

    @property
    def left(self):
        return self.bbox.left

    @property
    def right(self):
        return self.bbox.right
    @right.setter
    def right(self, value):
        self.bbox.right=value

    @left.setter
    def left(self, value):
        self.bbox.left=value

    @property
    def top(self):
        return self.bbox.top

    @property
    def bottom(self):
        return self.bbox.bottom

    @property
    def font_size(self) -> float:
        """
        The size of the font.

        This will be taken from the pdf itself, using the most common size within all
        the characters in the element.

        Returns:
            float: The font size of the element, rounded to the font_size_precision of
                the document.
        """

        if hasattr(self, "_font_size"):
            return self._font_size

        counter = Counter(
            (
                word.font_size
                for word in self.original_words
            )
        )
        self._font_size = counter.most_common(1)[0][0]

        return self._font_size


    @property
    def font_name(self) -> float:
        """
        The size of the font.

        This will be taken from the pdf itself, using the most common size within all
        the characters in the element.

        Returns:
            float: The font size of the element, rounded to the font_size_precision of
                the document.
        """

        if hasattr(self, "_font_name"):
            return self._font_name

        counter = Counter(
            (
                word.font_name
                for word in self.original_words
            )
        )
        self._font_name = counter.most_common(1)[0][0]

        return self._font_name

    @property
    def font(self):
        return self.font_name+'+'+str(self.font_size)

    @property
    def is_bold(self):
        return 'bold' in self.font_name.lower()