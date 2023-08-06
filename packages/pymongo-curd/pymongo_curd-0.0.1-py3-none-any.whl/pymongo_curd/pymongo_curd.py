from bson import ObjectId


class Document:
    def __init__(self, collection):
        """
        传入集合
        :param collection:集合名称
        """
        self._coll = collection

    def get(self,
            query: dict = None,
            projection: dict = None,
            skip: int = 0,
            limit: int = 0,
            sort: list = None):
        """
        查询所有文档
        :param query: 查询条件，dict 类型，若为空，则查询所有
        :param projection: 投影条件，dict 类型，若为空，则展示所有字段
        :param skip: 跳过多少条
        :param limit: 展示多少条
        :param sort: 排序。列表元组类型， [(),]
        :return: 若能查出数据，则返回数据列表，若查询不到，则返回 空列表
        """
        if query is None:
            select = {}

        if projection is None:
            projection = {}

        if sort:
            res_list = [item for item in self._coll.find(query, projection).skip(skip).limit(limit).sort(sort)]
            return res_list if res_list else []

        res_list = [item for item in self._coll.find(query, projection).skip(skip).limit(limit)]
        return res_list if res_list else []

    def get_by_id(self, _id: str):
        """
        通过 id 查询
        :param _id: str类型的 _id
        :return: 如果查询得到，则返回 dict 类型的数据，如果查询不到，则返回 None
        """
        query = {'_id': ObjectId(_id)}
        return self._coll.find_one(query)

    def post(self, document: dict):
        """
        新增一个文档
        :param document: 新增的文档， dict 类型
        :return: 新增文档的 _id
        """
        result = self._coll.insert_one(document)
        return result.inserted_id

    def put(self, _id: str, modify_doc: dict):
        """
        根据 _id 修改文档
        :param _id: 要修改的文档的 _id
        :param modify_doc: 修改文档内容
        :return: 返回修改的文档数量，0 代表没有做任何修改
        """
        query = {'_id': ObjectId(_id)}
        modify_doc = {'$set': modify_doc}
        result = self._coll.update_one(query, modify_doc)

        return result.modified_count

    def delete(self, _id: str):
        """
        根据 _id 删除文档
        :param _id: 要删除的文档的 _id
        :return: 返回删除的文档数量，0 代表没有文档删除
        """
        select = {'_id': ObjectId(_id)}
        result = self._coll.delete_one(select)
        return result.deleted_count

    def put_and_chick_repeat(self, _id: str, modify_doc: dict, chick_filed: str):
        """
        修改文档，并且检查特定字段是否 重复
        :param _id: 要修改的文档 _id
        :param modify_doc: 修改文档内容
        :param chick_filed: 要检查重复的 字段
        :return: 返回修改的文档数量，0 代表没有做任何修改。 重复返回 repeat
        """
        query = {chick_filed: modify_doc[chick_filed]}
        chick_repeat_result = self._coll.find_one(query)  # 检查重复结果
        if chick_repeat_result:
            if chick_repeat_result['_id'] == ObjectId(_id):
                return self.put(_id, modify_doc)
            else:
                return 'repeat'

        return self.put(_id, modify_doc)

    def post_and_chick_repeat(self, document: dict, chick_filed: str):
        """
        新增文档，并且检查特定字段是否重复
        :param document: 新增的文档
        :param chick_filed: 要检查重复的 字段
        :return: 返回新增文档的 _id，如果重复，返回 repeat
        """
        query = {chick_filed: document[chick_filed]}
        if self.get(query):
            return 'repeat'

        return self.post(document)


class SecDocument(Document):
    def post_sec(self, _id: str, sec_filed: str, document: dict):
        """
        二级文档的新增，
        会为二级文档新增一个 '_id' 为二级文档唯一标识符 str 类型。
        :param _id: 一级文档的 _id
        :param sec_filed: 二级文档的字段
        :param document: 新增的二级文档
        :return: 返回新增的文档数量，0 代表没有新增，1 为新增成功
        """
        query = {'_id': ObjectId(_id)}
        document['_id'] = str(ObjectId())  # 新增一个 二级文档内的 唯一标识符
        post_doc = {'$push': {sec_filed: document}}

        result = self._coll.update_one(query, post_doc)

        return result.modified_count

    def put_sec(self, _id: str, sec_id: str, sec_filed: str, modify_doc: dict):
        """
        修改二级文档，\n
        请注意！
        二级文档内一定要携带 _id
        :param _id: 一级文档 _id
        :param sec_id: 二级文档 _id
        :param sec_filed: 二级文档的字段
        :param modify_doc: 修改的二级文档
        :return: 返回修改的文档数量，0 代表没有做任何修改
        """
        query = {'_id': ObjectId(_id), f'{sec_filed}._id': sec_id}
        put_doc = {'$set': {f'{sec_filed}.$': modify_doc}}

        result = self._coll.update_one(query, put_doc)
        return result.modified_count

    def delete_sec(self, _id: str, sec_id: str, sec_filed: str):
        """
        删除一个二级文档
        :param _id: 一级文档 _id
        :param sec_id: 二级文档 _id
        :param sec_filed: 二级文档字段
        :return: 返回删除的文档数量，0 代表没有文档删除
        """
        query = {'_id': ObjectId(_id)}
        del_doc = {'$pull': {sec_filed: {'_id': sec_id}}}
        result = self._coll.update_one(query, del_doc)
        return result.modified_count

    def post_sec_and_chick_repeat(self, _id: str, sec_filed: str, document: dict, chick_filed: str):
        """
        新增二级文档，并且检查 特定字段 重复
        :param _id: 一级文档 _id
        :param sec_filed: 二级文档的字段
        :param document: 新增的二级文档
        :param chick_filed: 检查重复的字段
        :return: 返回新增的文档数量，0 代表没有新增，1 为新增成功。 如果重复，返回 repeat
        """
        query = {'_id': ObjectId(_id), f'{sec_filed}.{chick_filed}': document[chick_filed]}
        if self.get(query):
            return 'repeat'

        return self.post_sec(_id, sec_filed, document)

    def put_sec_and_chick_repeat(self, _id: str, sec_id: str, sec_filed: str, modify_doc: dict, chick_filed: str):
        """
        修改文档，并且检查 特定字段 重复
        :param _id: 一级文档 _id
        :param sec_id: 二级文档 _id
        :param sec_filed: 二级文档的字段
        :param modify_doc: 修改的 二级文档
        :param chick_filed: 检查重复的字段
        :return: 返回修改的文档数量，0 代表没有新增，1 为修改成功。 如果重复，返回 repeat
        """
        query = {'_id': ObjectId(_id), f'{sec_filed}.{chick_filed}': modify_doc[chick_filed]}
        chick_repeat_result = self._coll.find_one(query)
        if chick_repeat_result:

            for i in chick_repeat_result[sec_filed]:
                if i[chick_filed] == modify_doc[chick_filed]:
                    if i['_id'] == sec_id:
                        return self.put_sec(_id, sec_id, sec_filed, modify_doc)

            return 'repeat'

        return self.put_sec(_id, sec_id, sec_filed, modify_doc)
