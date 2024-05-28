"""
File containing the functions to serialize mongo docs
conforming to pydantic requirements
"""


def convert_doc(document) -> dict:
    """
    since fields starting with _ are considerated as private in python
    the solution consists of writing a function that adapts Mongo documents
    for use with Pydantic by renaming _id field to id.
    _id is the prymary key for mongo documents
    """
    return {
        "id": str(document["_id"]),
        "title": document["title"],
        "release_date": document["release_date"],
        "genre": document["genre"]
    }


def convert_doc_list(documents) -> list:
    """
    apply convert_doc to each elemnt of a list of docs
    """
    return [convert_doc(doc) for doc in documents]
