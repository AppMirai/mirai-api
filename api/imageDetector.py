


class ImageDetector():
    def __init__(self) :
        self.face_datasets = self.os.path.join(self.PROJECT_ROOT, 'shape_predictor_68_face_landmarks.dat')
        self.data_link = str(self.queryset)
        self.base_directory = str(self.MEDIA_ROOT)
        self.image_copy = self.base_directory + '/images/' + self.uid + 'cpy.jpg'
        self.link = self.base_directory + '/' + self.data_link
        
        if(self.os.path.exists(str(self.image_copy))):
            image = self.cv2.imread(self.image_copy)
        else:
            original_image = self.cv2.imread(self.link)
            self.cv2.imwrite(self.image_copy, original_image)
            image = self.cv2.imread(self.image_copy)

        self.detector = self.dlib.get_frontal_face_detector()
        self.predictor = self.dlib.shape_predictor(self.face_datasets)
        self.original_image = image.copy()
        self.gray_image = self.cv2.cvtColor(image, self.cv2.COLOR_BGR2GRAY)
        self.faces = self.detector(self.gray_image)