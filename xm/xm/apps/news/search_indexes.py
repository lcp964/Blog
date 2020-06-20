from haystack import indexes #导入搜索接口
from .models import News  #导入新闻列表需要在里面进行展示

#建立索引模型类
class NewsIndex(indexes.SearchIndex,indexes.Indexable):
    """
       News索引数据模型类
       可以借用 hay_stack 借助 ES 来查询
       """
    #  主要进行关键字查询 标题，作者，文章，内容
    text = indexes.CharField(document=True,use_template=True) #指定字段为True
    id = indexes.IntegerField(model_attr='id')
    title = indexes.CharField(model_attr='title')
    digest = indexes.CharField(model_attr='digest')
    content = indexes.CharField(model_attr='content')
    image_url = indexes.CharField(model_attr='image_url')

    def get_model(self):
        """返回建立索引的模型类
        """
        return News

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集
        """

        return self.get_model().objects.filter(is_delete=False)