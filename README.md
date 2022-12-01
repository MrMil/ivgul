# עיבגול
עיבגול היא שיטת כתיבה לעברית בהשראת שיטת הכתיבה הקוראנית הנגול.
על מנת להבין איך זה נראה ועובד, אפשר להיכנס לאתר שיש בו הסבר [כאן](https://mrmil.github.io/ivgul/)

# How to use
```html
<head>
    <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
    <script defer src="https://pyscript.net/latest/pyscript.js"></script>
    <py-script src="https://mrmil.github.io/ivgul/ivgul.pys"></py-script>
</head>
```

This will add a function called `render_ivgul` to your window object.

These are the parameters the function takes:
 * text - the text to display in the format described in the website
 * target - the id of the target DOM object to put the glyphs into
 * scale - optional, The glyphs created will be 75 pixels tall times the scale.
 * color - optional, the color of the glyph.

Example use:
```js
render_ivgul("שף|לםמ", "ivgul_container", 2, "#FF0000")
```

will create a glyph saying "שלום" in ivgul twice the default size in red letters.
