import colander


class Test(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), default='Not specific')
    count = colander.SchemaNode(colander.Int(), validator=colander.Range(1, 999), default=0)
