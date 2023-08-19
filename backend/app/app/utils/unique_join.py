from sqlalchemy.sql import visitors
from contextlib import suppress

def has_entity(self, model) -> bool:
    for visitor in visitors.iterate(self.statement):
        # Checking for `.join(Parent.child)` clauses
        if visitor.__visit_name__ == 'binary':
            for vis in visitors.iterate(visitor):
                # Visitor might not have table attribute
                with suppress(AttributeError):
                    # Verify if already present based on table name
                    if model.__table__.fullname == vis.table.fullname:
                        return True
        # Checking for `.join(Child)` clauses
        if visitor.__visit_name__ == 'table':
            # Visitor might be of ColumnCollection or so,
            # which cannot be compared to model
            with suppress(TypeError):
                if model == visitor.entity_namespace:
                    return True
        # Checking for `Model.column` clauses
        if visitor.__visit_name__ == "column":
            with suppress(AttributeError):
                if model.__table__.fullname == visitor.table.fullname:
                    return True
    return False

def unique_join(self, model, *args, **kwargs):
    """Join if given model not yet in query"""
    if not self.has_entity(model):
        self = self.join(model, *args, **kwargs)
    return self