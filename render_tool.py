import dmap2gcode
from PIL import Image
from math import inf

IMAGE_SCALE = 50
PIXEL_SIZE  = (1/3.65) / IMAGE_SCALE # mm

TOOL_COLOR = (127, 127, 127, 255)
BACKGROUND_COLOR = (255,0,255,0)

tools = {
    'ball3': dmap2gcode.make_tool_shape(dmap2gcode.ball_tool, 3, PIXEL_SIZE),
    'ball6': dmap2gcode.make_tool_shape(dmap2gcode.ball_tool, 6, PIXEL_SIZE),
    '45v6':  dmap2gcode.make_tool_shape(dmap2gcode.vee_common(45), 6, PIXEL_SIZE),
    '15v6':  dmap2gcode.make_tool_shape(dmap2gcode.vee_common(15), 6, PIXEL_SIZE),
    '90v6':  dmap2gcode.make_tool_shape(dmap2gcode.vee_common(90), 6, PIXEL_SIZE),
    '45taper2b6':  dmap2gcode.make_tool_shape(dmap2gcode.taper_ball_common(45, 2), 6, PIXEL_SIZE),
}


for name, tool in tools.items():
    print(name)
    #print(tool)
    #print(tool.shape)
    #print(tool.matrix.shape)

    toolmax = max([n for n in tool.matrix.flat if n != inf])

    #print(toolmax)
    m = (tool.matrix / toolmax) * 256
    #im = Image.new("P", tool.shape)
    im = Image.fromarray(m, "F")
    im.convert('RGBA').save(name + '.png')

    

    im2 = Image.new('RGBA', (tool.height,int(toolmax/PIXEL_SIZE+1)), BACKGROUND_COLOR)
    #print(im2.size)

    for x in range(im2.size[0]):
        _infless = [n for n in tool.matrix[x].flat if n != inf]
        #print(x, _infless)
        if not _infless:
            continue
        
        _min = min(_infless)/PIXEL_SIZE
        _max = max(_infless)/PIXEL_SIZE

        #print(_min, _max)
        for y in range(im2.size[1]):
            if y >= _min:
                #edge = min(abs(y - _min), abs(y - _max))
                im2.putpixel((x,y), TOOL_COLOR)
    
    #im2.save(name + '_side.png')

    n_height = max(im2.height + (10/IMAGE_SCALE/PIXEL_SIZE), 80/IMAGE_SCALE/PIXEL_SIZE)
    n_width = im2.width + (20/IMAGE_SCALE/PIXEL_SIZE)

    im3 = Image.new('RGBA', (int(n_width), int(n_height)), BACKGROUND_COLOR)

    w_pos = int((im3.width - im2.width)/2)
    im3.paste(im2, (w_pos,0))

    section = im2.crop((0,im2.height-1,im2.width,im2.height)).resize((im2.width, im3.height-im2.height))
    im3.paste(section, (w_pos, im2.height))

    im4 = Image.new('RGBA', (im3.width, int(im3.height + 10/IMAGE_SCALE/PIXEL_SIZE)), BACKGROUND_COLOR)
    im4.paste(im3.transpose(Image.FLIP_TOP_BOTTOM))
    im4.save(name + '_side.png')

    