def load_and_preprocess_img(path):
    import numpy as np
    from PIL import Image
    from torchvision import transforms


    transform = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                        std=[0.229, 0.224, 0.225])
                ])
    img = Image.open(path)
    img = transform(img).numpy()
    return np.expand_dims(img, axis=0)
