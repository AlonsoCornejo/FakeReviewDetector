import pickle

if __name__ == "__main__":

    path = '../Yelp_Dataset/'
    d = 'example_1'

    userPriors = {'201':0.12, '202': 0.13}
    prodPriors = {'0':0.45}
    reviewPriors = {('201','0'): 0.001, ('202', '0'):0.1}

    with open(path + d + '/UserPriors.pickle', 'wb') as f:
        pickle.dump(userPriors, f)
    with open(path + d + '/ProdPriors.pickle', 'wb') as f:
        pickle.dump(prodPriors, f)
    with open(path + d + '/ReviewPriors.pickle', 'wb') as f:
        pickle.dump(reviewPriors, f)
