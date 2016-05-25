from morse.core import blenderapi
from morse.core.services import service


@service(component="random")
def randomize():
    print("\n\n\n\n\n\n\n\n\n__________________\n________________\nrandomize!!!\n\n\n\n\n\n\n\n\n\n\n\n\n")
    from morse.builder import morsebuilder
    objlist = morsebuilder.bpymorse.get_objects()
    boxlist = list(filter(lambda x: x.name.startswith("Box."), objlist))

    import random
    random.shuffle(boxlist)

    morsebuilder.bpymorse.delete(boxlist)

    for i, box in enumerate(boxlist):
        x = i % 5
        y = i // 5
        print(box)
        print(box.location)
        box.location = (-10 + x * 3, -6 + y * 4, 0.51)
        print(box.location)
