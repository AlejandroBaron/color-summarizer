"Source: https://www.hackerearth.com/practice/notes/extracting-pixel-values-of-an-image-in-python/"
from PIL import Image
import numpy as np
import sys

from sklearn import datasets
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
import scipy.misc as scp

"INPUTS"
test= sys.argv[1]
n_colours=int(sys.argv[2])
method=sys.argv[3]


"Creating an Image object from the test file"
img = Image.open(test,'r')
img.show()
"List with all pixel values (R,G,B)"
pix_val = list(img.getdata())

n_pix= len(pix_val)


"Converting tuples (R,G,B) to lists [R,G,B] for sklearn"
Pixels=[]

for triplets in pix_val:
    Pixels.append(list(triplets))



"Training the model with the selected method"

if method=="mixture":
    gmm=GaussianMixture(n_components=n_colours).fit(Pixels)
    prediction=gmm.predict(Pixels)
    centers=gmm.means_
elif method=="kmeans":
    kmeans=KMeans(n_clusters=n_colours).fit(Pixels)
    prediction=kmeans.labels_
    centers=kmeans.cluster_centers_
elif method=="aglomerative":
    #print "Introduce metric to compute \n -metric \n -euclidean \n manhattan"
    metric="metric"
    #print "Introduce Linkage (ward,complete or average)"
    link="average"

    agg=AgglomerativeClustering(n_clusters=n_colours).fit(Pixels)
    prediction=agg.fit(X)

    "Calculating centroids"
    #centers=[rsum,bsum,gsum]

    "For each partition"
    for i in range(n_colours):
        "For each R,G, and B we find the average"
        for j in range(3):
            if prediction[i]==i:
                "If the partition matches the i index, meaning we are in the one to which the point belongs"
                centers[i][j]=centers[i][j]+Pixels[i][j]/prediction.count(i)

else:
    exit()


"Making the centers as 3 element tuples"
rounded_centers=[]
for i in range(len(centers)):
    rounded_centers.append(tuple([int(round(x)) for x in centers[i]]))

print(rounded_centers)


"Reconstructing the image from the aproximated pixels (centers of the clusters)"
recover_array=[]
for i in range(n_pix):
    triplet=rounded_centers[prediction[i]]
    recover_array.append(triplet)

"Loading the picture"
recover = Image.new(img.mode,img.size)
recover.putdata(recover_array)
recover.save('test_out.png')

recover.show()
