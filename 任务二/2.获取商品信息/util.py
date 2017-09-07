import hashlib


def  get_pic_md5(image_url, product_id):
    #http://gd4.alicdn.com/imgextra/i4/489950660/TB2nsRBmthvOuFjSZFBXXcZgFXa_!!489950660.jpg_400x400.jpg
    image_url = (image_url + product_id).encode("utf-8")
    a = hashlib.md5(image_url).hexdigest()
    return  (a)


if __name__ == '__main__':
    print (get_pic_md5('http://gd4.alicdn.com/imgextra/i4/489950660/TB2nsRBmthvOuFjSZFBXXcZgFXa_!!489950660.jpg_400x400.jpg','549952875318'))