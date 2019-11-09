from api import ma
from api.users.models import User,Role,RolesUsers


class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role


role_schema = RoleSchema(many=False)
roles_schema = RoleSchema(many=True)


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        exclude = ('password',)

    # role = ma.Function(lambda obj: obj.roles)
    roles = ma.Nested(RoleSchema, many=True)


user_schema = UserSchema(many=False)
users_schema = UserSchema(many=True)


class RolesUsersSchema(ma.ModelSchema):
    class Meta:
        model = RolesUsers


roleuser_schema = RolesUsersSchema(many=False)
roleusers_schema = RolesUsersSchema(many=True)
