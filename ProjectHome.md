This a small tool which I use to crop images under Linux.

```
    Usage:   pycrop [options] file
    
    Description:
             This program crops images. You can either pass a concrete image as
             an argument or the program will process all images from the current 
             directory.
             
             The program uses the tool "convert" from ImageMagic (http://www.imagemagick.org).
             
    Options: 
             -h         : print this help message and exit
             -v         : produce verbose output
             --image    : image file
             
    Keyboard control:
            down        : move the selection down
            up          : move the selection up
            left        : move the selection left
            right       : move the selection right
            +           : zoom in by 5% 
            -           : zoom out by 5% 
            Ctrl +      : zoom in by 1%
            Ctrl -      : zoom out by 1%
            Alt +       : zoom in by 25%
            Alt -       : zoom out by 25%
            Del         : change between landscape and portrait orientation
            Home        : move forward in the list of the preset side ratios 
            End         : move backward in the list of the preset side ratios 
            Enter       : crop the selected image
```