As a first approach I tried the simplest neural network possible with only a dense 128 unit layer. Surprisingly that was enough for 90% accuracy. This performance is probably due to every image having the road sign close to the center. 

Investigating further I learned that convolutional neural networks with several convolutional and pooling layers work very well for computer vision. As I understand, this is so because they greatly reduce the number of parameters to train as well as searching for learned features throughout the image.

After a bit of trial and error, what worked best was 3 stacks of convolutional plus pooling layers. More or less of them would somehow decrease accuracy. Then I tuned the image width and height to 50 and increased the number of epochs to 15 finding a sweetspot where I got my highest accuracy of 98% on an average run and up to 99% once.

I had to reduce the number of epochs to keep the video under 5 minutes