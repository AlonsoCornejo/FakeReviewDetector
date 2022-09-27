"""
	Define operations of review data:
	1) remove some reviews from the data
	2) add reviews to the data
"""

from numpy import random

def remove_reviews(user_data, prod_data):
    """take out some review data
    """
    u_ids = [k for k,v in user_data.items()]
    selected_u = random.choice(u_ids, 100, replace=False)
#     selected_u = [u_ids[0]]
#     print ('removed id = %s' % selected_u[0])
#     print ('number of missing reviews: %d' % len(selected_u))
#     break
    new_user_data = {}
    new_prod_data = {}
    
    for i in selected_u:
        # just take the first review out
        new_user_data[i] = [user_data[i][0]]
        target_id = user_data[i][0][0]
        
        user_data[i].pop(0)
        
        # remove the user if there is no review
        if len(user_data[i]) == 0:
            user_data.pop(i)
            
        if target_id not in new_prod_data:
            new_prod_data[target_id] = []
        prod_added = False
        for r in prod_data[target_id]:
            if r[0] == i:
                prod_added = True
                new_prod_data[target_id].append(r)
                prod_data[target_id].remove(r)
                
                if len(prod_data[target_id]) == 0:
                    prod_data.pop(target_id)
                break
        assert (prod_added == True)
    
    for u, r in new_user_data.items():
        found = False
        for p, rr in new_prod_data.items():
            for i in rr:
                if i[0] == u:
                    found = True
                    break
            if found:
                break
        assert found==True, 'user %s not found in product data' % u
        
    for p, r in new_prod_data.items():
        for i in r:
            assert i[0] in new_user_data, 'product %s not found in user data' % i[0]
    return new_user_data, new_prod_data

def insert_reviews(user_data, prod_data, new_user_data):
    """ Insert reviews into existing ones
    """
    for k,v in new_user_data.items():
        for review in v:
            if k not in user_data:
                user_data[k] = []
            user_data[k].append(review)
            
            product_id = review[0]
            if product_id not in prod_data:
                prod_data[product_id] = []
            # create and insert a review tuple (user_id, rating, label, date) for the product
            prod_data[product_id].append((k, review[1], review[2], review[3]))

def user_to_prod_view(user_data):
	""" Convert a set of reviews from user-centric view to product-centric view
	"""
	prod_data = {}
	for k, reviews in user_data.items():
		for r in reviews:
			prod_id = r[0]
			rating = r[1]
			label = r[2]
			date = r[3]
			
			if prod_id not in prod_data:
				prod_data[prod_id] = []
			prod_data[prod_id].append((k, rating, label, date))
	return prod_data

def prod_to_user_view(prod_data):
	""" Convert a set of reviews from product-centric view to review-centric view
	"""
	user_data = {}
	for k, reviews in prod_data.items():
		for r in reviews:
			user_id = r[0]
			rating = r[1]
			label = r[2]
			date = r[3]
			
			if user_id not in user_data:
				user_data[user_id] = []
			user_data[user_id].append((k, rating, label, date))
	return user_data

