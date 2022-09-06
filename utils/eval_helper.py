from sklearn.metrics import f1_score, accuracy_score, recall_score, precision_score, roc_auc_score, average_precision_score


"""
	Utility functions for evaluating the model performance
"""


def eval_deep(log, loader):
	"""
	Evaluating the classification performance given mini-batch data
	"""

	# get the empirical batch_size for each mini-batch
	data_size = len(loader.dataset.indices)

	# Here the batchsize is taken as arguments in input
	batch_size = loader.batch_size
	if data_size % batch_size == 0:
		size_list = [batch_size] * (data_size//batch_size)
	else:
		size_list = [batch_size] * (data_size // batch_size) + [data_size % batch_size]
	# size_list will always be equal to data_size, I don't know why it is written in code
	# Used for debugging purpose
	assert len(log) == len(size_list)

	accuracy, f1_macro, f1_micro, precision, recall = 0, 0, 0, 0, 0

	prob_log, label_log = [], []

	for batch, size in zip(log, size_list):
		# Here log is basically, out_log.append([F.softmax(out, dim=1), y])
		# argmax will give the highest value probability out of the softmax layer to make prediction
		# whereas y will store the actual prediction
		pred_y, y = batch[0].data.cpu().numpy().argmax(axis=1), batch[1].data.cpu().numpy().tolist()

		# appending prediction as numpy array (converted to list) to prob_log
		prob_log.extend(batch[0].data.cpu().numpy()[:, 1].tolist())

		# appending prediction as numpy array (converted to list) to label_log
		label_log.extend(y)

		# Applying evaluation function on y and y_pred
		accuracy += accuracy_score(y, pred_y) * size
		f1_macro += f1_score(y, pred_y, average='macro') * size
		f1_micro += f1_score(y, pred_y, average='micro') * size
		precision += precision_score(y, pred_y, zero_division=0) * size
		recall += recall_score(y, pred_y, zero_division=0) * size

	auc = roc_auc_score(label_log, prob_log)
	ap = average_precision_score(label_log, prob_log)

	return accuracy/data_size, f1_macro/data_size, f1_micro/data_size, precision/data_size, recall/data_size, auc, ap
