def get_graphcordinates(image_path,x_range,y_range,background_value):
    """
    x_range=[2018,2023]   #start and end point of horizontal direction of image
    y_range=[0,800]        #start and end point of vertical direction of image
    image_path='/kaggle /input/tata-stock-price/tata_stock_price.png'
    background_value=1   #1 for white background and dark plot
    """
    import matplotlib.pyplot as plt
    import numpy as np
    from PIL import Image

    image=Image.open(image_path)

    grayscale_image = image.convert('L')
    grayscale_image_arr=np.array(grayscale_image)
    length=grayscale_image_arr.shape[0]
    width=grayscale_image_arr.shape[1]
    
    if background_value==0: # If background is dark and plot is dark, we do the reverse
        grayscale_image_arr=255-grayscale_image_arr

    y_axis=[]
    for j in range(width):
        column=grayscale_image_arr[:,j]
        y=length-np.argmin(column)
        y_axis.append(y)
    y_axis=np.array(y_axis)
    x_axis=np.linspace(0,width,width)


    y_axis=y_range[0]+ ( y_axis*( y_range[1]-y_range[0] ) )/ length
    x_axis=x_range[0]+ ( x_axis*( x_range[1]-x_range[0] ) )/ width
    
    array=np.zeros((width,2))
    array[:,0]=x_axis
    array[:,1]=y_axis
    
    return array