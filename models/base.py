from core import db


def commit(obj):
    """
    Function for convenient commit
    """
    db.session.add(obj)
    db.session.commit()
    db.session.refresh(obj)
    return obj


class Model(object):
    @classmethod
    def create(cls, **kwargs):
        """
        Create new record

        cls: class
        kwargs: dict with object parameters
        """
        obj = cls(**kwargs)
        return commit(obj)

    @classmethod
    def update(cls, row_id: int, **kwargs: dict):
        """
        Update record by id

        cls: class
        row_id: record id
        kwargs: dict with object parameters
        """
        obj = cls.query.get(row_id)
        if obj:
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
        return commit(obj)
    
    @classmethod
    def delete(cls, row_id):
        """
        Delete record by id

        cls: class
        row_id: record id
        return: int (1 if deleted else 0)
        """
        obj = cls.query.get(row_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return 1
        return 0
    
    @classmethod
    def add_relation(cls, row_id, rel_obj):  
        """
        Add relation to object

        cls: class
        row_id: record id
        rel_obj: related object
        """      
        obj = cls.query.get(row_id)
        if cls.__name__ == 'Actor':
            obj.filmography.append(rel_obj)
        elif cls.__name__ == 'Movie':
            obj.cast.append(rel_obj)
        return commit(obj)
            
    @classmethod
    def remove_relation(cls, row_id, rel_obj):
        """
        Remove certain relation

        cls: class
        row_id: record id
        rel_obj: related object
        """
        obj = cls.query.get(row_id)
        if cls.__name__ == 'Actor':
            try:
                idx = obj.filmography.index(rel_obj)
                obj.filmography.pop(idx)
            except ValueError:
                print("Didn't find relation")
        elif cls.__name__ == 'Movie':
            try:
                idx = obj.cast.index(rel_obj)
                obj.cast.pop(idx)
            except ValueError:
                print("Didn't find relation")
        return commit(obj)

    @classmethod
    def clear_relations(cls, row_id):
        """
        Remove all relations by id

        cls: class
        row_id: record id
        """
        obj = cls.query.get(row_id)
        if cls.__name__ == 'Actor':
            obj.filmography = []
        elif cls.__name__ == 'Movie':
            obj.cast = []
        return commit(obj)