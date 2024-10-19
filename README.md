Started out with just one conv layer with 32 filters, 3x3 kernel, input size (w, h, 3)

Added a second with 64 filters, 5x5 kernel, input size (w,h,32) yielded .72 accuracy

Switched the second conv to input size (w, h, 96) got .87 accuracy

Switches the second conv kernel to 7 and 3 and performed worse and switching the first conv to 5 is worse too

removing the second dense layer with drop out yields .84 accuracy

increasing nodes to 256 from 128 is bad

