from marshmallow import Schema, fields


class PostSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    datetime = fields.Str()
    author = fields.Str()
    text = fields.Str()


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()
    admin = fields.Int()
