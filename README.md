# ImageStego
Demonstration of LSB Steganography, able to store Images or Binaries.

## Building Program
Run the following command in the root folder of the project:
```
python setup.py bdist
```

In the folder *dist* you should find the newly created distributable package.

For more options, please see python *setuptools*.

## Dependencies
* Python3
* Pillow
* bitstring

## Usage

Store Image: 
```
ImageStego.py -o misc/Stego -b misc/Bitplanes -si <path to image to hide> <path to image>
```
Extract Image: 
```
ImageStego.py -o misc/Stego -b misc/Bitplanes -ei <path to write hidden image> <path to image>
```
Store Binary Data: 
```
ImageStego.py -o misc/Stego -b misc/Bitplanes -s <path to binary> <path to image>
```
Extract Binary Data:
```
ImageStego.py -o misc/Stego -b misc/Bitplanes -e <path to binary to write> <path to image>
```

## Author
Kevin Almansa
