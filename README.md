# Detecting cars on images (JPEG)  

---

Example app showing cars (*cars, trucks and buses*) detection on jpeg images.  
It uses standard **resnet50_fpn** model from **torchvision** library of **PyTorch**.
It could be deployed with Docker file but this will work when container is started with root privileges.

When You start Docker container without root privileges please go to:  
https://github.com/MWKSolution/object-detector-mog  
which is version of this app for such a case.

Working example of this app could be seen at:  
https://object-detecto-prod-object-detector-fgvx4s.mo2.mogenius.io/

![result](https://user-images.githubusercontent.com/105928466/177966317-a465b2f2-4766-4220-b850-92acd670cb68.jpg)