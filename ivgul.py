from js import document, window, OffscreenCanvas
from pyodide.ffi import create_proxy

VOWELS = {
    'ן': '.',
    'ם': '|',
    'ף': ' ָ'.replace(' ', ''),
    'ך': ' ֻ'.replace(' ', ''),
    'ץ': ' ֶ'.replace(' ', ''),
}


DGESHIM = {
    'פ.': 'פּ',
    'ב.': 'בּ',
    'כ.': 'כּ'
}

PUNCTUATION = [',', '.', '!', '?', '-', ':', ";"]

def split_letters(letters):
    found_vowel = None
    
    if count_letters(letters) < 2:
        return None

    vowel_count = 0

    for vowel in VOWELS.keys():
        count = letters.count(vowel)
        if count == 1:
            found_vowel = vowel

        vowel_count += count

    if vowel_count != 1:
        return None

    if found_vowel is None:
        return None

    if found_vowel is not None:
        groups = letters.split(found_vowel)
        groups = groups[0], VOWELS[found_vowel], groups[1]

    if count_letters(groups[0]) > 2 or count_letters(groups[2]) > 2:
        return None

    return groups

def add_letters(ctx, letters, color, size, location_y, scale=1, location_x=14):
    ctx.font = f"{size*scale}px MyDavid"
    ctx.textAlign = "center"
    ctx.fillStyle = color
    ctx.fillText(letters, location_x * scale, (location_y+10) * scale)


def get_max_length(groups):
    return max([count_letters(groups[0]), count_letters(groups[2])])


def get_canvas(height):
    canvas = document.createElement("canvas")
    canvas.height = height
    ctx = canvas.getContext('2d')
    return canvas, ctx

def draw_ivgul_glypph(groups, target, scale=1, color="#000000"):
    canvas, ctx = get_canvas(75 * scale)

    length = get_max_length(groups)

    if groups[1] == '' and groups[2] == '' and groups[0] in PUNCTUATION:
        canvas.width = 28 * scale
        add_letters(ctx, groups[0], color, 80, 45, scale)
    elif groups[2] == '': # 2 tall
        canvas.width = 28 * scale
        if length == 1: # 1 wide
            add_letters(ctx, groups[0], color, 45, 27, scale)
            if groups[1] == "|":
                add_letters(ctx, groups[1], color, 34, 50, scale)
            elif groups[1] == ".":
                add_letters(ctx, groups[1], color, 60, 45, scale)
            elif groups[1] == VOWELS['ך']:
                add_letters(ctx, groups[1], color, 50, 33, scale, 6)
            else:
                add_letters(ctx, groups[1], color, 80, 30, scale, 6)
        else: # 2 wide
            add_letters(ctx, groups[0], color, 25, 17, scale)
            if groups[1] == "|":
                add_letters(ctx, groups[1], color, 50, 50, scale)
            elif groups[1] == ".":
                add_letters(ctx, groups[1], color, 90, 40, scale)
            elif groups[1] == VOWELS['ך']:
                add_letters(ctx, groups[1], color, 50, 33, scale, 6)
            else:
                add_letters(ctx, groups[1], color, 110, 25, scale, 3)

    else: # 3 tall
        if length == 1: # 1 wide
            canvas.width = 17 * scale
            add_letters(ctx, groups[0], color, 25, 17, scale, 8)
            if groups[1] == "|":
                add_letters(ctx, groups[1], color, 25, 35, scale, 8)
            elif groups[1] == ".":
                add_letters(ctx, groups[1], color, 60, 32, scale, 8)
            elif groups[1] == VOWELS['ך']:
                add_letters(ctx, groups[1], color, 45, 20, scale, 0)
            else:
                add_letters(ctx, groups[1], color, 50, 20, scale, 3)
            add_letters(ctx, groups[2], color, 25, 52, scale, 8)
        else: # 2 wide
            canvas.width = 31 * scale
            add_letters(ctx, groups[0], color, 25, 17, scale)
            if groups[1] == "|":
                add_letters(ctx, groups[1], color, 25, 35, scale)
            elif groups[1] == ".":
                add_letters(ctx, groups[1], color, 60, 32, scale)
            elif groups[1] == VOWELS['ך']:
                add_letters(ctx, groups[1], color, 60, 20, scale, 5)
            else:
                add_letters(ctx, groups[1], color, 60, 20, scale, 8)
            add_letters(ctx, groups[2], color, 25, 52, scale)

    document.getElementById(target).appendChild(canvas)


def create_space(target, scale=1):
    canvas, ctx = get_canvas(75*scale)
    canvas.width = 17 * scale
    document.getElementById(target).appendChild(canvas)


def create_linebreak(target):
    document.getElementById(target).appendChild(document.createElement("br"))


def count_letters(letters):
    for dagush in DGESHIM.values():
        letters = letters.replace(dagush, ".")
    return len(letters)


def create_glyph(letters, target, scale=1, color="#000000"):
    groups = split_letters(letters)
    if groups is not None:
        draw_ivgul_glypph(groups, target, scale, color)
    elif count_letters(letters) <= 2:
        draw_ivgul_glypph((letters, "", ""), target, scale, color)


def render_ivgul(text, target, scale=1, color="#000000"):
    for dagesh, dagush in DGESHIM.items():
        text = text.replace(dagesh, dagush)
    first_in_text = True
    first_in_line = True
    first_in_word = True
    for line in text.split("\n"):
        if first_in_line and not first_in_text: # Print line breaks on new lines
            create_linebreak(target)
        first_in_text = False

        for word in line.split(" "):
            if first_in_word and not first_in_line: # Print spaces before new word
                create_space(target, scale)
                first_in_word = False
            first_in_line = False

            for glyph in word.split("|"):
                create_glyph(glyph, target, scale, color)

            first_in_word = True

        first_in_line = True

def create_render_ivgul_js_function_in_window():
    font_container = document.createElement('div')
    font_container.style = "font: 0px MyDavid; position: absolute; visibility: hidden;"
    font_container.innerHTML = "This is required for the font to be loaded"
    document.body.appendChild(font_container)
    proxy = create_proxy(render_ivgul)
    window.render_ivgul = proxy

create_render_ivgul_js_function_in_window()

file_loaded_successfully = True