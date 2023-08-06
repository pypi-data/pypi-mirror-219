import sys
sys.path.append('../../src/')

from labeled_lda import llda_core
from quickcsv.file import *

class LLDA:
    
    def __init__(self,labeled_docs,language='en') -> None:
        self.labeled_docs=labeled_docs
        self.llda_model = llda_core.LldaModel(labeled_documents=self.labeled_docs, alpha_vector=0.01,language=language)

    def train(self,convergent_method='beta',delta_value=0.01,auto_save_by_num_inter=10,metric_path=None,max_iteration=100,use_convergent=True):
        # print(self.llda_model)
        # training
        # llda_model.training(iteration=10, log=True)
        list_metrics=[]
        count=0
        while True:
            count+=1
            # print("iteration %s sampling..." % (self.llda_model.iteration + 1))
            self.llda_model.training(1)
            # print("after iteration: %s, perplexity: %s" % (llda_model.iteration, llda_model.perplexity()))
            # print("delta beta: %s" % self.llda_model.delta_beta)
            list_metrics.append({
                'iteraction':self.llda_model.iteration,
                'perplexity':self.llda_model.perplexity(),
                "delta beta":self.llda_model.delta_beta,
                # "delta":self.get_theta(),
               #  "beta":self.get_beta()
            })
            if metric_path!=None:
                if self.llda_model.iteration % auto_save_by_num_inter == 0:
                    write_csv(metric_path,list_metrics)
            if count>=max_iteration:
                break
            if use_convergent and self.llda_model.is_convergent(method=convergent_method, delta=delta_value):
                break
            

        if metric_path!=None:
            write_csv(metric_path,list_metrics)

    def get_model(self):
        return self.llda_model
    
    def get_test_perplexity(self,documents,iteration=30,times=10):
        # perplexity
        # calculate perplexity on test data
        perplexity = self.llda_model.perplexity(documents=documents,
                                        iteration=iteration,
                                        times=times)
        # print("perplexity on test data: %s" % perplexity)
        return perplexity
    
    def get_train_perplexity(self):
        return self.llda_model.perplexity()
    
    def save(self,save_model_dir,save_derivative_properties=True):
        # llda_model.save_model_to_dir(save_model_dir, save_derivative_properties=True)
        self.llda_model.save_model_to_dir(save_model_dir,save_derivative_properties=save_derivative_properties)

    def load(self,save_model_dir):
        # load from disk
        self.llda_model = llda_core.LldaModel()
        self.llda_model.load_model_from_dir(save_model_dir, load_derivative_properties=False)
        # print("llda_model_new", self.llda_model)
    
    def get_top_terms_of_topic(self,topic,num=5):
        return self.llda_model.top_terms_of_topic(topic, num, False)

    def get_theta(self):
        return self.llda_model.theta

    def get_beta(self):
        return self.llda_model.beta
    
    def inference(self,document):
        topics = self.llda_model.inference(document=document, iteration=100, times=10)
        return topics
    
    def update(self,more_documents):
        # update
        # print("before updating: ", self.llda_model)
        # update_labeled_documents = [("new example test example test example test example test", ["example", "test"])]
        self.llda_model.update(labeled_documents=more_documents)
        # print("after updating: ", llda_model)

if __name__=="__main__":
    # initialize data
    labeled_documents = [("example example example example example"*10, ["example"]),
                     ("test llda model test llda model test llda model"*10, ["test", "llda_model"]),
                     ("example test example test example test example test"*10, ["example", "test"]),
                     ("good perfect good good perfect good good perfect good "*10, ["positive"]),
                     ("bad bad down down bad bad down"*10, ["negative"])]
    
    llda_model=LLDA(labeled_docs=labeled_documents)
    llda_model.train()
    llda_model.save('../../examples/data/model1')
    llda_model.load('../../examples/data/model1')
    print(llda_model.get_top_terms_of_topic('example'))
    print('theta:',llda_model.get_theta())
    print('beta:',llda_model.get_beta())
    
    