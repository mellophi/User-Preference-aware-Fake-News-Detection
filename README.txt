1. Please install the modules mentioned in requirements.txt

2. Copy the required dataset into 
	data\gossipcop\raw and
	data\politifact\raw
3. Delete the folders before starting to run the model if you need to create a fresh copy of processed data:
	data\gossipcop\processed and
	data\politifact\processed

3. To run the model, use the following command:
	python -u gnn.py --model gcn --feature bert --epochs 500 --lr 0.001 --nhid 128 --batch_size 128 --dataset politifact --device cpu --concat True --cluster False

4. The meaning of the hyperparameters are as follows:
	dataset: politifact or gossipcop                                | default='politifact'
	batch_size: batch size                                          | default=128
	lr: learning rate                                               | default=0.01
	weight_decay: weight decay                                      | default=0.01
	nhid: hidden size                                               | default=128
	dropout_ratio: dropout ratio                                    | default=0.0
	epochs: maximum number of epochs                                | default=35
	concat: whether concat news embedding and graph embedding       | default=True
	multi_gpu: multi-gpu mode                                       | default=False
	feature: feature type, [profile, spacy, bert, content]          | default='bert'
	model: model type, [gcn, gat, sage]                             | default='sage'
	cluster: whether want to use clustered endogeneous features     | default=False

5. To run the model provided in research paper, use cluster = False.

6. To run the model with the proposed approach (whether want to use clustered endogeneous features) use cluster = True

7. The accuracy is shown as output in the end.
