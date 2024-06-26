import os

from pymilvus import (
Collection,
connections,
db,
exceptions,
utility,
CollectionSchema,
DataType,
FieldSchema)


class Milvus:
    def __init__(
        self,
        host=os.getenv("MILVUS_HOST", "localhost"),
        port=os.getenv("MILVUS_PORT", "19530"),
    ):
        self.host = host
        self.port = port
        self.alias = "default"
        self.client = connections.connect(
            alias=self.alias, host=self.host, port=self.port
        )
        try:
            db.create_database("replai")
        except exceptions.MilvusException as me:
            me.message
        finally:
            db.using_database("replai")

    def get_valid_collection_name(self, collection_name):
        """
        if collection name have [",", "|", ";", "!","-","@","."]
        in name we remove that
        and replace with '_'
        """
        delimiters = [",", "|", ";", "!", "-", "@", "."]
        for delimiter in delimiters:
            collection_name = " ".join(collection_name.split(delimiter))
        return "_".join(collection_name.split())

    def get_collection(self, collection_name):
        if self.is_collection_exist(collection_name):
            return Collection(collection_name)
        else:
            raise exceptions.CollectionNotExistException(
                code="-1", message=f"{collection_name} does not exist."
            )

    def create_collection(self, collection_name, schema):
        try:
            return Collection(collection_name, schema)
        except exceptions.MilvusException as me:
            raise me("-1", f"{collection_name} did not create!")

    def upsert_collection(self, collection_name, data):
        """
        this function is for update or insert data

        Args:
            collection_name (_type_): name of collection
            data (_type_): data for store in collection
        """
        this_coll = self.get_collection(collection_name)
        mr = this_coll.upsert(data)
        print(mr)
        this_coll.flush()

    def drop_collection(self, collection_name):
        utility.drop_collection(collection_name)

    def delete_entity(self, collection_name, key_field, id):
        expr = f"{collection_name}_{key_field} == {id}"
        collection = self.get_collection(collection_name)
        collection.delete(expr)

    def search(
        self,
        vectors_to_search,
        collection_name,
        field,
        search_params,
        limit,
        output_fields,
    ):
        this_coll = self.get_collection(collection_name)
        this_coll.load()
        result = this_coll.search(
            data=vectors_to_search,
            anns_field=field,
            param=search_params,
            limit=limit,
            expr=None,
            output_fields=output_fields,
        )
        this_coll.release()
        return result

    def insert(self, collection_name, data):
        """
        Data format
        =====================
        [
            # primary keys
            [1, 2, 3, ...],
            # vectors
            [
                [1.0000649690628052,
                 0.9852553606033325,
                 0.9692840576171875,
                 ...],
            ]
        ]
        """
        collection = self.get_collection(collection_name)
        collection.insert(data)

    def list_of_db(self):
        return db.list_database()

    def is_collection_exist(self, collection_name):
        return utility.has_collection(collection_name)

    def list_of_collections(self):
        return utility.list_collections()

    def create_or_get_name_of_collection(self):
        fields = [
            FieldSchema(
                name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False
            ),
            FieldSchema(
                name="embeddings",
                dtype=DataType.FLOAT_VECTOR,
                dim=512,
            ),
        ]
        collection_name = self.get_valid_collection_name(
            "Mori"
        )
        schema = CollectionSchema(
            fields=fields,
            description=f"{collection_name} collection",
            enable_dynamic_field=True,
        )
        if not self.is_collection_exist(collection_name):
            this_coll = self.create_collection(collection_name, schema)
            index = {
                "index_type": "IVF_SQ8",
                "metric_type": "IP",
                "params": {"nlist": 128},
            }
            this_coll.create_index("embeddings", index)
        return collection_name