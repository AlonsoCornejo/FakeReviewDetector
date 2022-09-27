import sys

sys.path.insert(0, '../Utils')
from iohelper import *
from review_op import *
from eval_helper import *

sys.path.insert(0, 'featureExtractorPy/')
from updated_featureExtraction import *
from SpEagle import *

import pickle
import numpy as np

dataset_names = ['YelpChi', 'YelpNYC', 'YelpZip']
path = '../Yelp_Dataset/'

feature_name_path = './'
feature_name_filename = 'feature_list_matlab.txt'
user_feature_names, prod_feature_names, review_feature_names = load_feature_names(feature_name_path,
                                                                                  feature_name_filename)
# read polarity of the features
feature_suspicious_filename = 'feature_configuration.txt'
feature_config = load_feature_config(feature_name_path, feature_suspicious_filename)

def construct_feature_priors(dataset_name, user_data, prod_data):

    # extract features
    extractor = FeatureExtractor()
    userFeatures, prodFeatures, reviewFeatures = extractor.construct_all_features(user_data, prod_data)

    # save features
    with open(path + dataset_name + '/UserFeatures.pickle', 'wb') as f:
        pickle.dump(userFeatures, f)
    with open(path + dataset_name + '/ProdFeatures.pickle', 'wb') as f:
        pickle.dump(prodFeatures, f)
    with open(path + dataset_name + '/ReviewFeatures.pickle', 'wb') as f:
        pickle.dump(reviewFeatures, f)

    # calculate priors
    userPriors = extractor.calculateNodePriors(user_feature_names, userFeatures, feature_config)
    prodPriors = extractor.calculateNodePriors(prod_feature_names, prodFeatures, feature_config)
    reviewPriors = extractor.calculateNodePriors(review_feature_names, reviewFeatures, feature_config)

    # save priors
    with open(path + dataset_name + '/UserPriors.pickle', 'wb') as f:
        pickle.dump(userPriors, f)
    with open(path + dataset_name + '/ProdPriors.pickle', 'wb') as f:
        pickle.dump(prodPriors, f)
    with open(path + dataset_name + '/ReviewPriors.pickle', 'wb') as f:
        pickle.dump(reviewPriors, f)

def TestSpEagle(user_data, priors, verbose = False):

    """
    Run SpEagle in a regular setting with all data
    :param user_data:
    :param priors:
    :param verbose:
    :return:
    """
    if verbose:
        print("\n======TestSpEagle======\n")
    # set up SpEagle for detection
    numerical_eps = 1e-5
    user_review_potential = np.log(np.array([[1 - numerical_eps, numerical_eps], [numerical_eps, 1 - numerical_eps]]))
    eps = 0.1
    review_product_potential = np.log(np.array([[1 - eps, eps], [eps, 1 - eps]]))

    potentials = {'u_r': user_review_potential, 'r_u': user_review_potential,
                  'r_p': review_product_potential, 'p_r': review_product_potential}

    user_ground_truth, review_ground_truth = create_ground_truth(user_data)

    print('Use SpEagle without labeled data:')
    print('\tUser AUC\tReview AUC')
    model = SpEagle(user_data, priors, potentials, max_iters = 10)
    model.schedule(schedule_type='bfs')

    iter = 0
    while iter < 10:

        # set up additional number of iterations
        if iter == 0:
            num_bp_iters = 2
        else:
            num_bp_iters = 1

        message_diff = model.run_bp(start_iter = iter, max_iters = num_bp_iters)

        iter += num_bp_iters

        # userBelief, reviewBelief, prodBelief = model.classify()
        # user_auc = evaluate(user_ground_truth, userBelief)
        # review_auc = evaluate(review_ground_truth, reviewBelief)
        # print('\t%f\t%f' % (user_auc, review_auc))

        if message_diff < 1e-3:
            break
    return userBelief, reviewBelief, prodBelief

def construct_review_features():
    """
    Concatenate user, product, and reviews features into a single feature vector of the review.
    :return:
    """
    review_feature_dict, num_features =create_review_features(userFeatures, prodFeatures, reviewFeatures,
                                    user_feature_names, prod_feature_names, review_feature_names)
    out_f = open('review_label_predictions_features.pickle', 'w')
    _, review_ground_truth = create_ground_truth(user_data)
    results = np.zeros((len(review_ground_truth), 2 + num_features))
    # output posteriors to file
    for k, v in review_ground_truth.items():
        review_feature = review_feature_dict[k]
        review_feature = np.concatenate(([v, reviewBelief[k]], review_feature))
        review_feature = np.reshape(review_feature, (-1, 2 + num_features))
        results = np.concatenate((results, review_feature), axis=0)
    pickle.dump(results[1:,:], out_f)
    out_f.close()

def TestStreamSpEagle(user_data, priors, num_hops = 1, old_data_ratio = 0.1, random_sample = False, verbose = False):

    """
    Test streaming SpEagle
    :return:
    """

    if verbose:
        print("\n======TestStreamSpEagle======\n")
    # randomly partition the data
    old_user_data = {}
    new_user_data = {}
    total_reviews = 0
    for u_id, reviews in user_data.items():
        total_reviews += len(reviews)

    old_data_size = int(old_data_ratio * total_reviews)

    print ("old_data_size = %d" % old_data_size)

    cur_old_data_size = 0

    for u_id, reviews in user_data.items():
        for r in reviews:
            if random_sample:
                if np.random.rand() > 0.1:
                    if u_id not in new_user_data:
                        new_user_data[u_id] = []
                    new_user_data[u_id].append(r)
                else:
                    if u_id not in old_user_data:
                        old_user_data[u_id] = []
                    old_user_data[u_id].append(r)
            else:
                if cur_old_data_size > old_data_size:
                    if u_id not in new_user_data:
                        new_user_data[u_id] = []
                    new_user_data[u_id].append(r)
                else:
                    if u_id not in old_user_data:
                        old_user_data[u_id] = []
                    old_user_data[u_id].append(r)
                    cur_old_data_size += 1

    numerical_eps = 1e-5
    user_review_potential = np.log(
        np.array([[1 - numerical_eps, numerical_eps], [numerical_eps, 1 - numerical_eps]]))
    eps = 0.1
    review_product_potential = np.log(np.array([[1 - eps, eps], [eps, 1 - eps]]))

    potentials = {'u_r': user_review_potential, 'r_u': user_review_potential,
                  'r_p': review_product_potential, 'p_r': review_product_potential}

    user_ground_truth, review_ground_truth = create_ground_truth(user_data)

    model = SpEagle(old_user_data, priors, potentials, max_iters = 10)
    model.schedule(schedule_type='bfs')

    #
    # run SpEagle on the first part of the data
    iter = 0
    while iter < 10:

        # set up additional number of iterations
        if iter == 0:
            num_bp_iters = 2
        else:
            num_bp_iters = 1

        message_diff = model.run_bp(start_iter=iter, max_iters=num_bp_iters)

        iter += num_bp_iters

        if message_diff < 1e-3:
            break

    # add more data
    model.add_new_data(new_user_data, priors)
    starting_nodes = set()
    for u_id, reviews in new_user_data.items():
        unique_u_id = 'u' + u_id
        starting_nodes.add(unique_u_id)
        for r in reviews:
            unique_p_id = 'p' + r[0]
            starting_nodes.add(unique_p_id)
            starting_nodes.add((unique_u_id, unique_p_id))
    starting_nodes = list(starting_nodes)
    model.local_schedule(starting_nodes, num_hops=num_hops)

    # re-run SpEagle on the newly-generated schedule
    iter = 0
    while iter < 10:

        # set up additional number of iterations
        if iter == 0:
            num_bp_iters = 2
        else:
            num_bp_iters = 1

        message_diff = model.run_bp(start_iter=iter, max_iters=num_bp_iters)

        iter += num_bp_iters

        userBelief, reviewBelief, prodBelief = model.classify()
        user_auc = evaluate(user_ground_truth, userBelief)
        review_auc = evaluate(review_ground_truth, reviewBelief)
        print('\t%f\t%f' % (user_auc, review_auc))
        if message_diff < 1e-3:
            break
    return userBelief, reviewBelief, prodBelief

if __name__ == '__main__':

    for d in dataset_names:
        metadata_filename = path + d + '/metadata.gz'
        user_data, prod_data = read_graph_data(metadata_filename)
        with open(path + d + '/UserPriors.pickle', 'rb') as f:
            userPriors = pickle.load(f)
        with open(path + d + '/ProdPriors.pickle', 'rb') as f:
            prodPriors = pickle.load(f)
        with open(path + d + '/ReviewPriors.pickle', 'rb') as f:
            reviewPriors = pickle.load(f)

        num_spams = 0
        for k, v in user_data.items():
            for r in v:
                if r[2] == -1:
                    num_spams += 1
        print(num_spams)
        priors = [userPriors, prodPriors, reviewPriors]

        # userBelief, reviewBelief, prodBelief = TestSpEagle(user_data, priors, verbose=True)
        
        # run multiple random tests
        # for h in range(1, 10):
        #     print ('num_hops = %d' % h)

        #     new_userBelief, new_reviewBelief, new_prodBelief = TestStreamSpEagle(user_data, priors, num_hops = h, old_data_ratio = 0.01, random_sample = False, verbose=True)
    
        #     diff = 0
        #     for u_id, u_b in userBelief.items():
        #         diff += abs(u_b - new_userBelief[u_id])
        #     print('diff in user belief = %f' % diff)
    
        #     diff = 0
        #     for p_id, p_b in prodBelief.items():
        #         diff += abs(p_b - new_prodBelief[p_id])
        #     print('diff in product belief = %f' % diff)
    
        #     diff = 0
        #     for r_id, r_b in reviewBelief.items():
        #         diff += abs(r_b - new_reviewBelief[r_id])
        #     print('diff in review belief = %f' % diff)
