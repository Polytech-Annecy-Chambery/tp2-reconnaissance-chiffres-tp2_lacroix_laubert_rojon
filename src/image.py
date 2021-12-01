from skimage import io
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np

class Image:
    def __init__(self):
        """Initialisation d'une image composee d'un tableau numpy 2D vide
        (pixels) et de 2 dimensions (H = height et W = width) mises a 0
        """
        self.pixels = None
        self.H = 0
        self.W = 0
    

    def set_pixels(self, tab_pixels):
        """ Remplissage du tableau pixels de l'image self avec un tableau 2D (tab_pixels)
        et affectation des dimensions de l'image self avec les dimensions 
        du tableau 2D (tab_pixels) 
        """
        self.pixels = tab_pixels
        self.H, self.W = self.pixels.shape


    def load(self, file_name):
        """ Lecture d'un image a partir d'un fichier de nom "file_name"""
        self.pixels = io.imread(file_name)
        self.H,self.W = self.pixels.shape 
        print("lecture image : " + file_name + " (" + str(self.H) + "x" + str(self.W) + ")")


    def display(self, window_name):
        """Affichage a l'ecran d'une image"""
        fig = plt.figure(window_name)
        if (not (self.pixels is None)):
            io.imshow(self.pixels)
            io.show()
        else:
            print("L'image est vide. Rien à afficher")


    #==============================================================================
    # Methode de binarisation
    # 2 parametres :
    #   self : l'image a binariser
    #   S : le seuil de binarisation
    #   on retourne une nouvelle image binarisee
    #==============================================================================
    def binarisation(self, S):
        # creation d'une image vide
        im_bin = Image()
        
        # affectation a l'image im_bin d'un tableau de pixels de meme taille
        # que self dont les intensites, de type uint8 (8bits non signes),
        # sont mises a 0
        im_bin.set_pixels(np.zeros((self.H, self.W), dtype=np.uint8))

        # TODO: boucle imbriquees pour parcourir tous les pixels de l'image im_bin
        # et calculer l'image binaire
        for i in  range(self.H):
            for j in range(self.W): 
                if self.pixels[i][j]>=S:
                    im_bin.pixels[i][j] = 255
                else:
                    im_bin.pixels[i][j] = 0
        
        return im_bin
        pass


    #==============================================================================
    # Dans une image binaire contenant une forme noire sur un fond blanc
    # la methode 'localisation' permet de limiter l'image au rectangle englobant
    # la forme noire
    # 1 parametre :
    #   self : l'image binaire que l'on veut recadrer
    #   on retourne une nouvelle image recadree
    #==============================================================================
    def localisation(self):
        L_max = 0
        L_min = self.H
        C_max = 0
        C_min = self.W
        for i in range(self.H):
            for j in range(self.W):
                if (self.pixels[i][j]==0):
                    if i<L_min:
                        L_min = i
                    if j<C_min:
                        C_min = j
                    if i>L_min:
                        L_max = i
                    if j>C_min:
                        C_max = j
        nbl=L_max-L_min
        nbc=C_max-C_min
        im_loc = Image()
        im_loc.set_pixels(np.zeros((nbl,nbc), dtype=np.uint8))
        for i in range(L_max-L_min):
            for j in range(C_max-C_min):
                im_loc.pixels[i][j]=self.pixels[L_min+i][C_min+j]
                
        return(im_loc)
        pass

    #==============================================================================
    # Methode de redimensionnement d'image
    #==============================================================================
    def resize(self, new_H, new_W):
        im_resized=resize(self.pixels, (new_H,new_W), 0)
        im_resized=np.uint8(im_resized*255)
        im_res = Image()
        im_res.set_pixels(np.zeros((new_H,new_W), dtype=np.uint8))
        for i in range(new_H):
            for j in range(new_W):
                im_res.pixels[i][j]=im_resized[i][j]
        return(im_res)
        pass


    #==============================================================================
    # Methode de mesure de similitude entre l'image self et un modele im
    #==============================================================================
    def similitude(self, im):
        sim=0 
        for i in range(self.H): 
            for j in range(self.W): 
                if self.pixels[i][j]==im.pixels[i][j]: 
                    sim+=1 
        return(sim/(im.H*im.W)) 
        pass


