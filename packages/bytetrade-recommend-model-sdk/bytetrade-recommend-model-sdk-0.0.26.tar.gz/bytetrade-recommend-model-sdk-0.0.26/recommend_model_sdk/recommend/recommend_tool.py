import faiss
import numpy as np
from datetime import datetime


from recommend_model_sdk.tools.common_tool import CommonTool
from recommend_model_sdk.mind_sdk.config.content_similar_config import ContentSimilarConfig
from recommend_model_sdk.mind_sdk.model.content_similar_model import ContentSimilarModelRecall

class RecommendTool:

    def __init__(self, base_document_id_to_embedding,
                 pretrained_item_embedding_model_name,
                 pretrained_item_embedding_model_version) -> None:
        """_summary_

        Args:
            base_document_id_to_embedding (_type_): _description_
            {
                "document_id":{
                    "embedding":[],numpy
                    "created_at": datetime
                }
            }

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
        """
        
        content_config = ContentSimilarConfig(pretrained_item_embedding_model_name,pretrained_item_embedding_model_version)
        self.__content_similar_model = ContentSimilarModelRecall(base_document_id_to_embedding,content_config)

    
    def __recall_content_similar(self,candidate_document_id_to_document_info,limit = 100):
        url_weight_tuple_list = self.__content_similar_model.recall(candidate_document_id_to_document_info,limit)
        return url_weight_tuple_list
    
    def __rank_content_similar(self):
        pass
    
    def recommend(self,candidate_document_id_to_document_info,rank_limit=100):
        return self.__recall_content_similar(candidate_document_id_to_document_info,rank_limit)
        
    
